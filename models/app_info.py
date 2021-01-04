from config.global_config import global_config
from firebase_admin import credentials, firestore
from dataclasses import dataclass
import datetime

import firebase_admin
import logger

log = logger.setup_custom_logger(__name__)
config = global_config.get_instance().CFG

@dataclass
class app_info(dict):
    bundle_id: str
    app_name: str
    android_link: str
    apple_link: str
    last_saved_review: datetime.date

    def __init__(self, bundle_id, app_name, android_link, apple_link, last_saved_review):
        self.bundle_id = bundle_id
        self.app_name = app_name
        self.android_link = android_link
        self.apple_link = apple_link
        self.last_saved_review = last_saved_review
        dict.__init__(self, bundle_id=bundle_id, app_name=app_name, android_link=android_link, apple_link=apple_link, last_saved_review=last_saved_review)

    @classmethod
    def from_dict(obj, dictionary):
        bi = dictionary["bundle_id"]
        an = dictionary["app_name"]
        al = apl = lrw = None
        if dictionary.get("android_link") != None:
            al = dictionary["android_link"]
        if dictionary.get("apple_link") != None:
            apl = dictionary["apple_link"]
        if dictionary.get("last_saved_review") != None:
            lrw = dictionary["last_saved_review"]
        return obj(bi, an, al, apl, lrw)
     
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
        doc_ref = db.collection(u'apps').document(self.bundle_id)
        if doc_ref.get().exists:
            log.warning(f'Already exists. Updating {self.bundle_id}')
            doc_ref.update(self.to_dict())
        else:
            doc_ref.set(self.to_dict())
        return True
    
    def update_date(self, date):
        db = self.__init_db()
        if (self.bundle_id is None):
            log.error(f"Can't write an instance of app_info with no bundle_id")
            return False
        if (date is None):
            return False
        doc_ref = db.collection(u'apps').document(self.bundle_id)
        doc_ref.update({u'last_saved_review': date.strftime('%m/%d/%Y')})
        return True
    
    @classmethod
    def load_from_bundle_id(self, bundle_id):
        if not type(bundle_id) is list:
            bundle_id = [bundle_id]
        if not bundle_id[0]:
            log.error(f"Can't load an instance of app_info with no bundle_id")
            raise Exception("Invalid bundle id.")
        db = self.__init_db()
        apps = []
        for id in bundle_id:
            doc_ref = db.collection(u'apps').document(id)
            if not doc_ref.get().exists:
                log.warning(f"App with {id} does not exist")
            else:
                apps.append(self.from_dict(doc_ref.get().to_dict()))
        log.info(f"Succesfully loaded {len(apps)}/{len(bundle_id)} apps.")
        if len(apps) == 1:
            return apps[0]
        else:
            return apps


    def to_dict(self):
        dest = {
            u'bundle_id': self.bundle_id,
            u'app_name': self.app_name,
        }

        if self.android_link is not None:
            dest[u'android_link'] = self.android_link
        if self.apple_link is not None:
            dest[u'apple_link'] = self.apple_link
        if self.last_saved_review is not None:
            dest[u'last_saved_review'] = self.last_saved_review

        return dest

    def __repr__(self):
        return(
            f'app_info(\
                bundle_id={self.bundle_id}, \
                app_name={self.app_name}, \
                android_link={self.android_link}, \
                apple_link={self.apple_link}, \
                last_saved_review={self.last_saved_review}\
            )'
        )