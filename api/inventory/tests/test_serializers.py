from datetime import datetime

import pytest

from api.inventory.models import Product
from api.inventory.serializers import (
    InventorySerializer,
    ProductSerializer,
    PurchaseSerializer,
    SaleSerializer,
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "product_data, is_valid",
    [
        ({"name": "Test Product", "price": 1000,
         "description": "A test product"}, True),
        # 無効: nameが空
        ({"name": "", "price": 1000, "description": "A test product"}, False),
        ({"name": "Test Product", "price": -1000,
         "description": "A test product"}, False),  # 無効: priceが負
    ],
)
def test_product_serializer(product_data, is_valid):
    serializer = ProductSerializer(data=product_data)
    assert serializer.is_valid() == is_valid
    if is_valid:
        product = serializer.save()
        assert product.name == product_data["name"]
        assert product.price == product_data["price"]
        assert product.description == product_data["description"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity, is_valid",
    [
        (10, True),
        (-5, False),  # 無効: quantityが負
    ],
)
def test_purchase_serializer(quantity, is_valid):
    product = Product.objects.create(
        name="Test Product", price=1000, description="A test product"
    )
    purchase_data = {
        "product": product.id,
        "quantity": quantity,
        "purchase_date": datetime.now(),
    }
    serializer = PurchaseSerializer(data=purchase_data)
    assert serializer.is_valid() == is_valid
    if is_valid:
        purchase = serializer.save()
        assert purchase.product == product
        assert purchase.quantity == purchase_data["quantity"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity, is_valid",
    [
        (5, True),
        (-3, False),  # 無効: quantityが負
    ],
)
def test_sale_serializer(quantity, is_valid):
    product = Product.objects.create(
        name="Test Product", price=1000, description="A test product"
    )
    sale_data = {
        "product": product.id,
        "quantity": quantity,
        "sales_date": datetime.now(),
    }
    serializer = SaleSerializer(data=sale_data)
    assert serializer.is_valid() == is_valid
    if is_valid:
        sale = serializer.save()
        assert sale.product == product
        assert sale.quantity == sale_data["quantity"]


@pytest.mark.parametrize(
    "inventory_data, is_valid",
    [
        (
            {"id": 1, "unit": 1000, "quantity": 10,
                "type": 1, "date": datetime.now()},
            True,
        ),
        (
            {"id": "invalid", "unit": 1000, "quantity": 10,
                "type": 1, "date": datetime.now()},
            False,  # 無効: idが文字列
        ),
    ],
)
def test_inventory_serializer(inventory_data, is_valid):
    serializer = InventorySerializer(data=inventory_data)
    assert serializer.is_valid() == is_valid
    if is_valid:
        validated_data = serializer.validated_data
        assert validated_data["id"] == inventory_data["id"]
        assert validated_data["unit"] == inventory_data["unit"]
        assert validated_data["quantity"] == inventory_data["quantity"]
        assert validated_data["type"] == inventory_data["type"]
