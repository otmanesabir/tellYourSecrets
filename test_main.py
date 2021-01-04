import requests
from config import global_config


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

print("\n----------------- LOADED CONFIG -------------------------------\n")

payload = {'search_type': 'reviews', 'bundle_ids': ['com.facebook.analytics', 'com.facebook.games'], 'crawler': 'app store'} 
r = requests.post("http://127.0.0.1:5000/post", json=payload)
print(r.status_code)


print("\n----------------- Completed -------------------------------")