from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now


class Product(models.Model):
    """
    商品
    """
    name = models.CharField(max_length=100, verbose_name='商品名')
    price = models.IntegerField(
        verbose_name='価格', validators=[MinValueValidator(0)])
    description = models.TextField(verbose_name='商品説明', null=True, blank=True)

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品一覧'


class Purchase(models.Model):
    """
    仕入
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name='数量', validators=[MinValueValidator(0)])
    purchase_date = models.DateTimeField(verbose_name='仕入日時', default=now)

    class Meta:
        db_table = 'purchases'
        verbose_name = '仕入'
        verbose_name_plural = '仕入一覧'


class Sale(models.Model):
    """
    売上
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name='数量', validators=[MinValueValidator(0)])
    sale_date = models.DateTimeField(verbose_name='売上日時', default=now)

    class Meta:
        db_table = 'sales'
        verbose_name = '売上'
        verbose_name_plural = '売上一覧'
