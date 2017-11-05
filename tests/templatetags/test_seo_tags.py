import pytest

from wapps.metadata import Metadata


@pytest.mark.django_db
def test_page_meta(jinja_context, settings, faker):
    ctx = jinja_context()
    assert 'page_meta' in ctx
    assert isinstance(ctx['page_meta'](ctx), Metadata)
