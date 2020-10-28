from rest_framework import serializers

from users import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')
