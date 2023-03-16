import uuid

import pytest
from pytest_factoryboy import register

from clothes.tests.factories import *

register(CategoryFactory)
register(SubcategoryFactory)
register(SizesFactory)
register(BrandFactory)
register(ClothesFactory)
register(Sizes_of_ClothesFactory)
register(ClothesWithSizeFactory)


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        kwargs['password'] = 'strong_test_password'
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def logged_in_client(client, my_user):
    return client.force_login(my_user)
