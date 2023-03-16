import factory
from clothes.models import *


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category_name = 'test_category'
    slug = 'test_category'


class SubcategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subcategory

    subcategory_name = 'test_sub_name'
    slug = 'test_sub_name'
    category = factory.SubFactory(CategoryFactory)


class SizesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sizes

    size_title = 'test_size_title'
    slug = 'test_size_title'
    size = 'test_size'


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    brand_name = 'test_brand_name'
    slug = 'test_brand_name'


class ClothesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clothes

    title = 'clothes_title'
    slug = 'clothes_title'
    content = 'some_description'
    price = 999
    photo = 'jordan1.webp'

    brand = factory.SubFactory(BrandFactory)
    subcategory = factory.SubFactory(SubcategoryFactory)
    category = factory.SubFactory(CategoryFactory)


class Sizes_of_ClothesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Sizes_of_Clothes

    id_clothes = factory.SubFactory(ClothesFactory)
    id_size = factory.SubFactory(SizesFactory)
    count = 10


class ClothesWithSizeFactory(ClothesFactory):
    sizes = factory.RelatedFactory(SizesFactory, 'clothes')
