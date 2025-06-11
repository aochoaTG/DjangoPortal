"""This module contains the urls for the supplier app."""
from .views import *

from django.urls import path

urlpatterns = [
    path('dashboard/', index, name='administrator_dashboard'),
    path('administrator/', index, name='administrator_index'),
    path('requisitions/', requisitions, name='requisitions'),
    path('requisition_lines/', requisition_lines, name='requisition_lines'),


    path('supplier/', index_supplier, name='supplier_index'),
    path('supplier_dashboard/', index_supplier, name='supplier_dashboard'),
    path('supplier/<int:user_id>/update/',
         supplier_update, name='supplier_update'),
    path('supplier/<int:user_id>/create/',
         supplier_create, name='supplier_create'),

    path('request_quote', request_quote, name='request_quote'),
    path('quote_requests', quote_requests, name='quote_requests'),
    path('delete_rfq/<int:id>/', delete_rfq, name='delete_rfq'),

    path('notices/', notices, name='notices'),
    path('notices_table/', notices_table, name='notices_table'),

    path('notices_supplier/', notices_supplier, name='notices_supplier'),
    path('notices_table_supplier/', notices_table_supplier, name='notices_table_supplier'),
    
    path('delete_notice/<int:notice_id>/', delete_notice, name='delete_notice'),
    path('edit_notice/<int:notice_id>/', edit_notice, name='edit_notice'),

    path('requisition_lines_table/', requisition_lines_table,
         name='requisition_lines_table'),
    path('requisitions_table/', requisitions_table, name='requisitions_table'),
    path('requisitions/<int:id>/<str:company>/details/',
         requisition_details, name='requisition_details'),

    path('purchase_orders/', purchase_orders, name='purchase_orders'),
    path('purchase_orders_table', purchase_orders_table,
         name='purchase_orders_table'),

    path('quote_requests_table/', quote_requests_table, name='quote_requests_table'),

    path('admin_quote_requests_table/', admin_quote_requests_table, name='admin_quote_requests_table'),
    path('quotes_table/', quotes_table, name='quotes_table'),
    path('rfq/<int:rfq>/edit/', edit_quote_request, name='edit_quote_request'),

    path('generate_rfq_pdf/<int:id>/', generate_rfq_pdf, name='generate_rfq_pdf'),
    path('generate_rfq_supplier_pdf/<int:id>/', generate_rfq_supplier_pdf, name='generate_rfq_supplier_pdf'),

    path('supplier_rfq/', supplier_rfq, name='supplier_rfq'),
    path('quotes/', quotes, name='quotes'),

    path('addQuoteModal/', addQuoteModal, name='addQuoteModal'),

    path('reject_request/<int:id>/', reject_request, name='reject_request'),
    path('upload_quote/', upload_quote, name='upload_quote'),

    path('docs_validation/', docs_validation, name='docs_validation'),
    path('docs_validation_table/', docs_validation_table, name='docs_validation_table'),
    path('<int:supplier_id>/document/<str:doc_code>/approve/', approve_document_view, name='approve_document'),

     path(
     '<int:supplier_id>/document/<str:doc_code>/reject/',
     reject_document_view,
     name='reject_document'
     ),

     path('load_quote/<int:quote_request_id>/', load_quote, name='load_quote'),
]
