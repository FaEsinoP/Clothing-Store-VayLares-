from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', ClothesHome.as_view(), name='home'),
    path('man/', ForMan.as_view(), name='man'),
    path('woman/', ForWoman.as_view(), name='woman'),
    path('about/', about, name='about'),
    path('faq/', faq, name='faq'),
    path('add/', AddProduct.as_view(), name='add'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('category/<slug:category_slug>/', ClothesCategory.as_view(), name='category'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
]
