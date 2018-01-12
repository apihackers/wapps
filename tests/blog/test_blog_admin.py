import pytest

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures('site'),
]


@pytest.mark.parametrize('user__is_superuser', [True])
def test_render_blog_post_model_admin(client, user, blog, blog_post_factory):

    posts = blog_post_factory.create_batch(3, full=True, tags=2, categories=2)
    client.force_login(user)

    response = client.get('/admin/blog/blogpost/')

    assert response.status_code == 200

    assert response.context['all_count'] == len(posts)
