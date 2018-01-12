import pytest

from wapps.pytest import assert_redirects


@pytest.mark.django_db
def test_image_view(image, client):
    response = client.get('/images/{pk}/original'.format(pk=image.pk))
    assert_redirects(response, image.get_rendition('original').url, fetch_redirect_response=False)


@pytest.mark.django_db
def test_image_view_image_not_found(client):
    response = client.get('/images/123/original')
    assert response.status_code == 404
