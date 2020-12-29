# uses the bundle ID as the file name and the main app identifier.

class app_info:
    def __init__(self, bundle_id, app_name, android_link, apple_link, last_saved_review):
        self.bundle_id = bundle_id
        self.app_name = app_name
        self.android_link = android_link
        self.apple_link = apple_link
        self.last_saved_review = last_saved_review


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