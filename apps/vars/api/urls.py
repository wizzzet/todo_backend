from django.urls import path

from vars.api import resources


app_name = 'vars'

urlpatterns = (
    path(
        '',
        resources.SettingsView.as_view(),
        name='settings'
    ),
)
