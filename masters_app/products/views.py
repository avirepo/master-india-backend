from django.shortcuts import get_object_or_404
from rest_framework import generics, views

# Create your views here.
from products.models import Category, Product, SubCategory
from products.serializers import CategorySerializer, ProductsSerializer, SubCategorySerializer


class OrderByMixing:
    def order_by(self):
        order_by = None
        if isinstance(self, views.APIView):
            order_by = self.request.query_params.get('order_by')
            order = self.request.query_params.get('order', 'ASC')
            if order_by:
                order_by = order == 'ASC' and order_by or f'-{order_by}'
        if not order_by:
            order_by = 'id'
        return order_by


class CategoryList(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        return Category.objects.all()


class SubCategoryList(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SubCategorySerializer

    def get_queryset(self, *args, **kwargs):
        category = get_object_or_404(Category.objects, id=self.kwargs.get('category_id'))
        return SubCategory.objects.filter(category=category)


class ProductListCreate(generics.ListCreateAPIView, OrderByMixing):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductsSerializer

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all().order_by(self.order_by())
