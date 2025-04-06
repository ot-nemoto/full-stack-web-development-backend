from rest_framework.response import Response
from rest_framework.views import APIView


class ProductView(APIView):
    def get(self, request, format=None):
        return Response({"message": "products"})
