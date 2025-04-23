import pytest
from django.urls import reverse
from django.test import Client

# Test basic page loading
@pytest.mark.django_db
def test_home_page(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200

# Test authenticated user access
@pytest.mark.django_db
def test_authenticated_access(client, create_user):
    client.force_login(create_user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'user' in response.context
    assert response.context['user'].is_authenticated
