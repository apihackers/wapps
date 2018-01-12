import pytest

import feedparser

from wapps.feed import ExtendedAtomFeed


@pytest.mark.django_db
def test_minimal_site_feed(client, site, identity):
    response = client.get('/atom/')

    assert response.status_code == 200
    assert response['Content-Type'].split(';', 1)[0] == 'application/atom+xml'

    d = feedparser.parse(response.content)
    for prefix, url in ExtendedAtomFeed.namespaces.items():
        assert prefix in d.namespaces
        assert d.namespaces[prefix] == url
    assert d.feed.title == identity.name
    assert len(d.entries) == 0
    assert d.feed.webfeeds_accentcolor == {'image': identity.bg_color}
    assert 'webfeeds_cover' not in d.feed
    assert 'webfeeds_logo' not in d.feed
    assert 'webfeeds_icon' not in d.feed


@pytest.mark.django_db
def test_full_site_feed(client, site, full_identity, page_factory, settings, faker):
    settings.GOOGLE_ANALYTICS_ID = faker.sentence()
    pages = page_factory.create_batch(3, parent=site.root_page, published=True)
    response = client.get('/atom/')

    assert response.status_code == 200
    assert response['Content-Type'].split(';', 1)[0] == 'application/atom+xml'

    d = feedparser.parse(response.content)
    assert d.feed.title == full_identity.name
    assert len(d.entries) == len(pages)
    assert d.feed.webfeeds_analytics == {
        'id': settings.GOOGLE_ANALYTICS_ID,
        'engine': 'GoogleAnalytics',
    }
    assert 'webfeeds_cover' in d.feed
    assert 'webfeeds_logo' in d.feed
    assert 'webfeeds_icon' in d.feed
