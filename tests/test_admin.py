import pytest

from django.urls import reverse

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures('site'),
]


@pytest.mark.parametrize('user__is_superuser', [True])
def test_insert_js_in_admin(client, page, user):
    client.force_login(user)

    response = client.get(reverse('wagtailadmin_pages:edit', args=(page.id,)))

    assert response.status_code == 200

    html = response.content.decode('utf8')

    assert 'wapps/hallo-counter.js' in html
    assert 'wapps/colorful.css' in html
