from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.urls import re_path
from django.urls import include


urlpatterns = [
    path('api/v1.0/', include([
        re_path('^folders/', include("folders.urls")),
        re_path('^groups/', include("groups.urls")),
    ]))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
