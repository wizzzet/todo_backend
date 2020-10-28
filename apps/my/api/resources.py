from rest_framework.views import APIView
from rest_framework.response import Response

from my.api import serializers


class AccountView(APIView):
    """Personal area"""

    @staticmethod
    def get(request):
        return Response(
            serializers.AccountShortSerializer(request.user, context={'request': request}).data
        )
