from models import app_info
from crawlers import play_store as ps
from crawlers import app_store
import datetime as dt
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

print("\n----------------- Completed -------------------------------")

samurai_bs = app_info.app_info("Samurai Slash Run Slice", "https://play.google.com/store/apps/details?id=com.innersloth.spacemafia", "https://apps.apple.com/us/app/samurai-slash-run-slice/id1535201167", dt.date.today)
reviews = app_store.getReviews(samurai_bs, 20)
for r in reviews:
    print(r)