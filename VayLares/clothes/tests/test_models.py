import pytest

from clothes.models import User


@pytest.mark.django_db
def test_user_create(client):
    user1 = User.objects.create_user(username='test', email='test@mail.com',
                                     password='testasd123Asd', gender='Женский')
    assert User.objects.count() == 1
    assert user1.gender == 'Женский'
    assert not user1.image


@pytest.mark.djago_db
def test_clothes_create(clothes_factory):
    clothes = clothes_factory.build()
    assert clothes.gender == 'All'
    assert clothes.category.category_name == 'test_category'
