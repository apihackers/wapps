import pytest


@pytest.mark.django_db
def test_http_response_error_middleware(client):
    response = client.get('/error/')
    assert response.content == b'42'
    assert response.status_code == 442


@pytest.mark.django_db
def test_first_visit_middleware(client):
    # First visit
    assert client.get('/first-visit/').content == b'True'
    assert client.session['visited'] is True
    # Second visit
    assert client.get('/first-visit/').content == b'False'
    assert client.session['visited'] is True


@pytest.mark.django_db
def test_first_visit_middleware_when_authenticated(client, user):
    client.force_login(user)
    # First visit
    assert client.get('/first-visit/').content == b'False'
