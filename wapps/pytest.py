import pytest

from urllib.parse import urljoin, urlsplit

from django.conf import settings
from django.http import QueryDict
from django.http.request import split_domain_port, validate_host
from django.middleware import csrf
from django.template import RequestContext, engines
from django.utils.encoding import smart_text
from django.utils.functional import SimpleLazyObject
from django_jinja.base import dict_from_context
from pytest_factoryboy import register, LazyFixture


def pytest_configure(config):
    from wapps import factories
    register(factories.IdentityFactory, 'identity', author=LazyFixture('site'))
    register(factories.ImageFactory, 'image')
    register(factories.ImageFactory)
    register(factories.PageFactory)
    register(factories.RootFactory)
    register(factories.SiteFactory)
    register(factories.UserFactory)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    from wagtail.wagtailcore.models import Page, Site
    with django_db_blocker.unblock():
        # Remove some initial data that is brought by the sandbox module
        Site.objects.all().delete()
        Page.objects.all().exclude(depth=1).delete()


@pytest.fixture
def rf(site):
    from wapps import factories
    return factories.RequestFactory(site=site)


@pytest.fixture
def urf(user, site):
    from wapps import factories
    return factories.RequestFactory(site=site, user=user)


def render_jinja_template(template, **ctx):
    from wapps import factories
    engine = engines['jinja2']
    template = engine.from_string(template)
    request = ctx.get('request', factories.RequestFactory().get('/'))
    context = RequestContext(request, ctx)
    return template.render(context)


def get_jinja_context(**ctx):
    '''Generate a jinja context like django-jinja'''
    from wapps import factories
    engine = engines['jinja2']
    request = ctx.get('request', factories.RequestFactory().get('/'))
    context = dict_from_context(ctx)

    def _get_val():
        token = csrf.get_token(request)
        if token is None:
            return 'NOTPROVIDED'
        else:
            return smart_text(token)

    context["request"] = request
    context["csrf_token"] = SimpleLazyObject(_get_val)

    # Support for django context processors
    for processor in engine.context_processors:
        context.update(processor(request))

    return engine.from_string('').template.new_context(context)


@pytest.fixture
def jinja():
    return render_jinja_template


@pytest.fixture
def jinja_context():
    return get_jinja_context


def error(msg, details, *args, **kwargs):
    return ': '.join((msg, details.format(*args, **kwargs)))


def assert_redirects(response, expected_url, status_code=302,
                     target_status_code=200, fetch_redirect_response=True):
    '''
    Assert that a response redirected to a specific URL and that the
    redirect URL can be loaded.

    Won't work for external links since it uses the test client to do a
    request (use fetch_redirect_response=False to check such links without
    fetching them).
    '''
    __tracebackhide__ = True
    if hasattr(response, 'redirect_chain'):
        # The request was a followed redirect
        assert len(response.redirect_chain) > 0, error(
            'Response didn\'t redirect as expected',
            'Response code was {0} (expected {1})',
            response.status_code, status_code
        )

        assert response.redirect_chain[0][1] == status_code, error(
            'Initial response didn\'t redirect as expected',
            'Response code was {0} (expected {1})',
            response.redirect_chain[0][1], status_code
        )

        url, status_code = response.redirect_chain[-1]
        scheme, netloc, path, query, fragment = urlsplit(url)

        assert response.status_code == target_status_code, error(
            'Response didn\'t redirect as expected',
            'Final Response code was {0} (expected {1})',
            response.status_code, target_status_code
        )

    else:
        # Not a followed redirect
        assert response.status_code == status_code, error(
            'Response didn\'t redirect as expected',
            'Response code was {0} (expected {1})',
            response.status_code, status_code
        )

        url = response.url
        scheme, netloc, path, query, fragment = urlsplit(url)

        # Prepend the request path to handle relative path redirects.
        if not path.startswith('/'):
            url = urljoin(response.request['PATH_INFO'], url)
            path = urljoin(response.request['PATH_INFO'], path)

        if fetch_redirect_response:
            # netloc might be empty, or in cases where Django tests the
            # HTTP scheme, the convention is for netloc to be 'testserver'.
            # Trust both as "internal" URLs here.
            domain, port = split_domain_port(netloc)
            if domain and not validate_host(domain, settings.ALLOWED_HOSTS):
                raise ValueError(
                    "The test client is unable to fetch remote URLs (got %s). "
                    "If the host is served by Django, add '%s' to ALLOWED_HOSTS. "
                    "Otherwise, use assertRedirects(..., fetch_redirect_response=False)."
                    % (url, domain)
                )
            redirect_response = response.client.get(
                path, QueryDict(query), secure=(scheme == 'https'))

            # Get the redirection page, using the same client that was used
            # to obtain the original response.
            assert redirect_response.status_code == target_status_code, error(
                'Couldn\'t retrieve redirection page "{0}"'.format(path),
                'response code was {0} (expected {1})',
                redirect_response.status_code, target_status_code
            )

    assert url == expected_url, 'Response redirected to "{0}", expected "{1}"'.foramt(url, expected_url)
