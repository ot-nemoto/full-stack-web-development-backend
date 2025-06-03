import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from api.inventory.models import Sale, SalesFile, Status


@transaction.atomic
def execute(download_history):
    entry = SalesFile.objects.select_for_update().get(pk=download_history.id)
    if entry.status != Status.ASYNC_UNPROCESSED:
        return

    filename = entry.file_name

    df = pd.read_csv(filename)
    sales_instances = [
        Sale(product_id=row['product'], sale_date=row['date'],
             quantity=row['quantity'], import_file=entry)
        for _, row in df.iterrows()
    ]
    Sale.objects.bulk_create(sales_instances)

    entry.status = Status.ASYNC_PROCESSED
    entry.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            download_history = SalesFile.objects.filter(
                status=Status.ASYNC_UNPROCESSED).order_by('id').first()
            if download_history is None:
                # 実行中に未処理以外になった場合はスキップ
                break
            else:
                execute(download_history)
