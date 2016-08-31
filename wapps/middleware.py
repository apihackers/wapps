from django.middleware.locale import LocaleMiddleware


class AdminLocaleMiddleware(LocaleMiddleware):
    ALLOWED_PATHS = [
        '/admin',
    ]

    def process_request(self, request):
        print('process', request.path)
        if any(request.path.startswith(p) for p in self.ALLOWED_PATHS):
            return super(AdminLocaleMiddleware, self).process_request(request)

    # def process_response(self, request, response):
    #     print('response', request.path)
    #     if any(request.path.startswith(p) for p in self.ALLOWED_PATHS):
    #         return super(AdminLocaleMiddleware, self).process_response(request, response)


class FirstVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['first_visit'] = not (request.session.get('visited', False) or request.user.is_authenticated())
        response = self.get_response(request)
        request.session['visited'] = True
        return response
