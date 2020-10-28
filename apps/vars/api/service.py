from django.conf import settings


def get_default_admins():
    return ','.join([admin[1] for admin in settings.ADMINS])
