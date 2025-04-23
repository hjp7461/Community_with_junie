import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
    }

@pytest.fixture
def create_user(user_data):
    User = get_user_model()
    return User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password']
    )