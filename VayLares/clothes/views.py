from django.http import HttpResponse
from django.shortcuts import render

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить позицию", 'url_name': 'add'},
        {'title': "Войти", 'url_name': 'login'},
        ]


def index(request):
    return render(request, 'clothes/index.html', {'title': 'Главная страница', 'menu': menu})


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})


def login(reques):
    return HttpResponse("Авторизаtion")

def add(reques):
    return HttpResponse("Добавление позиции")