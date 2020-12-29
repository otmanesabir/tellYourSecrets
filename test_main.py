import play_store as ps
import datetime as dt
import app_info
from config import global_config

print(
    """ 
        ----------------------------------------------------------
        Loading the global values of this environment.
        -----------------------------------------------------------
    """
)
# THe only place an Instance of global_values is created
globalvalues = global_config.global_config.get_instance()

print(globalvalues.CFG)

print("----------------- Completed -------------------------------")

among_us = app_info.app_info("Among Us", "https://play.google.com/store/apps/details?id=com.innersloth.spacemafia", "", dt.date.today)
reviews = ps.getReviews(among_us, 10)
for r in reviews:
    print(r)