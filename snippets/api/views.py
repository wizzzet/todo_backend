from django.core.exceptions import FieldDoesNotExist

from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import AllowAny

from snippets.api.swagger.schema import SimpleAutoSchema
from snippets.sites import get_site_id


class PublicViewMixin(object):
    permission_classes = (AllowAny,)


class SiteMixin(object):
    def get_site_id(self):
        return get_site_id(self.request)

    def filter_queryset(self, queryset):
        queryset = super(SiteMixin, self).filter_queryset(queryset)

        try:
            queryset.model._meta.get_field('site')
            queryset = queryset.filter(site_id=self.get_site_id())
        except FieldDoesNotExist:
            try:
                queryset.model._meta.get_field('sites')
                queryset = queryset.filter(sites=self.get_site_id())
            except FieldDoesNotExist:
                pass

        except AttributeError:
            # возможно, это вообще не queryset, а список
            if not isinstance(queryset, (list, tuple, set)):
                raise

        return queryset


class BaseAPIViewMixin(object):
    swagger_schema = SimpleAutoSchema


class PublicAPIViewMixin(PublicViewMixin, BaseAPIViewMixin):
    pass


class BaseListAPIView(SiteMixin, ListAPIView):
    pass


class BaseRetrieveAPIView(SiteMixin, RetrieveAPIView):
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PageRetrieveAPIView(SiteMixin, RetrieveAPIView):
    """Позволяет получать объекты "страниц", уникальные по site_id (наследники BasePage)"""

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return get_object_or_404(queryset, site_id=self.get_site_id())
