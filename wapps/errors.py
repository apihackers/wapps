
class HttpResponseError(Exception):
    '''A prerendered HTTP response as exception'''
    def __init__(self, response):
        self.response = response


class ErrorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, ex):
        if isinstance(ex, HttpResponseError):
            return ex.response
