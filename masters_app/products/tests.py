from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from products.common.utils import build_url
from products.models import Category, Product, SubCategory
from products.serializers import CategorySerializer, ProductsSerializer, SubCategorySerializer

APPLICATION_JSON_CONTENT_TYPE = 'application/json; charset=utf-8'


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.category_1 = Category.objects.create(name='Test Category 1')
        self.sub_category_1_category_1 = SubCategory.objects.create(
            name='Test SC1 C1', category=self.category_1
        )
        self.sub_category_2_category_1 = SubCategory.objects.create(
            name='Test SC2 C1', category=self.category_1
        )

        self.category_2 = Category.objects.create(name='Test Category 2')
        self.sub_category_1_category_2 = SubCategory.objects.create(
            name='Test SC1 C2', category=self.category_2
        )
        self.sub_category_2_category_1 = SubCategory.objects.create(
            name='Test SC2 C2', category=self.category_2
        )

        self.category_3 = Category.objects.create(name='Test Category 3')
        self.sub_category_1_category_2 = SubCategory.objects.create(
            name='Test SC1 C3', category=self.category_3
        )
        self.sub_category_2_category_1 = SubCategory.objects.create(
            name='Test SC2 C3', category=self.category_3
        )


class ListCategoryTestCase(BaseTestCase):

    def test_category(self):
        response = self.client.get(reverse('v1:categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CategorySerializer(Category.objects.all(), many=True).data, response.data)


class ListSubCategoryTestCase(BaseTestCase):

    def test_for_invalid(self):
        response = self.client.get(
            reverse('v1:sub_categories', kwargs={
                'category_id': 100
            })
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND, 'Provide sub category not exists'
        )

    def test_for_valid_category_1(self):
        category = self.category_1
        response = self.client.get(
            reverse('v1:sub_categories', kwargs={
                'category_id': category.id
            })
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubCategorySerializer(
            SubCategory.objects.filter(category=category), many=True
        ).data, response.data)

    def test_for_valid_category_2(self):
        category = self.category_2
        response = self.client.get(
            reverse('v1:sub_categories', kwargs={
                'category_id': category.id
            })
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SubCategorySerializer(
            SubCategory.objects.filter(category=category), many=True
        ).data, response.data)


class ListProductsTestCase(BaseTestCase):

    def test_for_order_by_name(self):
        response = self.client.get(
            build_url('v1:products', params={'order_by': 'name'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('name'), many=True
        ).data, response.data)

    def test_for_order_by_name_desc(self):
        response = self.client.get(
            build_url('v1:products', params={'order_by': 'name', 'order': 'DESC'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('-name'), many=True
        ).data, response.data)

    def test_for_order_by_category(self):
        response = self.client.get(
            build_url('v1:products', params={'order_by': 'sub_category__category'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('sub_category__category'), many=True
        ).data, response.data)

    def test_for_order_by_category_desc(self):
        response = self.client.get(
            build_url(
                'v1:products', params={'order_by': 'sub_category__category', 'order': 'DESC'}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('-sub_category__category'), many=True
        ).data, response.data)

    def test_for_order_by_sub_category(self):
        response = self.client.get(
            build_url('v1:products', params={'order_by': 'sub_category'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('sub_category'), many=True
        ).data, response.data)

    def test_for_order_by_sub_category_desc(self):
        response = self.client.get(
            build_url(
                'v1:products', params={'order_by': 'sub_category', 'order': 'DESC'}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductsSerializer(
            Product.objects.order_by('-sub_category'), many=True
        ).data, response.data)

    def test_create_invalid_category_product(self):
        response = self.client.post(
            build_url('v1:products'),
            data={
                'name': 'Valid Product',
                'sub_category': 0
            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, 'Provide sub category not exists'
        )

    def test_create_valid_category_product(self):
        response = self.client.post(
            build_url('v1:products'),
            data={
                'name': 'Valid Product',
                'sub_category': self.sub_category_1_category_1.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
