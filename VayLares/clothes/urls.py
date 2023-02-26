from django.urls import path, include
from .views import *
from rest_framework import routers

from django.contrib.auth import views as auth_views

router = routers.SimpleRouter()
router.register(r'clothes', ClothesViewSet)

urlpatterns = [
    # path('api/v1/clotheslist', ClothesViewSet.as_view({'get': 'list'})),
    # path('api/v1/clotheslist/<int:pk>/', ClothesViewSet.as_view({'put': 'update'})),
    path('api/v1/', include(router.urls)),
    path('', ClothesHome.as_view(), name='home'),
    path('man/', ForMan.as_view(), name='man'),
    path('woman/', ForWoman.as_view(), name='woman'),
    path('about/', About.as_view(), name='about'),
    path('faq/', Faq.as_view(), name='faq'),
    path('add/', AddProduct.as_view(), name='add'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('category/<slug:category_slug>/', ClothesCategory.as_view(), name='category'),
    path('subcategory/<slug:subcategory_slug>', ClothesSubCategory.as_view(), name='subcategory'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),

    path('fav/', Favourites.as_view(), name='fav_detail'),
    path('fav/add/<int:product_id>/', fav_add, name='fav_add'),
    path('fav/remove/<int:product_id>/', fav_remove, name='fav_remove'),

    path('profile/', Profile.as_view(), name='profile'),
    path('orders/', ClothesOrders.as_view(), name='orders'),

    path('reset_password/', ResetPassword.as_view(), name='reset_password'),
    path('reset_password_sent/', ResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ConfirmNewPass.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', ResetComplete.as_view(), name='password_reset_complete'),
]
