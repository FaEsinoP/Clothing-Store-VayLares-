from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.forms import CartAddProductForm
from .Favourites import Favour
from .forms import *
from .serializers import ClothesSerializer
from .utils import *

from rest_framework import generics, viewsets


class ClothesViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = ClothesSerializer


class BrandAPIlist(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = ClothesSerializer


class BrandAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = ClothesSerializer


class ClothesHome(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Имя коллекции, которая используется в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        search_request = self.request.GET.get('search', '').title()
        if not search_request:
            return Clothes.objects.filter(is_published=True).select_related('category', 'brand')


class ForMan(DataMixin, ListView):
    paginate_by = 5
    model = Clothes
    template_name = 'clothes/man.html'
    context_object_name = 'goods'  # Имя коллекции, которая используется в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Для мужчин', gender_selected='Для мужчин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(gender='Man', is_published=True).select_related('brand') | Clothes.objects.filter(
            gender='All', is_published=True).select_related('brand')


class ForWoman(DataMixin, ListView):
    paginate_by = 5
    model = Clothes
    template_name = 'clothes/woman.html'
    context_object_name = 'goods'  # Имя коллекции, которая используется в шаблоне

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Для женщин', gender_selected='Для женщин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(gender='Woman', is_published=True).select_related(
            'brand') | Clothes.objects.filter(gender='All', is_published=True).select_related('brand')


class About(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/about.html'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))


class Faq(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/faq.html'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Частые вопросы')
        return dict(list(context.items()) + list(c_def.items()))


class AddProduct(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGoodForm
    template_name = 'clothes/addgood.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление товара')
        return dict(list(context.items()) + list(c_def.items()))


class ClothesCategory(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Имя коллекции, которая используется в шаблоне
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.category_name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(category__slug=self.kwargs['category_slug'],
                                      is_published=True).select_related('brand')


class ClothesSubCategory(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Имя коллекции, которая используется в шаблоне
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sc = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        c_def = self.get_user_context(title='Подкатегория - ' + str(sc.subcategory_name),
                                      cat_selected=context['goods'][0].category.pk, subcat_selected=sc.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(subcategory__slug=self.kwargs['subcategory_slug'],
                                      is_published=True).select_related('brand')


class ShowProduct(DataMixin, DetailView):
    model = Clothes
    form_class = CartAddProductForm
    template_name = 'clothes/good.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sizes = context['good'].sizes.all()
        soc = Sizes_of_Clothes.objects.filter(id_clothes=context['good'].id, count__gt=0).values_list('id_size',
                                                                                                      flat=True)

        c_def = self.get_user_context(title=context['good'], sizes=sizes, soc=soc)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'clothes/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        '''Логинит пользователя при успешной регистрации'''
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'clothes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def PageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@require_POST
def fav_add(request, product_id):
    fav = Favour(request)
    product = get_object_or_404(Clothes, id=product_id)
    fav.add(product=product)
    print(request.path_info)
    return redirect('fav_detail')


def fav_remove(request, product_id):
    fav = Favour(request)
    fav.remove(product_id)
    return redirect('fav_detail')


class Favourites(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/favourites.html'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        fav = Favour(self.request)
        c_def = self.get_user_context(title='Избранное', fav=fav)
        return dict(list(context.items()) + list(c_def.items()))


class Profile(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'clothes/profile.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Личный кабинет')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.all()