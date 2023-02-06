from .Favourites import Favour


def fav(request):
    return {'fav': Favour(request)}