import pytest
from products.models import ProductCategory, Product

@pytest.fixture
def test_category(db):
    return ProductCategory.objects.create(name='Test')

@pytest.fixture
def test_product(merchant, test_category):
    return Product.objects.create(
        merchant_id=merchant.id,
        name="Test Product 01",
        description="Test Product Description 01",
        price=100,
        category_id=test_category.id,
        inventory=50
    )

@pytest.mark.django_db
def test_product_create(merchant, merchant_client, test_category):
    payload = {
        "merchant_id": merchant.id,
        "name": "Test Product 02",
        "description": "Test Product Description 02",
        "price":100,
        "category_id": test_category.id,
        "inventory":50
    }
    response = merchant_client.post(f"/products/products/", payload)
    assert response.status_code == 201
    
@pytest.mark.django_db
def test_product_list(customer_client):
    response = customer_client.get(f"/products/products/")

    assert response.status_code == 200

# @pytest.mark.django_db
# def test_add_product_into_cart(customer_client,test_product):
#     payload = {
#         "quantity": 1,
#         "product": test_product.id,
#     }
#     response = customer_client.post(f"/cart/cart-items/", payload)

#     assert response.status_code == 200
