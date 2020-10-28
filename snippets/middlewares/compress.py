from django.http.response import HttpResponse, HttpResponseRedirectBase
from django.utils.deprecation import MiddlewareMixin

from snippets.slimmer import slimmer


class CompressMiddleware(MiddlewareMixin):
    """HTML compress middleware"""
    @staticmethod
    def process_response(request, response):
        if isinstance(response, HttpResponse) \
                and not isinstance(response, HttpResponseRedirectBase) \
                and response.get('Content-Type', '').find('text/html') == 0\
                and response.status_code < 400:
            response.content = slimmer.xhtml_slimmer(response.content)
        return response
