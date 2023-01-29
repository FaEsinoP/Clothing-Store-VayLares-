from django.urls import path

from cart.views import *

app_name = 'cart'

urlpatterns = [
    path('', Basket.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]
