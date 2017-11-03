
class HttpResponseError(Exception):
    '''A prerendered HTTP response as exception'''
    def __init__(self, response):
        self.response = response
