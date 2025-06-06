""" This module is used to configure the supplier app. """
from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    """ This class is used to configure the supplier app. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.supplier'
