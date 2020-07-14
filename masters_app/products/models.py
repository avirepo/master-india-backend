from django.db import models


class BaseModel(models.Model):
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(
        unique=True,
        max_length=256,
        help_text='Provide category name'
    )

    def __str__(self):
        return f'{self.name}'


class SubCategory(BaseModel):
    category = models.ForeignKey(to='products.Category', on_delete=models.CASCADE)
    name = models.CharField(
        unique=True,
        max_length=256,
        help_text='Provide sub category name'
    )

    def __str__(self):
        return f'{self.category} - {self.name}'


class Product(BaseModel):
    sub_category = models.ForeignKey(to='products.SubCategory', on_delete=models.CASCADE)
    name = models.CharField(
        unique=True,
        max_length=256,
        help_text='Provide prodct name'
    )

    def __str__(self):
        return f'{self.sub_category} - {self.name}'

    @property
    def category(self):
        return self.sub_category.category.name

    @property
    def sub_category_name(self):
        return self.sub_category.name
    
