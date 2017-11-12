from django.utils.translation import ugettext_lazy as _

from wapps import json


def test_serialize_lazy_strings():
    assert json.dumps(_('test')) == '"test"'
