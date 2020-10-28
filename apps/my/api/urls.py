from django.urls import path

from my.api import resources


app_name = 'my'

urlpatterns = (
    path(
        'account/',
        resources.AccountView.as_view(),
        name='account'
    ),
)
