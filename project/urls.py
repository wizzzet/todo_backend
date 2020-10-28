from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path, include, path
from django.views.static import serve

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from project import views


handler400 = 'views.e400'
handler403 = 'views.e403'
handler404 = 'views.e404'
handler500 = 'views.e500'


api_info = openapi.Info(
    title='Todo Demo API',
    default_version='v1',
    description='API for Todo Demo',
    contact=openapi.Contact(email='wizzzet@gmail.com'),
)

schema_view = get_schema_view(
    api_info,
    validators=['flex'],
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = (
    path(
        'swagger/docs/',
        schema_view.as_view()
    ),
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    )
)

# API urlpatterns
api_urlpatterns = []
for app in settings.API_APPS:
    namespace = app.replace('.', '_')
    api_urlpatterns.append(
        path('api/<str:lang>/%s/' % app, include('%s.api.urls' % app, namespace=namespace))
    )
urlpatterns += tuple(api_urlpatterns)


# MEDIA urlpatterns
if settings.DEBUG is True:
    urlpatterns += (
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    )

if getattr(settings, 'ENV', 'production') == 'dev':
    urlpatterns += tuple(staticfiles_urlpatterns())

urlpatterns += (
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
)
