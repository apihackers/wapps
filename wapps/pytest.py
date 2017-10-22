import pytest

from pytest_factoryboy import register, LazyFixture

from django_jinja.base import dict_from_context

from django.template import RequestContext, engines
from django.middleware import csrf
from django.utils.encoding import smart_text
from django.utils.functional import SimpleLazyObject


def pytest_configure(config):
    from wapps import factories
    register(factories.IdentityFactory, 'identity', author=LazyFixture('site'))
    register(factories.ImageFactory, 'image')
    register(factories.ImageFactory)
    register(factories.PageFactory)
    register(factories.RootFactory)
    register(factories.SiteFactory)
    register(factories.UserFactory)


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
