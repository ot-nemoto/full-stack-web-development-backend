# Generated by Django 5.2 on 2025-05-09 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SalesFile",
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
                    "file_name",
                    models.CharField(max_length=100, verbose_name="ファイル名"),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "同期"),
                            (1, "非同期_未処理"),
                            (2, "非同期_処理済"),
                        ],
                        verbose_name="状態",
                    ),
                ),
            ],
            options={
                "verbose_name": "売上ファイル",
                "verbose_name_plural": "売上ファイル一覧",
                "db_table": "sales_files",
            },
        ),
        migrations.AddField(
            model_name="sale",
            name="import_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventory.salesfile",
                verbose_name="売上ファイルID",
            ),
        ),
    ]
