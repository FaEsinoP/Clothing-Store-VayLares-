from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('man/', for_man, name='man'),
    path('woman/', for_woman, name='woman'),
    path('about/', about, name='about'),
    path('add/', add, name='add'),
    path('login/', login, name='login'),
    path('category/<int:category_id>/', show_category, name='category'),
]