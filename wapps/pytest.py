import pytest

from urllib.parse import urljoin, urlsplit

from django.conf import settings
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.http.request import split_domain_port, validate_host
from django.middleware import csrf
from django.template import RequestContext, engines
from django.utils.encoding import smart_text
from django.utils.functional import SimpleLazyObject
from django.utils.text import slugify
from django_jinja.base import dict_from_context
from pytest_factoryboy import register, LazyFixture


def pytest_configure(config):
    from wapps import factories
    register(factories.CategoryFactory)
    register(factories.FullIdentityFactory, 'full_identity', site=LazyFixture('site'))
    register(factories.IdentityFactory, 'identity', site=LazyFixture('site'))
    register(factories.ImageFactory)
    register(factories.ImageFactory, 'image')
    register(factories.PageFactory)
    register(factories.SiteFactory)
    register(factories.UserFactory)
    register(factories.TagFactory)


@pytest.fixture(autouse=True)
def _wagtail_cleanup(request, django_db_blocker, _django_db_marker):
    '''Cleanup wagtail initial data if db is in use'''
    marker = request.keywords.get('django_db', None)
    if marker:
        from wagtail.wagtailcore.models import Page, Site
        with django_db_blocker.unblock():
            # Remove some initial data that is brought by the sandbox module
            if not request.node.get_marker('no_wagtail_cleanup'):
                Site.objects.all().delete()
                Page.objects.all().delete()
            marker = request.node.get_marker('load_db_fixture')
            if marker:
                call_command('loaddata', marker.args[0])


@pytest.fixture
def wrf(site):
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


def _error(msg, *args, **kwargs):
    '''A simple wrapper to str.format allowing cleaner line wrapping'''
    return msg.format(*args, **kwargs)


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
        assert len(response.redirect_chain) > 0, _error(
            'Response didn\'t redirect as expected: '
            'Response code was {0} (expected {1})',
            response.status_code, status_code
        )

        assert response.redirect_chain[0][1] == status_code, _error(
            'Initial response didn\'t redirect as expected: '
            'Response code was {0} (expected {1})',
            response.redirect_chain[0][1], status_code
        )

        url, status_code = response.redirect_chain[-1]
        scheme, netloc, path, query, fragment = urlsplit(url)

        assert response.status_code == target_status_code, _error(
            'Response didn\'t redirect as expected: '
            'Final Response code was {0} (expected {1})',
            response.status_code, target_status_code
        )

    else:
        # Not a followed redirect
        assert response.status_code == status_code, _error(
            'Response didn\'t redirect as expected: '
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
                    'The test client is unable to fetch remote URLs (got {0}). '
                    'If the host is served by Django, add "{1}" to ALLOWED_HOSTS. '
                    'Otherwise, use assertRedirects(..., fetch_redirect_response=False).'
                    ''.format(url, domain)
                )
            redirect_response = response.client.get(path, QueryDict(query), secure=(scheme == 'https'))

            # Get the redirection page, using the same client that was used
            # to obtain the original response.
            assert redirect_response.status_code == target_status_code, _error(
                'Couldn\'t retrieve redirection page "{0}": '
                'response code was {1} (expected {2})',
                path, redirect_response.status_code, target_status_code
            )

    assert url == expected_url, 'Response redirected to "{0}", expected "{1}"'.foramt(url, expected_url)


def _can_create_at(parent_model, child_model):
    __tracebackhide__ = True
    return child_model in parent_model.allowed_subpage_models()


def assert_can_create_at(parent_model, child_model):
    '''
    Assert a particular child Page type can be created under a parent
    Page type. ``parent_model`` and ``child_model`` should be the Page
    classes being tested.
    '''
    __tracebackhide__ = True
    assert _can_create_at(parent_model, child_model), _error(
        'Can not create a {child.app_label}.{child.model_name} under a {parent.app_label}.{parent.model_name}',
        child=child_model._meta,
        parent=parent_model._meta
    )


def assert_can_not_create_at(parent_model, child_model):
    '''
    Assert a particular child Page type can not be created under a parent
    Page type. ``parent_model`` and ``child_model`` should be the Page
    classes being tested.
    '''
    __tracebackhide__ = True
    assert not _can_create_at(parent_model, child_model), _error(
        'Can create a {child.app_label}.{child.model_name} under a {parent.app_label}.{parent.model_name}',
        child=child_model._meta,
        parent=parent_model._meta
    )


def assert_can_create(parent, child_model, data, client):
    '''
    Assert that a child of the given Page type can be created under the
    parent, using the supplied POST data.
    ``parent`` should be a Page instance, and ``child_model`` should be a
    Page subclass. ``data`` should be a dict that will be POSTed at the
    Wagtail admin Page creation method.
    '''
    __tracebackhide__ = True
    assert_can_create_at(parent.specific_class, child_model)

    if 'slug' not in data and 'title' in data:
        data['slug'] = slugify(data['title'])
    data['action-publish'] = 'action-publish'

    add_url = reverse('wagtailadmin_pages:add', args=[
        child_model._meta.app_label, child_model._meta.model_name, parent.pk])
    response = client.post(add_url, data, follow=True)

    assert response.status_code != 200, _error(
        'Creating a {model.app_label}.{model.model_name} returned a {status}',
        model=child_model._meta, status=response.status_code
    )

    if response.redirect_chain == []:
        assert 'form' in response.context, 'Creating a page failed unusually'
        form = response.context['form']
        assert form.errors, 'Creating a page failed for an unknown reason'

        pytest.fail(_error(
            'Validation errors found when creating a {model.app_label}.{model.model_name}: \n{details}',
            details='\n'.join('\t{0}: {1}'.format(field_errors) for field_errors in sorted(form.errors.items())),
            model=child_model._meta
        ))

    explore_url = reverse('wagtailadmin_explore', args=[parent.pk])
    assert response.redirect_chain != [(explore_url, 302)], _error(
        'Creating a page {model.app_label}.{model.model_name} didnt redirect the user to the explorer, but to {chain}',
        model=child_model._meta,
        chain=response.redirect_chain
    )


def assert_allowed_subpage_types(parent_model, child_models):
    '''
    Test that the only page types that can be created under
    ``parent_model`` are ``child_models``.
    The list of allowed child models may differ from those set in
    ``Page.subpage_types``, if the child models have set
    ``Page.parent_page_types``.
    '''
    __tracebackhide__ = True
    assert set(parent_model.allowed_subpage_models()) == set(child_models)


def assert_allowed_parent_types(child_model, parent_models):
    '''
    Test that the only page types that ``child_model`` can be created under
    are ``parent_models``.
    The list of allowed parent models may differ from those set in
    ``Page.parent_page_types``, if the parent models have set
    ``Page.subpage_types``.
    '''
    __tracebackhide__ = True
    assert set(child_model.allowed_parent_page_models()) == set(parent_models)
