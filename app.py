from flask import Flask, request
from flask.helpers import make_response
from crawler_tasks import search_app as sa
from crawler_tasks import get_reviews as gr
import requests
import logger


app = Flask(__name__)
log = logger.setup_custom_logger(__name__)

@app.route('/')
def hello():
    return 'Home page'

@app.route('/post/receive/apps', methods=['POST'])
def receive_test():
    if (request.is_json):
        print("received info")
    dictFromServer = request.get_json()
    print(dictFromServer)
    return 'Home page'

@app.route('/post', methods=['POST'])
def get_request():
    if not request.is_json:
        log.error("Did not receive JSON will not proceed")
        return make_response('Bad Request', 404)
    data = request.get_json()
    if (data["search_type"] == "apps"):
        results = sa.delay(data["crawler"], data["keyword"], data["start_index"]).get()
        gr.delay(data["crawler"], results) # don't really need to wait for these results.
        bundles = []
        for result in results:
            bundles.append(result["bundle_id"])
        dictToSend = {'bundle_ids': bundles}
        res = requests.post('http://localhost:5000/post/receive/apps', json=dictToSend)
        print('response from server:', res.status_code)
        return make_response('Received !', 201) # response to your request.

if __name__ == "__main__":
    app.run()