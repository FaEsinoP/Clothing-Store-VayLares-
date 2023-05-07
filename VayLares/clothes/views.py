from django.contrib.auth import logout, login
from django.contrib.auth.views import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.forms import CartAddProductForm
from .favourites import Favour
from .forms import *
from .serializers import BrandSerializer
from .utils import *

from rest_framework import generics, viewsets


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandAPIlist(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ClothesHome(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['gender_selected'] = None
        c_def = self.get_user_context(title='Главная страница', gender_selected=self.request.session['gender_selected'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        search_request = self.request.GET.get('search', '').title()
        if not search_request:
            return Clothes.objects.filter(is_published=True).select_related('category', 'brand')


class ForMan(DataMixin, ListView):
    paginate_by = 5
    model = Clothes
    template_name = 'clothes/man.html'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['gender_selected'] = 'Для мужчин'
        c_def = self.get_user_context(title='Для мужчин', gender_selected=self.request.session['gender_selected'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Clothes.objects.filter(gender='Man', is_published=True).select_related('brand') | Clothes.objects.filter(
            gender='All', is_published=True).select_related('brand')


class ForWoman(DataMixin, ListView):
    paginate_by = 5
    model = Clothes
    template_name = 'clothes/woman.html'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.request.session['gender_selected'] = 'Для женщин'
        c_def = self.get_user_context(title='Для женщин', gender_selected=self.request.session['gender_selected'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
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
    context_object_name = 'goods'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.category_name), cat_selected=c.pk,
                                      gender_selected=self.request.session['gender_selected'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):

        if self.request.session['gender_selected'] == 'Для мужчин':
            gender = 'Man'
        elif self.request.session['gender_selected'] == 'Для женщин':
            gender = 'Woman'

        if self.request.session['gender_selected']:
            return Clothes.objects.filter(category__slug=self.kwargs['category_slug'], gender=gender,
                                          is_published=True).select_related('brand') | \
                Clothes.objects.filter(category__slug=self.kwargs['category_slug'], gender='All',
                                       is_published=True).select_related('brand')
        return Clothes.objects.filter(category__slug=self.kwargs['category_slug'],
                                      is_published=True).select_related('brand')


class ClothesSubCategory(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/index.html'
    context_object_name = 'goods'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sc = Subcategory.objects.get(slug=self.kwargs['subcategory_slug'])
        c_def = self.get_user_context(title='Подкатегория - ' + str(sc.subcategory_name),
                                      cat_selected=context['goods'][0].category.pk, subcat_selected=sc.pk,
                                      gender_selected=self.request.session['gender_selected'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):

        if self.request.session['gender_selected'] == 'Для мужчин':
            gender = 'Man'
        elif self.request.session['gender_selected'] == 'Для женщин':
            gender = 'Woman'

        if self.request.session['gender_selected']:
            return Clothes.objects.filter(subcategory__slug=self.kwargs['subcategory_slug'], gender=gender,
                                          is_published=True).select_related('brand') | \
                Clothes.objects.filter(subcategory__slug=self.kwargs['subcategory_slug'], gender='All',
                                       is_published=True).select_related('brand')

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

        c_def = self.get_user_context(title=context['good'], sizes=sizes, soc=soc, gender_selected=gender_selected)
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


class Profile(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'clothes/profile.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профиль')
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))


class ClothesOrders(LoginRequiredMixin, DataMixin, ListView):
    model = Orders
    template_name = 'clothes/orders.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Orders.objects.filter(user_name=self.request.user.username).prefetch_related('product__id_clothes',
                                                                                              'product__id_size')
        lst = [ord.id for ord in orders]
        ord_of_clothes = Orders_of_Clothes.objects.filter(id_order__in=lst).select_related('id_clothes_with_size',
                                                                                           'id_order')
        c_def = self.get_user_context(title='Мои заказы', orders=orders, ord_of_clothes=ord_of_clothes)
        return dict(list(context.items()) + list(c_def.items()))


class ResetPassword(PasswordResetView):
    template_name = 'clothes/password_reset_email.html'


class ResetDone(PasswordResetDoneView):
    template_name = 'clothes/password_reset_done.html'


class ConfirmNewPass(PasswordResetConfirmView):
    template_name = 'clothes/password_reset_confirm.html'


class ResetComplete(DataMixin, PasswordResetCompleteView, LoginView):
    form_class = LoginUserForm
    template_name = 'clothes/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация", newpass=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')
