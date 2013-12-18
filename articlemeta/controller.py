from xylose.scielodocument import Article


class DataBroker(object):

    def __init__(self, databroker):
        self.db = databroker


    def get_article(self, code):

        data = self.db.find_one({'code': code})

        del(data['_id'])
        
        return data

