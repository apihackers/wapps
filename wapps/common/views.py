from django.shortcuts import redirect

from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found


def image(request, pk, specs):
    '''
    Request an image given some specs and redirects to it
    '''
    image = Image.objects.get(pk=pk)
    rendition = get_rendition_or_not_found(image, specs)
    return redirect(rendition.url)
