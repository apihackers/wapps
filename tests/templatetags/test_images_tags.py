import pytest

from wapps.templatetags.images import DEFAULT_BACKGROUND, DEFAULT_FOREGROUND, PLACEHOLDIT_URL


@pytest.mark.django_db
def test_placeholder_url_provivded(jinja, faker):
    url = faker.url()
    rendered = jinja('{{ url|placeholder(300, 400) }}', url=url)
    assert rendered == url


@pytest.mark.django_db
def test_placeholder_text_from_text(rf, jinja, faker):
    text = faker.sentence()
    rendered = jinja('{{ url|placeholder(300, 400, text=text) }}', url=None, text=text)
    assert rendered == PLACEHOLDIT_URL.format(width=300, height=400,
                                              fg=DEFAULT_FOREGROUND.replace('#', ''),
                                              bg=DEFAULT_BACKGROUND.replace('#', ''),
                                              text=text.replace(' ', '+'))


@pytest.mark.django_db
def test_placeholder_text_from_identity(rf, jinja, identity):
    rendered = jinja('{{ url|placeholder(300, 400) }}', url=None, request=rf.get('/'))
    assert rendered == PLACEHOLDIT_URL.format(width=300, height=400,
                                              fg=DEFAULT_FOREGROUND.replace('#', ''),
                                              bg=DEFAULT_BACKGROUND.replace('#', ''),
                                              text=identity.name.replace(' ', '+'))


@pytest.mark.django_db
def test_placeholder_text_from_site(rf, jinja, site):
    rendered = jinja('{{ url|placeholder(300, 400) }}', url=None, request=rf.get('/'))
    assert rendered == PLACEHOLDIT_URL.format(width=300, height=400,
                                              fg=DEFAULT_FOREGROUND.replace('#', ''),
                                              bg=DEFAULT_BACKGROUND.replace('#', ''),
                                              text=site.site_name.replace(' ', '+'))


@pytest.mark.django_db
def test_placeholder_text_from_size(rf, jinja):
    request = rf.get('/')
    request.site = None
    rendered = jinja('{{ url|placeholder(300, 400) }}', url=None, request=request)
    assert rendered == PLACEHOLDIT_URL.format(width=300, height=400,
                                              fg=DEFAULT_FOREGROUND.replace('#', ''),
                                              bg=DEFAULT_BACKGROUND.replace('#', ''),
                                              text='300x400')
