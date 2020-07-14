from django.contrib import admin

# Register your models here.
from products.models import Category, Product, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('category', 'name',)
    search_fields = ('name', 'category')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('sub_category', 'name',)
    search_fields = ('name', 'sub_category')
