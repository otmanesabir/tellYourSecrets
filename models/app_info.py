class app_info:
    def __init__(self, app_name, android_link, apple_link, last_saved_review):
        self.app_name = app_name
        self.android_link = android_link
        self.apple_link = apple_link
        self.last_saved_review = last_saved_review

    def __repr__(self):
        return(
            f'app_info(\
                app_name={self.app_name}, \
                android_link={self.android_link}, \
                apple_link={self.apple_link}, \
                last_saved_review={self.last_saved_review}\
            )'
        )