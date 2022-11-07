from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('man/', for_man, name='man'),
    path('woman/', for_woman, name='woman'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('add/', add, name='add'),
    path('login/', login, name='login'),
    path('category/<slug:category_slug>/', show_category, name='category'),
    path('product/<slug:product_slug>/', show_product, name='product'),
]