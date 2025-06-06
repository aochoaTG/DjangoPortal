"""This module contains the configuration of the accounts app."""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration of the accounts app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
