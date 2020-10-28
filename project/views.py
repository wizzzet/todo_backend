from django.http import HttpResponse
from django.views import View

from rest_framework.decorators import api_view

from snippets.http.response import error_response


@api_view()
def e400(request, exception=None, *args, **kwargs):
    return error_response(status=400)


@api_view()
def e403(request, exception=None, *args, **kwargs):
    return error_response(status=403)


@api_view()
def e404(request, exception=None, *args, **kwargs):
    return error_response(status=404)


def e500(request, *args, **kwargs):
    return error_response(status=500, only_json=True)


class HomeView(View):
    @staticmethod
    def get(request, **kwargs):
        return HttpResponse('API')
