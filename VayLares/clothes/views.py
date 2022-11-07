from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *

menu = [{'title': "Для мужчин", 'url_name': 'man'},
        {'title': "Для женщин", 'url_name': 'woman'},
        {'title': "Добавить позицию", 'url_name': 'add'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def index(request):
    goods = Clothes.objects.all()
    context = {
        'goods': goods,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'clothes/index.html', context=context)


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


def add(request):
    if request.method == 'POST':
        form = AddGoodForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = AddGoodForm()
    return render(request, 'clothes/addgood.html', {'form': form, 'title': 'Добавление товара', 'menu': menu})


def show_category(request, category_slug):
    goods = Clothes.objects.filter(category__slug=category_slug)
    context = {
        'goods': goods,
        'menu': menu,
        'title': 'Категория',
        'cat_selected': category_slug,
    }

    return render(request, 'clothes/index.html', context=context)


def show_product(request, product_slug):
    good = get_object_or_404(Clothes, slug=product_slug)
    context = {
        'good': good,
        'menu': menu,
        'title': good.title,
        'cat_selected': good.category_id,
    }

    return render(request, 'clothes/good.html', context=context)
