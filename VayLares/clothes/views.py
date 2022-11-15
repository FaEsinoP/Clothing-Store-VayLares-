from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class ClothesHome(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Для отображения товаров
    gender_select = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.filter(is_published=True).select_related('category', 'brand')


class ForMan(DataMixin, ListView):
    paginate_by = 6
    model = Clothes
    template_name = 'clothes/man.html'
    context_object_name = 'goods'  # Для отображения товаров

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Для мужчин', gender_selected='Для мужчин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(gender='Man', is_published=True).select_related('brand') | Clothes.objects.filter(
            gender='All', is_published=True).select_related('brand')


class ForWoman(DataMixin, ListView):
    paginate_by = 9
    model = Clothes
    template_name = 'clothes/woman.html'
    context_object_name = 'goods'  # Для отображения товаров

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Для женщин', gender_selected='Для женщин')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(gender='Woman', is_published=True).select_related(
            'brand') | Clothes.objects.filter(gender='All', is_published=True).select_related('brand')


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})


def faq(request):
    return HttpResponse("Частый вопросы")


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
    context_object_name = 'goods'  # Для отображения товаров
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.category_name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(category__slug=self.kwargs['category_slug'],
                                      is_published=True).select_related('category', 'brand')


class ShowProduct(DataMixin, DetailView):
    model = Clothes
    template_name = 'clothes/good.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['good'])
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
