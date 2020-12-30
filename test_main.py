from celery.utils.collections import ChainMap
from celery import chain
from config import global_config
from crawlers import crawler_interface as ci
from crawler_tasks import search_app as sa
from crawler_tasks import get_reviews as gr


print(
    """ 
        -------------------------------------------------------------------------------------------------------------
        Launched sample file of the engine. Please make sure RabbitMQ & Celery are ready to run.
        --------------------------------------------------------------------------------------------------------------
    """
)
# THe only place an Instance of global_values is created
config = global_config.global_config.get_instance().CFG

print(config)

processed_data = chain(sa.s(ci.crawler_types.PLAY_STORE, "Facebook", 0), gr.s()).apply_async().get()

print("\n----------------- Completed -------------------------------")