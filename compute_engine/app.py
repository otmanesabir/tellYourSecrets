from flask import Flask, request
from flask.helpers import make_response
from crawler_tasks import search_app as sa
from crawler_tasks import get_reviews as gr
from models import app_info as ai
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
        log.error("did not receive valid JSON... will not proceed")
        return make_response('Bad Request', 400)
    data = request.get_json()
    if (data["search_type"] == "apps"):
        results = sa.delay(data["crawler"], data["keyword"], data["start_index"]).get()
        gr.delay(data["crawler"], results) # don't really need to wait for these results.
        dictToSend = {'bundle_ids': [d['bundle_id'] for d in results]}
        # TODO SEND TO THE WEB APP
        res = requests.post('http://localhost:5000/post/receive/apps', json=dictToSend)
        print('response from server:', res.status_code)
    elif (data["search_type"] == "reviews"):
        apps = ai.app_info.load_from_bundle_id(data["bundle_ids"])
        gr.delay(data["crawler"], apps)
    return make_response('Succesfully Processed!', 201) # response to our request.

if __name__ == "__main__":
    app.run()