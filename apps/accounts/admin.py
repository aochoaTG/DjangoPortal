"""This module contains the admin configuration for the accounts app."""
from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)
