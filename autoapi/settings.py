from django.conf import settings

DEFAULT_AUTOAPI_CONFIGURATION = {
}

AUTOAPI_CONFIGURATION = getattr(
    settings, 'AUTOAPI_CONFIGURATION', DEFAULT_AUTOAPI_CONFIGURATION)