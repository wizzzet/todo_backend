from rest_framework import serializers

from snippets.api.serializers.mixins import CommonSerializer
from users import models


class AccountProfileSerializer(serializers.ModelSerializer):
    """User's personal data serializer"""

    class Meta:
        model = models.User
        fields = (
            'email', 'first_name', 'id', 'is_staff', 'last_name',
            'middle_name', 'phone', 'username'
        )


class AccountShortSerializer(CommonSerializer):
    """User serializer"""

    user = serializers.SerializerMethodField()

    @staticmethod
    def get_user(obj):
        return AccountProfileSerializer(obj).data
