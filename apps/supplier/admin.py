"""This module contains the admin configuration for the supplier app."""
from django.contrib import admin
from apps.supplier.models import Notice, NoticeSeen, SupplierQuoteRequest, SupplierQuoteRequestItem

admin.site.register(Notice)
admin.site.register(NoticeSeen)
admin.site.register(SupplierQuoteRequest)
admin.site.register(SupplierQuoteRequestItem)
