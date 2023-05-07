from .favourites import Favour


def fav(request):
    return {'fav': Favour(request)}
