from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from VayLares import settings
from clothes.views import PageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('clothes.urls')),
    # path('captcha/', include('captcha.urls')),
]
handler404 = PageNotFound

if settings.DEBUG:
    import debug_toolbar
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)