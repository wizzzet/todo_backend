from django.urls import path

from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from authorization.api import resources


app_name = 'authorization'

urlpatterns = (
    path(
        'login/',
        resources.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        resources.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'registration/',
        resources.RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'restore/request/',
        resources.RestorePasswordRequestView.as_view(),
        name='restore_password_request'
    ),
    path(
        'restore/password/',
        resources.RestorePasswordView.as_view(),
        name='restore_password'
    ),
    path(
        'restore/verify/',
        resources.RestoreVerifyTokenView.as_view(),
        name='restore_verify_token'
    ),
    path(
        'token/refresh/',
        refresh_jwt_token,
        name='refresh_jwt_token'
    ),
    path(
        'token/verify/',
        verify_jwt_token,
        name='verify_jwt_token'
    )
)
