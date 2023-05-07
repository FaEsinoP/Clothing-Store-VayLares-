import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_homepage_view(client):
    url = reverse('home')
    response = client.get(url)
    assert response.context_data['gender_selected'] is None


@pytest.mark.django_db
def test_forman_view(client):
    url = reverse('man')
    response = client.get(url)
    assert response.context_data['gender_selected'] == 'Для мужчин'


@pytest.mark.django_db
def test_forwoman_view(client):
    url = reverse('woman')
    response = client.get(url)
    assert response.context_data['gender_selected'] == 'Для женщин'
