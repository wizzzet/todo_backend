from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler,\
    jwt_encode_handler

from snippets.api.serializers.mixins import CommonSerializer
from users.models import User


class JWTSerializer(JSONWebTokenSerializer):
    """
    JWT serializer
    """
    def __init__(self, *args, **kwargs):
        super(JWTSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.EmailField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            params = Q()
            for login_field in User.LOGIN_FIELDS:
                params |= Q(**{login_field: attrs.get(self.username_field)})
            fuser = User.objects.filter(params)

            if fuser:
                credentials[self.username_field] = getattr(fuser.first(), self.username_field)
                user = authenticate(**credentials)

                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    if not user.has_crm_access:
                        msg = _('No access to CRM.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)


class RegistrationSerializer(CommonSerializer):
    """
    Registration serializer
    """

    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30, required=False, allow_null=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True)
    password = serializers.CharField(max_length=255, required=True)
    username = serializers.EmailField()

    @staticmethod
    def validate_username(value):
        try:
            value = value.lower().strip()
            User.objects.get(email=value)
            raise serializers.ValidationError(_('The specified email is already in use.'))
        except User.DoesNotExist:
            pass

        return value

    def create(self, validated_data):
        kwargs = {
            'email': validated_data['username'].lower().strip(),
            'first_name': validated_data['first_name'].strip(),
            'last_name': validated_data.get('last_name', ''),
            'phone': validated_data.get('phone', None),
            'username': validated_data['username'].lower().strip()
        }
        user = User(**kwargs)
        user.set_password(validated_data['password'])
        user.save()
        return user


class RestorePasswordRequestSerializer(CommonSerializer):
    """
    Password recovery serializer
    """
    user = None
    username = serializers.EmailField()

    def validate_username(self, username):
        try:
            user = User.objects.get(email=username.lower())
            self.user = user
        except User.DoesNotExist:
            raise serializers.ValidationError(_('The specified email could not be found.'))

        return username


class RestorePasswordSerializer(CommonSerializer):
    """
    Password change serializer
    """
    password = serializers.CharField(min_length=5)
    password_confirm = serializers.CharField(min_length=5)
    token = serializers.CharField()
    user = None

    def validate_token(self, value):
        if len(value) != 80:
            raise serializers.ValidationError(_('Recovery token length does not match.'))

        try:
            user = User.objects.get(restore_token=value)

            if timezone.now() >= user.restore_token_expiry:
                raise serializers.ValidationError(_('The recovery token has expired.'))

            self.user = user

        except User.DoesNotExist:
            raise serializers.ValidationError(
                _(
                    'The specified password recovery token was not found. '
                    'It may be outdated or has already been used before.'
                )
            )

        return value

    def validate(self, attrs):

        if attrs['password'].lower() != attrs['password_confirm'].lower():
            raise serializers.ValidationError(_('The specified passwords do not match.'))

        return attrs


class RestoreVerifyTokenSerializer(CommonSerializer):
    """
    Password recovery verifiing serializer
    """
    token = serializers.CharField(min_length=80, max_length=80)
    user = None

    def validate_token(self, value):
        try:
            user = User.objects.get(restore_salt=value)

            if timezone.now() >= user.restore_salt_expiry:
                raise serializers.ValidationError(_('The recovery code has expired.'))

        except User.DoesNotExist:
            raise serializers.ValidationError(
                _(
                    'The specified password recovery code was not found. <br>'
                    'It may be outdated or has already been used before.'
                )
            )

        self.user = user
        return value
