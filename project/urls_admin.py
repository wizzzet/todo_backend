from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path, include, path
from django.views.static import serve


admin.autodiscover()

urlpatterns = (
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
)

if settings.DEBUG is True:
    urlpatterns += (
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    )

if getattr(settings, 'ENV', 'production') == 'dev':
    urlpatterns += tuple(staticfiles_urlpatterns())

urlpatterns += (
    path('', admin.site.urls),
)
