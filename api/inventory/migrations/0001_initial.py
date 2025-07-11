# Generated by Django 5.2 on 2025-05-08 22:52

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="商品名")),
                (
                    "price",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="価格",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="商品説明"),
                ),
            ],
            options={
                "verbose_name": "商品",
                "verbose_name_plural": "商品一覧",
                "db_table": "products",
            },
        ),
        migrations.CreateModel(
            name="Purchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="数量",
                    ),
                ),
                (
                    "purchase_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="仕入日時"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "仕入",
                "verbose_name_plural": "仕入一覧",
                "db_table": "purchases",
            },
        ),
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="数量",
                    ),
                ),
                (
                    "sale_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="売上日時"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "売上",
                "verbose_name_plural": "売上一覧",
                "db_table": "sales",
            },
        ),
    ]
