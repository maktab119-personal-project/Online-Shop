from django.shortcuts import render , get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.generics import GenericAPIView , ListAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework import status
from .models import Product , Category
from .serializers import ProductSerializer , CategorySerializer

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .models import Product
from .serializers import ProductSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ProductListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, is_delete=False)

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(brand_name__icontains=search)
            )

        max_price = self.request.GET.get('max_price')
        if max_price and max_price.isdigit():
            queryset = queryset.filter(price__lte=int(max_price))

        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))

        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class ProductRetrieveUpdateDeleteView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Product.objects.filter(is_active=True, is_delete=False)
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.make_delete()  # استفاده از LogicalMixin برای حذف منطقی
        return Response({"message": "Product deleted logically."}, status=status.HTTP_204_NO_CONTENT)


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(is_active=True, is_delete=False)
    serializer_class = CategorySerializer
