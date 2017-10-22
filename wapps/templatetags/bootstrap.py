# from django.utils.safestring import mark_safe
from django_jinja import library


@library.filter
@library.global_function
def bootstrap_center_grid_offsets(nb, sizes):
    # offsets = []
    for res, size in sizes.items():
        pass
