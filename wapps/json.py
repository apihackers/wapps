import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import force_text
from django.utils.functional import Promise


class WappsEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(WappsEncoder, self).default(obj)


def dumps(*args, **kwargs):
    kwargs['cls'] = WappsEncoder
    return json.dumps(*args, **kwargs)
