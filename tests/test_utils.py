from wapps import utils


def test_timehash_default():
    assert len(utils.timehash()) == 10


def test_timehash_custom_length():
    assert len(utils.timehash(20)) == 20


def test_timehash_different():
    first = utils.timehash()
    second = utils.timehash()
    assert first != second


class SettingProxyTest:
    def test_undefined_setting(self, settings, faker):
        proxy = utils.SettingProxy('UNDEFINED')
        assert bool(proxy) is False
        assert proxy == None  # noqa

    def test_none_setting(self, settings, faker):
        settings.VALUE = None
        proxy = utils.SettingProxy('VALUE')
        assert bool(proxy) is False
        assert proxy == None  # noqa

    def test_string_setting(self, settings, faker):
        settings.VALUE = faker.word()
        proxy = utils.SettingProxy('VALUE')
        assert str(proxy) == settings.VALUE
        assert bool(proxy) is True

    def test_empty_string_setting(self, settings, faker):
        settings.VALUE = ''
        proxy = utils.SettingProxy('VALUE')
        assert str(proxy) == ''
        assert bool(proxy) is False

    def test_bool_setting(self, settings, faker):
        settings.VALUE = True
        proxy = utils.SettingProxy('VALUE')
        assert proxy == True  # noqa

        settings.VALUE = False
        proxy = utils.SettingProxy('VALUE')
        assert proxy == False  # noqa
