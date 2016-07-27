from django.utils.functional import lazy
from django.utils.safestring import mark_safe

mark_safe_lazy = lazy(mark_safe, str)
