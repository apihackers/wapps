import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = 'secret1234'

    class Meta:
        model = get_user_model()

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._create(target_class, *args, **kwargs)

        if password:
            user.set_password(password)
            user.clear_password = password
            user.save()
        return user
