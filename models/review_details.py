class review_details:
    def __init__(self, app_name, description, date, rating):
        self.app_name = app_name
        self.description = description
        self.date = date
        self.rating = rating

    def __repr__(self):
        return(
            f'review_details(\
                app_name={self.app_name}, \
                description={self.description}, \
                date={self.date}, \
                rating={self.rating}\
            )'
        )
