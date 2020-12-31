from collections import namedtuple
from celery import Celery, subtask, group
from crawlers import play_store, app_store, crawler_interface
from models import app_info as ai

ct = crawler_interface.crawler_types

## celery -A crawler_tasks worker --loglevel=INFO
app = Celery('crawler_tasks', backend='rpc://', broker='pyamqp://', task_serializer='pickle', result_serializer='pickle', accept_content=['application/json'])

@app.task
def get_reviews(value):
    apps, crawler_type = value
    res = []
    for app_info in apps:
        app_info = ai.app_info.from_dict(app_info)
        if (crawler_type == ct.PLAY_STORE):
            res.append(play_store.play_store_crawler().get_reviews(app_info))
        elif (crawler_type == ct.APP_STORE):
            res.append(app_store.app_store_crawler().get_reviews(app_info))
        elif (crawler_type == ct.ALL):
            res.append(play_store.play_store_crawler().get_reviews(app_info))
            res.append(app_store.app_store_crawler().get_reviews(app_info))
    return res

@app.task
def search_app(crawler_type, app_name, start_idx):
    res = []
    if (crawler_type == ct.PLAY_STORE):
        res = play_store.play_store_crawler().search_app_name(app_name, start_idx)
    elif (crawler_type == ct.APP_STORE):
        res = app_store.app_store_crawler().search_app_name(app_name, start_idx)
    elif (crawler_type == ct.ALL):
        res = play_store.play_store_crawler().search_app_name(app_name, start_idx)
        res.append(app_store.app_store_crawler().search_app_name(app_name, start_idx))
    return res, crawler_type