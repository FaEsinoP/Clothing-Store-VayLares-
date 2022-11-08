from django.urls import path

from .views import *

urlpatterns = [
    path('', ClothesHome.as_view(), name='home'),
    path('man/', for_man, name='man'),
    path('woman/', for_woman, name='woman'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('add/', AddProduct.as_view(), name='add'),
    path('login/', login, name='login'),
    path('category/<slug:category_slug>/', ClothesCategory.as_view(), name='category'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
]
