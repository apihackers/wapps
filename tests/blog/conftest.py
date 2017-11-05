from pytest_factoryboy import register
from wapps.blog import factories

register(factories.BlogFactory)
register(factories.BlogPostFactory)
