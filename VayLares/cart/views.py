from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from clothes.models import Clothes
from clothes.utils import DataMixin
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Clothes, id=product_id)
    form = CartAddProductForm(request.POST)
    cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Clothes, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


class Basket(DataMixin, ListView):
    model = Clothes
    template_name = 'clothes/basket.html'
    context_object_name = 'goods'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        c_def = self.get_user_context(title='Корзина', cart=cart)
        return dict(list(context.items()) + list(c_def.items()))
