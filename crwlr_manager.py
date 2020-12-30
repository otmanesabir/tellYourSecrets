import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from crawlers import play_store as ps
from crawlers import app_store
from config import global_config
import logger

cfg = global_config.global_config.get_instance().CFG 

# Waits to receive a request with a name.
# Once received {name}:
  # request a sample of the first apps given a name
  # write those to the firestore
  # send requests to the crawlers
  # get latest information

# Use the application default credentials

log = logger.setup_custom_logger(__name__)

def sample_write(searchField):
  cred = credentials.Certificate(cfg["firebase_credentials"])
  firebase_admin.initialize_app(cred)
  crawler = ps.play_store_crawler()
  apps = crawler.search_app_name(searchField, 0)
  
  for app in apps:
    app.write_to_db()
    reviews = crawler.get_reviews(app)
    # parse reviews for each of these apps
    for r in reviews:
      r.write_to_db()
    log.info(f"Finished writing {len(reviews)} reviews to firestore")
  log.info(f"Finished writing {len(apps)} apps to firestore")
