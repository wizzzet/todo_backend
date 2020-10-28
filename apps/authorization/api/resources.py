from datetime import timedelta

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from authorization.api import serializers, service
from snippets.api.auth import jwt_response_payload_handler
from snippets.api.response import success_response, validation_error_response
from snippets.api.swagger import response as openapi_response
from snippets.api.views import PublicAPIViewMixin
from snippets.utils import datetime
from snippets.utils.datetime import utcnow
from snippets.utils.email import send_email
from snippets.utils.passwords import generate_recovery_token


class LoginView(PublicAPIViewMixin, JSONWebTokenAPIView):
    """
    User authorization
    """
    serializer_class = serializers.JWTSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response = Response(jwt_response_payload_handler(token, user, request))

            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(
                    api_settings.JWT_AUTH_COOKIE, token, expires=expiration, httponly=True
                )

            user.last_login = timezone.now()
            user.save()
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(PublicAPIViewMixin, APIView):
    """
    Logout
    With token invalidation in future
    """
    @staticmethod
    def delete(request, **kwargs):
        return success_response()


class RegistrationView(PublicAPIViewMixin, APIView):
    """
    Registration and authorization of new user
    """
    serializer_class = serializers.RegistrationSerializer

    @swagger_auto_schema(
        request_body=serializers.RegistrationSerializer,
        responses={
            200: openapi_response.jwt_token_response,
            400: openapi_response.validation_error_response,
        }
    )
    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        service.register_user(serializer)
        return success_response(str(_(
            'Registration completed successfully. '
            'The administrator will review your request and give you access.'
        )))


class RestorePasswordRequestView(PublicAPIViewMixin, APIView):
    """
    Sets salt hash for user password recovery process
    """
    @swagger_auto_schema(
        request_body=serializers.RestorePasswordRequestSerializer,
        responses={
            200: openapi_response.success_response,
            400: openapi_response.validation_error_response,
        }
    )
    def post(self, request, **kwargs):

        serializer = serializers.RestorePasswordRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        serializer.user.restore_salt = generate_recovery_token()
        serializer.user.restore_salt_expiry = utcnow() + timedelta(hours=3)
        serializer.user.restore_token = None
        serializer.user.restore_token_expiry = None
        serializer.user.save()

        send_email(
            'restore_link',
            [serializer.user.email],
            _('Password Reset Request'),
            params={
                'site': settings.SITE_NAME,
                'site_url': settings.SITE_URL,
                'user': serializer.user,
                'salt': serializer.user.restore_salt,
                'request': request
            }
        )

        return success_response(
            _('Reset link has been sent to your email.')
        )


class RestoreVerifyTokenView(PublicAPIViewMixin, APIView):
    """
    Sets restore hash for user password recovery process
    """
    @swagger_auto_schema(
        request_body=serializers.RestoreVerifyTokenSerializer,
        responses={
            200: openapi_response.recovery_token_response,
            400: openapi_response.validation_error_response,
        }
    )
    def post(self, request, **kwargs):

        serializer = serializers.RestoreVerifyTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        serializer.user.restore_salt = None
        serializer.user.restore_salt_expiry = None
        serializer.user.restore_token = generate_recovery_token()
        serializer.user.restore_token_expiry = utcnow() + timedelta(hours=3)
        serializer.user.save()

        return Response({'token': serializer.user.restore_token})


class RestorePasswordView(PublicAPIViewMixin, APIView):
    """
    Set new password from form during password recovery process
    """
    @swagger_auto_schema(
        request_body=serializers.RestorePasswordSerializer,
        responses={
            200: openapi_response.jwt_token_response,
            400: openapi_response.validation_error_response,
        }
    )
    def post(self, request, **kwargs):

        serializer = serializers.RestorePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        user = serializer.user
        raw_password = serializer.validated_data['password']

        user.restore_token = None
        user.restore_token_expiry = None
        user.set_password(raw_password)
        user.save()

        send_email(
            'recovery_new_password',
            [user.email],
            _('New password on the site %s') % settings.SITE_NAME,
            params={
                'site': settings.SITE_NAME,
                'site_url': settings.SITE_URL,
                'user': user,
                'password': raw_password,
                'request': request
            }
        )

        serializer = serializers.JWTSerializer()
        authorization_data = serializer.validate(attrs={
            'username': user.email,
            'password': raw_password
        })

        response_data = jwt_response_payload_handler(authorization_data['token'], user, request)
        return Response(response_data)
