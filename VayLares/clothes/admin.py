from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ClothesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'gender', 'category', 'subcategory', 'get_html_photo', 'get_html_alternative_photo',
        'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'gender', 'category')
    list_editable = ('is_published',)
    list_filter = ('gender', 'category', 'subcategory')
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        'title', 'slug', 'gender', 'price', 'brand', 'category', 'subcategory', 'content', 'photo', 'get_html_photo',
        'alternative_photo', 'get_html_alternative_photo', 'is_published',)
    readonly_fields = ('time_create', 'get_html_photo', 'get_html_alternative_photo')

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=70>")
        else:
            return "Нет фото"

    get_html_photo.short_description = "Photo"

    def get_html_alternative_photo(self, object):
        if object.alternative_photo:
            return mark_safe(f"<img src='{object.alternative_photo.url}' width=70>")
        else:
            return "Нет фото"

    get_html_alternative_photo.short_description = "Alternative_Photo"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    list_display_links = ('id', 'category_name')
    search_fields = ('category_name',)
    prepopulated_fields = {"slug": ("category_name",)}


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategory_name', 'category')
    list_display_links = ('id', 'subcategory_name')
    search_fields = ('subcategory_name',)
    prepopulated_fields = {"slug": ("subcategory_name",)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name')
    list_display_links = ('id', 'brand_name')
    search_fields = ('brand_name',)
    prepopulated_fields = {"slug": ("brand_name",)}


admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
