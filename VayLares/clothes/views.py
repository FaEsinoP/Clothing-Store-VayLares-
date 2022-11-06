from django.http import HttpResponse
from django.shortcuts import render

from clothes.models import Clothes, Category

menu = [{'title': "Для мужчин", 'url_name': 'man'},
        {'title': "Для женщин", 'url_name': 'woman'},
        {'title': "Добавить позицию", 'url_name': 'add'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "О сайте", 'url_name': 'about'},
        ]


def index(request):
    goods = Clothes.objects.all()
    cats = Category.objects.all()
    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'clothes/index.html', context=context)


def for_man(request):
    goods = Clothes.objects.filter(gender='All')
    cats = Category.objects.all()

    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Для мущжчин',
        'cat_selected': 0,
    }
    return render(request, 'clothes/man.html', context=context)


def for_woman(request):
    goods = Clothes.objects.filter(gender='Woman')
    cats = Category.objects.all()
    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Для женщин',
        'cat_selected': 0,
    }
    return render(request, 'clothes/woman.html', context=context)


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})


def login(request):
    return HttpResponse("Авторизаtion")


def add(request):
    return HttpResponse("Добавление позиции")


def show_category(request, category_id):
    goods = Clothes.objects.filter(category=category_id)
    cats = Category.objects.all()
    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Категория',
        'cat_selected': category_id,
    }

    return render(request, 'clothes/index.html', context=context)


def show_product(request, product_id):
    return HttpResponse(f'Товар №{product_id}')