import pytest

from wapps import social

expected_user_urls = [
    ('twitter', 'https://twitter.com/apihackers'),
    ('linkedin', 'https://www.linkedin.com/in/apihackers'),
    ('facebook', 'https://facebook.com/n/?apihackers'),
    ('instagram', 'https://instagram.com/_u/apihackers'),
    ('pinterest', 'https://pinterest.com/apihackers'),
    ('youtube', 'https://www.youtube.com/user/apihackers'),
]

expected_icons = [
    ('twitter', 'fa-twitter'),
    ('linkedin', 'fa-linkedin'),
    ('facebook', 'fa-facebook'),
    ('instagram', 'fa-instagram'),
    ('pinterest', 'fa-pinterest'),
    ('reddit', 'fa-reddit'),
    ('email', 'fa-envelope'),
    ('youtube', 'fa-youtube'),
]

expected_share_urls = [
    ('twitter', 'https://twitter.com/share?url=https%3A%2F%2Fsomewhere.com&text=My+title'),
    ('linkedin', 'https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fsomewhere.com&title=My+title'),
    ('facebook', 'https://www.facebook.com/sharer.php?u=https%3A%2F%2Fsomewhere.com'),
    ('google', 'https://plus.google.com/share?url=https%3A%2F%2Fsomewhere.com'),
    ('reddit', 'https://reddit.com/submit?url=https%3A%2F%2Fsomewhere.com&title=My+title'),
    ('email', 'mailto:?subject=My+title&body=https%3A%2F%2Fsomewhere.com'),
]


@pytest.mark.parametrize('network,expected', expected_user_urls)
def test_user_url_from_username(network, expected):
    assert social.user_url(network, 'apihackers') == expected


@pytest.mark.parametrize('network,expected', expected_user_urls)
def test_user_url_from_url(network, expected):
    assert social.user_url(network, expected) == expected


@pytest.mark.parametrize('network,expected', expected_user_urls)
def test_user_url_from_http_url(network, expected):
    http_url = expected.replace('https:', 'http:')
    assert social.user_url(network, http_url) == expected


@pytest.mark.parametrize('network,expected', expected_icons)
def test_network_icons(network, expected):
    assert social.icon(network) == expected


@pytest.mark.parametrize('network,expected', expected_share_urls)
def test_share_urls(network, expected):
    assert social.share_url(network, 'https://somewhere.com', 'My title') == expected


@pytest.mark.parametrize('network,expected', expected_share_urls)
def test_no_share_urls(network, expected):
    assert social.share_url('youtube', 'https://somewhere.com', 'My title') is None


def test_network_not_found():
    with pytest.raises(ValueError):
        social.network('unknown')
