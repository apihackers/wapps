import pytest

import re


@pytest.mark.django_db
def test_timehash(jinja):
    rendered = jinja('{{ timehash() }}')
    assert len(rendered) == 10


@pytest.mark.django_db
def test_timehashcustom_length(jinja):
    rendered = jinja('{{ timehash(12) }}')
    assert len(rendered) == 12


@pytest.mark.django_db
def test_now(jinja):
    rendered = jinja('{{ now().isoformat() }}')
    assert re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}\+\d{2}\:\d{2}$', rendered)


@pytest.mark.django_db
def test_json(jinja):
    rendered = jinja('{{ True|json }}')
    assert rendered == 'true'
