import pandas as pd
from django.db import transaction
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .exceptions import BusinessException
from .models import Product, Purchase, Sale, SalesFile, Status
from .serializers import (
    FileSerializer,
    InventorySerializer,
    ProductSerializer,
    PurchaseSerializer,
    SaleSerializer,
)


class ProductView(APIView):

    def get_object(self, pk):
        """
        指定されたIDの商品の情報を取得する
        """
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound

    def get(self, request, id=None, format=None):
        """
        商品情報を取得する
        """
        if id is None:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        商品情報を登録する
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def put(self, request, id, format=None):
        """
        商品情報を更新する
        """
        product = self.get_object(id)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        """
        商品情報を削除する
        """
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_200_OK)


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PurchaseView(APIView):
    def post(self, request, format=None):
        """
        仕入情報を登録する
        """
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class SaleView(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        """
        売上情報を登録する
        """
        serializer = SaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        purchase = Purchase.objects.filter(product_id=request.data['product']).aggregate(
            quantity_sum=Coalesce(Sum('quantity'), 0))
        sales = Sale.objects.filter(product_id=request.data['product']).aggregate(
            quantity_sum=Coalesce(Sum('quantity'), 0))

        if purchase['quantity_sum'] < (sales['quantity_sum'] + int(request.data['quantity'])):
            raise BusinessException('在庫数量を超過することはできません')

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class InventoryView(APIView):
    # 仕入れ・売上情報を取得する
    def get(self, request, id=None, format=None):
        if id is None:
            return Response({}, status.HTTP_400_BAD_REQUEST)

        purchases = Purchase.objects.filter(product_id=id).prefetch_related('product').values(
            "id", "quantity", type=Value('1'), date=F('purchase_date'), unit=F('product__price'))
        sales = Sale.objects.filter(product_id=id).prefetch_related('product').values(
            "id", "quantity", type=Value('2'), date=F('sale_date'), unit=F('product__price'))
        queryset = purchases.union(sales).order_by(F("date"))
        serializer = InventorySerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class SalesSyncView(APIView):

    parser_classes = [MultiPartParser]

    @transaction.atomic
    @swagger_auto_schema(
        operation_description="売上ファイルをアップロードして処理します",
        manual_parameters=[
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="アップロードするCSVファイル",
                type=openapi.TYPE_FILE,
                required=True,
            ),
        ],
        responses={
            201: "ファイルが正常に処理されました",
        },
    )
    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data['file'].name

        with open(filename, 'wb') as f:
            f.write(serializer.validated_data['file'].read())

        sales_file = SalesFile(file_name=filename, status=Status.SYNC)
        sales_file.save()

        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            sales = Sale(
                product_id=row['product'], sale_date=row['date'], quantity=row['quantity'], import_file=sales_file)
            sales.save()

        return Response(status=201)
