import datetime

from django.conf import settings
from django.contrib.sites.models import Site


def get_site_param(request, rest=True):
    getter = request.query_params if rest else request.GET
    site_param = getter.get('site', None)

    try:
        site_param = int(site_param)
    except (TypeError, ValueError):
        site_param = None

    if not site_param:
        return datetime.date.today().year

    return site_param


def get_site_url(site):
    if site.domain.split('.')[0] == str(datetime.datetime.today().year):
        return settings.SITE_URL
    return f'{settings.SITE_PROTOCOL}{site.domain}'


def get_site(request):
    site_param = get_site_param(request)
    domain = f'{site_param}.{settings.SITE_NAME}'
    site = Site.objects.get(domain=domain)
    site.url = get_site_url(site)
    return site


def get_site_id(request):
    site = get_site(request)
    return site.id


def get_default_site():
    domain = f'{datetime.date.today().year}.{settings.SITE_NAME}'
    return Site.objects.get(domain=domain)


def get_default_site_id():
    return get_default_site().id
