from django.shortcuts import redirect, get_object_or_404


from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.shortcuts import get_rendition_or_not_found


def image(request, pk, specs):
    '''
    Request an image given some specs and redirects to it
    '''
    image = get_object_or_404(get_image_model(), pk=pk)
    rendition = get_rendition_or_not_found(image, specs)
    return redirect(rendition.url)
