from wapps import utils


def test_timehash_default():
    assert len(utils.timehash()) == 10


def test_timehash_custom_length():
    assert len(utils.timehash(20)) == 20


def test_timehash_different():
    first = utils.timehash()
    second = utils.timehash()
    assert first != second
