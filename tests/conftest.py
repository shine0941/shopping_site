import pytest
from rest_framework.test import APIClient
from users.models import User, Customer, AdminUser


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def customer_user(db):
    return User.objects.create_user(email='test_customer@site.com', password='testpass')

@pytest.fixture
def customer_client(customer_user):
    client = APIClient()
    client.force_authenticate(user=customer_user)
    return client

# @pytest.fixture
# def tag(db):
#     return Tag.objects.create(name='Django')

# @pytest.fixture
# def article(user, category):
#     article = Article.objects.create(
#         title='Test Article',
#         content='Some content',
#         category=category,
#         author=user
#     )
#     return article

@pytest.fixture
def merchant_user(db):
    user = User.objects.create_user(email='test_merchant@site.com', password='pass123')
    # AdminUser.objects.create(user=user, role='merchant')
    return user

@pytest.fixture
def merchant(merchant_user):
    return AdminUser.objects.create(user=merchant_user, role='merchant')

@pytest.fixture
def merchant_client(merchant_user):
    client = APIClient()
    client.force_authenticate(user=merchant_user)
    return client
