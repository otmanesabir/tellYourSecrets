import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logger

log = logger.setup_custom_logger(__name__)

class app_info(dict):
    def __init__(self, bundle_id, app_name, android_link, apple_link, last_saved_review):
        dict.__init__(self, bundle_id=bundle_id, app_name=app_name, android_link=android_link, apple_link=apple_link, last_saved_review=last_saved_review)

    def __init_db():
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
            log.warning(f"Can't write an instance of app_info with no bundle_id")
            return False
        if (date is None):
            return False
        doc_ref = db.collection(u'apps').document(self.bundle_id)
        doc_ref.update({u'last_saved_review': date.strftime('%m/%d/%Y')})
        return True

    @staticmethod
    def from_dict(source):
        pass
        # ...

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