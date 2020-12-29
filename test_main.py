from models import app_info
from crawlers import play_store as ps
from crawlers import app_store
import datetime as dt
from config import global_config
import crwlr_manager as cm

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

cm.sample_write("Idiot")