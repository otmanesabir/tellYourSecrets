from flask import Flask, request
from flask.helpers import make_response
from crawler_tasks import search_app as sa
from crawler_tasks import get_reviews as gr
from celery import chain
import logger


app = Flask(__name__)
log = logger.setup_custom_logger(__name__)

@app.route('/')
def hello():
    return 'Home page'

@app.route('/post', methods=['POST'])
def get_request():
    if not request.is_json:
        log.error("Did not receive JSON will not proceed")
        return make_response('Bad Request', 404)
    data = request.get_json()
    chain(sa.s(data["crawler"], data["keyword"], data["start_index"]), gr.s()).apply_async()
    return make_response('Received !', 201) # response to your request.

if __name__ == "__main__":
    app.run()