import MySQLdb as mysql
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from clothes.forms import AddGoodForm
from clothes.models import *
from clothes.utils import DataMixin
from .cart import Cart
from .forms import *


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    if 'select_size' in request.POST:
        size_id = request.POST['select_size']
        product = get_object_or_404(Sizes_of_Clothes, id_clothes=product_id, id_size=size_id)
    else:
        product = get_object_or_404(Sizes_of_Clothes, id=product_id)
    form = CartAddProductForm(product.count, request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    else:
        cart.add(product=product, quantity=1, update_quantity=False)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')


class Basket(DataMixin, CreateView):
    form_class = AddGoodForm
    model = Clothes
    template_name = 'clothes/basket.html'
    allow_empty = False

    def post(self, request, *args, **kwargs):

        con = mysql.connect(user="root",
                            passwd="5555555555A",
                            db="clothes_store")

        cart = Cart(self.request)

        order = Orders(status='In progress', user_name=request.user.username)
        order.save()

        for item in cart:
            order.product.add(item['product'])
        order.save()

        with con:
            cur = con.cursor()
            cur.execute("UPDATE clothes_orders SET total_price = %s WHERE id = %s", (cart.get_total_price(), order.id))

            for item in cart:
                cur.execute("UPDATE clothes_sizes_of_clothes SET count = %s WHERE id = %s",
                            (item['product'].count - int(item['quantity']), item['product'].id))
                cur.execute(
                    "UPDATE clothes_orders_of_clothes SET count = %s WHERE id_order_id = %s AND id_clothes_with_size_id = %s",
                    (int(item['quantity']), order.id, item['product'].id))

            con.commit()

        cart.clear()
        return redirect('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        c_def = self.get_user_context(title='Корзина', cart=cart, len=cart.__len__())
        return dict(list(context.items()) + list(c_def.items()))
