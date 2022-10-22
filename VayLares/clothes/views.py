from django.http import HttpResponse
from django.shortcuts import render

menu = ['Главная', 'Добавить', 'О сайте']


def index(request):
    return render(request, 'clothes/index.html', {'title': 'Главная страница', 'menu': menu})


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})
