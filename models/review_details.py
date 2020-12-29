class review_details:
    def __init__(self, app_name, description, date, rating):
        self.app_name = app_name
        self.description = description
        self.date = date
        self.rating = rating
    
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
