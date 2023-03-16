import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_add_url_as_user(client):
    url = reverse('add')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_url_as_superuser(admin_client):
    url = reverse('add')
    response = admin_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_homepage_url(admin_client):
    url = reverse('home')
    response = admin_client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == 'clothes/index.html'
