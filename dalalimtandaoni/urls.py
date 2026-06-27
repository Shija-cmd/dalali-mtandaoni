from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.views.static import serve


urlpatterns = [

    path(settings.ADMIN_URL, admin.site.urls),

    path('', include('properties.urls')),

    path('accounts/', include('accounts.urls')),

]

handler404 = 'properties.views.custom_404'
handler403 = 'properties.views.custom_403'
handler500 = 'properties.views.custom_500'


if settings.DJANGO_SERVE_MEDIA:

    urlpatterns += [
        re_path(
            r'^media/(?P<path>.*)$',
            serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]

if settings.DJANGO_SERVE_STATIC:

    urlpatterns += [
        re_path(
            r'^static/(?P<path>.*)$',
            serve,
            {
                'document_root': settings.STATICFILES_DIRS[0]
            }
        )
    ]
