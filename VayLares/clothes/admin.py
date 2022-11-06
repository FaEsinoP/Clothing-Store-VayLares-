from django.contrib import admin

from .models import *


class ClothesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'gender', 'category', 'subcategory', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'gender', 'category')
    list_editable = ('is_published',)
    list_filter = ('gender', 'category', 'subcategory')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    search_fields = ('category_name',)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategory_name', 'category')
    list_display_links = ('id', 'subcategory_name')
    search_fields = ('subcategory_name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name')
    list_display_links = ('id', 'brand_name')
    search_fields = ('brand_name',)


admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
