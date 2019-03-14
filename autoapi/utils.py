from django.apps import apps

from autoapi.settings import AUTOAPI_CONFIGURATION


def get_model(app_name, model_name):
    if not app_name or not model_name:
        return None

    if not is_managed(app_name, model_name):
        return None

    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        return None

    return model


def is_managed(app_name, model_name):
    managed_apps = AUTOAPI_CONFIGURATION.keys()
    if not managed_apps:
        return True
    if managed_apps and app_name in managed_apps:
        managed_models = AUTOAPI_CONFIGURATION[app_name].keys()
        if not managed_models or model_name in managed_models:
            return True
    return False
