from django.http import HttpResponse
from wapps.errors import HttpResponseError


def error(request):
    response = HttpResponse('42', status=442)
    raise HttpResponseError(response)


def first_visit(request):
    return HttpResponse(request.session.get('first_visit'))
