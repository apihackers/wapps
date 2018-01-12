import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    is_superuser = False

    class Meta:
        model = get_user_model()
