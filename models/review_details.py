from config.global_config import global_config
from firebase_admin import credentials, firestore
from dataclasses import dataclass
import datetime

import firebase_admin
import logger


# TODO somehow make reviews unique
log = logger.setup_custom_logger(__name__)
config = global_config.get_instance().CFG

@dataclass
class review_details(dict):
    bundle_id: str
    app_name: str
    description: str
    date: datetime.date
    rating: str

    def __init__(self, bundle_id, app_name, description, date, rating):
        dict.__init__(self, bundle_id=bundle_id, app_name=app_name, description=description, date=date, rating=rating)

    @classmethod
    def from_dict(obj, dictionary):
        return obj(dictionary["bundle_id"], dictionary["app_name"], dictionary["description"], dictionary["date"], dictionary["rating"])
    
    def __init_db():
        if not firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
            cred = credentials.Certificate(config["firebase_credentials"])
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db

    def write_to_db(self):
        db = self.__init_db()
        if (self.bundle_id is None):
            log.warning(f"Can't write an instance of app_info with no bundle_id")
            return False
        doc_ref = db.collection(u'reviews').document(self.bundle_id)
        if doc_ref.get().exists:
            log.warning(f'Already exists. Updating {self.bundle_id}')
            doc_ref.update({u'reviews': firestore.ArrayUnion([self.to_dict()])})
        else:
            doc_ref.set({u'reviews': [self.to_dict()]})
        return True

    
    def to_dict(self):
        dest = {
            u'app_name': self.app_name,
            u'description': self.description,
        }

        if self.date is not None:
            dest[u'date'] = self.date.strftime('%m/%d/%Y')
        if self.rating is not None:
            dest[u'rating'] = self.rating

        return dest
    
    def __repr__(self):
        return(
            f'review_details(\
                app_name={self.app_name}, \
                description={self.description}, \
                date={self.date}, \
                rating={self.rating}\
            )'
        )
