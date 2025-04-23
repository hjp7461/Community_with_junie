import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

# Test user model
def test_create_user(user_data):
    User = get_user_model()
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password']
    )
    assert user.username == user_data['username']
    assert user.email == user_data['email']
    assert user.check_password(user_data['password'])

# Test user authentication
@pytest.mark.django_db
def test_user_authentication(client, create_user, user_data):
    # Test login
    login_successful = client.login(
        username=user_data['username'],
        password=user_data['password']
    )
    assert login_successful is True
