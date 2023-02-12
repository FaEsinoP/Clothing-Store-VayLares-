import copy

from django.conf import settings
from clothes.models import Clothes


class Favour:

    def __init__(self, request):
        self.session = request.session
        fav = self.session.get(settings.FAV_SESSION_ID)
        if not fav:
            fav = self.session[settings.FAV_SESSION_ID] = {}
        self.fav = fav
        self.lst = [int(item) for item in self.fav]  # Чтобы менят кнопку в товаре на закрашенную

    def __iter__(self):
        product_ids = self.fav.keys()
        products = Clothes.objects.filter(id__in=product_ids)

        fav = copy.deepcopy(self.fav)

        for product in products:
            fav[str(product.id)]['product'] = product

        for item in fav.values():
            yield item

    def __len__(self):
        return len(self.fav)

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.fav:
            self.fav[product_id] = {'quantity': 1}
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.fav:
            del self.fav[product_id]
            self.save()
