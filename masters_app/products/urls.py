from django.conf.urls import url

import products.views as views

urlpatterns = [
    url(
        r'^app/category/$',
        views.CategoryList.as_view(),
        name='categories'
    ),
    url(
        r'^app/sub-category/(?P<category_id>[0-9]+)/$',
        views.SubCategoryList.as_view(),
        name='sub_categories'
    ),
    url(
        r'^app/products/$',
        views.ProductListCreate.as_view(),
        name='products'
    ),
]
