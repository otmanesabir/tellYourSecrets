import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from crawlers import play_store as ps
from crawlers import app_store
import logger

# Waits to receive a request with a name.
# Once received {name}:
  # request a sample of the first apps given a name
  # write those to the firestore
  # send requests to the crawlers
  # get latest information

# Use the application default credentials

log = logger.setup_custom_logger(__name__)

def sample_write(searchField):
  cred = credentials.Certificate("/Users/otmanesabir/tellyoursecrets-pro-firebase-adminsdk.json")
  firebase_admin.initialize_app(cred)
  db = firestore.client()
  apps = ps.search_app_name(searchField, 0)
  
  for app in apps:
    doc_ref = db.collection(u'apps').document(app.bundle_id)
    if doc_ref.get().exists:
      log.warning(f'Already exists. Updating {app.bundle_id}')
      doc_ref.update(app.to_dict())
    else:
      doc_ref.set(app.to_dict())
    reviews = ps.get_reviews(app, 20)
    
    # parse reviews for each of these apps
    for r in reviews:
      db.collection(u'reviews').add(r.to_dict())
    log.info(f"Finished writing {len(reviews)} reviews to firestore")
  log.info(f"Finished writing {len(apps)} apps to firestore")
