import pytest
from rest_framework import status
from rest_framework.test import APIClient

from api.inventory.models import Product, Purchase, Sale


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_all_products_no_data(client):
    """
    データが存在しない場合のテスト
    """
    response = client.get('/api/inventory/products/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_all_products_with_data(client):
    """
    データが存在する場合のテスト
    """
    # テスト用データを作成
    Product.objects.create(name="Product 1", price=1000,
                           description="Description 1")
    Product.objects.create(name="Product 2", price=2000,
                           description="Description 2")
    response = client.get('/api/inventory/products/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['name'] == "Product 1"
    assert response.data[1]['name'] == "Product 2"


@pytest.mark.django_db
def test_get_product_by_id(client):
    """
    テスト用データを作成してGETリクエストを送信
    """
    product = Product.objects.create(
        name="Product 1", price=1000, description="Description 1")
    response = client.get(f'/api/inventory/products/{product.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Product 1"
    assert response.data['price'] == 1000


@pytest.mark.django_db
def test_get_product_by_invalid_id(client):
    """
    存在しないIDでのGETリクエスト
    """
    response = client.get('/api/inventory/products/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_product(client):
    """
    テスト用データを作成してPOSTリクエストを送信
    """
    data = {
        "name": "New Product",
        "price": 1500,
        "description": "New Product Description"
    }
    response = client.post(
        '/api/inventory/products/model/', data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.first().name == "New Product"


@pytest.mark.django_db
def test_create_product_with_invalid_data(client):
    """
    無効なデータ(空の名前)でのPOSTリクエスト
    """
    data = {
        "name": "",
        "price": 1500,
        "description": "New Product Description"
    }
    response = client.post(
        '/api/inventory/products/model/', data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_product(client):
    """
    テスト用データを作成してPUTリクエストを送信
    """
    product = Product.objects.create(
        name="Product 1", price=1000, description="Description 1")
    data = {
        "name": "Updated Product",
        "price": 2000,
        "description": "Updated Description"
    }
    response = client.put(
        f'/api/inventory/products/{product.id}/', data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    assert product.name == "Updated Product"
    assert product.price == 2000


@pytest.mark.django_db
def test_update_product_with_invalid_id(client):
    """
    存在しないIDでのPUTリクエスト
    """
    data = {
        "name": "Updated Product",
        "price": 2000,
        "description": "Updated Description"
    }
    response = client.put('/api/inventory/products/999/',
                          data=data, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_product_with_invalid_data(client):
    """
    無効なデータ(負の価格)でのPUTリクエスト
    """
    product = Product.objects.create(
        name="Product 1", price=1000, description="Description 1")
    data = {
        "name": "Updated Product",
        "price": -2000,
        "description": "Updated Description"
    }
    response = client.put(
        f'/api/inventory/products/{product.id}/', data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_product(client):
    """
    テスト用データを作成してDELETEリクエストを送信
    """
    product = Product.objects.create(
        name="Product 1", price=1000, description="Description 1")
    response = client.delete(f'/api/inventory/products/{product.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_delete_product_with_invalid_id(client):
    """
    存在しないIDでのDELETEリクエスト
    """
    response = client.delete('/api/inventory/products/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_purchase(client):
    """
    PurchaseView: 正常なデータでのPOSTリクエスト
    """
    product = Product.objects.create(
        name="Test Product", price=1000, description="Description")
    data = {
        "product": product.id,
        "quantity": 10,
        "purchase_date": "2025-04-21T12:00:00Z"
    }
    response = client.post('/api/inventory/purchases/',
                           data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Purchase.objects.count() == 1
    assert Purchase.objects.first().quantity == 10


@pytest.mark.django_db
def test_create_purchase_with_invalid_data(client):
    """
    PurchaseView: 無効なデータでのPOSTリクエスト
    """
    data = {
        "product": 999,  # 存在しない商品ID
        "quantity": -5,  # 無効な数量
        "purchase_date": "2025-04-21T12:00:00Z"
    }
    response = client.post('/api/inventory/purchases/',
                           data=data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_sale(client):
    """
    SaleView: 正常なデータでのPOSTリクエスト
    """
    product = Product.objects.create(
        name="Test Product", price=1000, description="Description")
    Purchase.objects.create(product=product, quantity=20,
                            purchase_date="2025-04-20T12:00:00Z")
    data = {
        "product": product.id,
        "quantity": 5,
        "sales_date": "2025-04-21T12:00:00Z"
    }
    response = client.post('/api/inventory/sales/', data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Sale.objects.count() == 1
    assert Sale.objects.first().quantity == 5


@pytest.mark.django_db
def test_create_sale_with_insufficient_stock(client):
    """
    SaleView: 在庫不足でのPOSTリクエスト
    """
    product = Product.objects.create(
        name="Test Product", price=1000, description="Description")
    Purchase.objects.create(product=product, quantity=5,
                            purchase_date="2025-04-20T12:00:00Z")
    data = {
        "product": product.id,
        "quantity": 10,  # 在庫を超える数量
        "sales_date": "2025-04-21T12:00:00Z"
    }
    response = client.post('/api/inventory/sales/', data=data, format='json')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.django_db
def test_get_inventory(client):
    """
    InventoryView: 正常なデータでのGETリクエスト
    """
    product = Product.objects.create(
        name="Test Product", price=1000, description="Description")
    Purchase.objects.create(product=product, quantity=10,
                            purchase_date="2025-04-20T12:00:00Z")
    Sale.objects.create(product=product, quantity=5,
                        sale_date="2025-04-21T12:00:00Z")
    response = client.get(f'/api/inventory/inventories/{product.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_inventory_with_invalid_id(client):
    """
    InventoryView: 存在しないIDでのGETリクエスト
    """
    response = client.get('/api/inventory/inventories/999/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
