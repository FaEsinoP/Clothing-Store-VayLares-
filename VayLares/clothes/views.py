from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


# def index(request):
#     goods = Clothes.objects.all()
#     context = {
#         'goods': goods,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#
#     return render(request, 'clothes/index.html', context=context)

class ClothesHome(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Для отображения товаров

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(is_published=True)


def for_man(request):
    goods = Clothes.objects.filter(gender='All')

    context = {
        'goods': goods,
        'menu': menu,
        'title': 'Для мущжчин',
        'cat_selected': 0,
    }
    return render(request, 'clothes/man.html', context=context)


def for_woman(request):
    goods = Clothes.objects.filter(gender='Woman')
    context = {
        'goods': goods,
        'menu': menu,
        'title': 'Для женщин',
        'cat_selected': 0,
    }
    return render(request, 'clothes/woman.html', context=context)


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})


def faq(request):
    return HttpResponse("Частый вопросы")


def login(request):
    return HttpResponse("Авторизаtion")


# def add(request):
#     if request.method == 'POST':
#         form = AddGoodForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddGoodForm()
#     return render(request, 'clothes/addgood.html', {'form': form, 'title': 'Добавление товара', 'menu': menu})


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


# def show_category(request, category_slug):
#     goods = Clothes.objects.filter(category__slug=category_slug)
#     context = {
#         'goods': goods,
#         'menu': menu,
#         'title': 'Категория',
#         'cat_selected': category_slug,
#     }
#
#     return render(request, 'clothes/index.html', context=context)

class ClothesCategory(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'  # Для отображения товаров
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['goods'][0].category),
                                      cat_selected=context['goods'][0].category_id)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):  # Указываем, что именно выбирать из модели
        return Clothes.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


# def show_product(request, product_slug):
#     good = get_object_or_404(Clothes, slug=product_slug)
#     context = {
#         'good': good,
#         'menu': menu,
#         'title': good.title,
#         'cat_selected': good.category_id,
#     }
#
#     return render(request, 'clothes/good.html', context=context)

class ShowProduct(DataMixin, DetailView):
    model = Clothes
    template_name = 'clothes/good.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['good'])
        return dict(list(context.items()) + list(c_def.items()))
