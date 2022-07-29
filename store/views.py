from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Collection, Product
from .serializers import CollectionSerializer, ProductsSerializer

# Create your views here.


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductsSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductsSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if product.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be delete because order items associates with this"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionCreateList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer


class CollectionRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, id=pk)
        if collection.products.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be delete because many products are associates with this"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
