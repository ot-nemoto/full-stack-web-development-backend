import pytest
from django.core.exceptions import ValidationError

from api.inventory.models import Product, Purchase, Sale


@pytest.mark.django_db
@pytest.mark.parametrize(
    "name, price, description, is_valid",
    [
        ("Test Product", 1000, "A test product", True),  # 正常ケース
        ("", 1000, "A test product", False),  # 無効: nameが空
        ("Test Product", -100, "A test product", False),  # 無効: priceが負
    ],
)
def test_product_model(name, price, description, is_valid):
    product = Product(name=name, price=price, description=description)
    if is_valid:
        product.full_clean()  # バリデーションを手動で呼び出す
        product.save()
        assert product.name == name
        assert product.price == price
        assert product.description == description
    else:
        with pytest.raises(ValidationError):
            product.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity, is_valid",
    [
        (10, True),  # 正常ケース
        (-5, False),  # 無効: quantityが負
    ],
)
def test_purchase_model(quantity, is_valid):
    product = Product.objects.create(
        name="Test Product",
        price=1000,
        description="A test product"
    )
    purchase = Purchase(product=product, quantity=quantity)
    if is_valid:
        purchase.full_clean()  # バリデーションを手動で呼び出す
        purchase.save()
        assert purchase.product == product
        assert purchase.quantity == quantity
    else:
        with pytest.raises(ValidationError):
            purchase.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "quantity, is_valid",
    [
        (5, True),  # 正常ケース
        (-3, False),  # 無効: quantityが負
    ],
)
def test_sale_model(quantity, is_valid):
    product = Product.objects.create(
        name="Test Product",
        price=1000,
        description="A test product"
    )
    sale = Sale(product=product, quantity=quantity)
    if is_valid:
        sale.full_clean()  # バリデーションを手動で呼び出す
        sale.save()
        assert sale.product == product
        assert sale.quantity == quantity
    else:
        with pytest.raises(ValidationError):
            sale.full_clean()
