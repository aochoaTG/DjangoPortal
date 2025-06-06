"""URLs para la aplicación de cuentas."""
from django.urls import path
from django.contrib.auth import views as auth_views
from apps.accounts.forms import UserForm, SupplierFiscalForm, SupplierBankForm
from . import views
from .views import SupplierWizard

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
# Ruta para registrar usuarios
    path('register/', views.register, name='register'),
# Ruta para iniciar sesión
    path('login_view/', views.login_view, name='login_view'),
# Ruta para mostrar los usuarios
    path('show/', views.show, name='show_staff_users'),
# Ruta para mostrar los usuarios proveedores
    path('show_suppliers/', views.show_suppliers, name='show_suppliers'),
    path('create_staff_user', views.create_staff_user, name='create_staff_user'),  # Ruta para crear un usuario
    path('create_supplier_user', views.create_supplier_user, name='create_supplier_user'),  # Ruta para crear un usuario de proveedor
    path('delete_account/<int:user_id>/', views.delete_account, name='delete_account'),  # Ruta para eliminar un usuario
    path('password_change_modal/<int:user_id>/', views.password_change_modal, name='password_change_modal'),
    path('profile_modal/<int:user_id>/', views.profile_modal, name='profile_modal'),
    path('update_staff_account/<int:user_id>/', views.update_staff_account, name='update_staff_account'),
    path('show_catsuppliers', views.show_catsuppliers, name='show_catsuppliers'),
    path('show_table_catsuppliers', views.show_table_catsuppliers, name='show_table_catsuppliers'),
    path('staffusers_table', views.staffusers_table, name='staffusers_table'),
    path('show_suppliers_table', views.show_suppliers_table, name='show_suppliers_table'),
    path('update_cat_supplier_modal/<int:supplier_id>/', views.update_cat_supplier_modal, name='update_cat_supplier_modal'),
    path('delete_catsupplier/<int:supplier_id>/', views.delete_catsupplier, name='delete_catsupplier'),
    path('update_digital_files/<int:supplier_id>/', views.update_digital_files, name='update_digital_files'),
    path('accept_supplier/<int:user_id>/', views.accept_supplier, name='accept_supplier'),
    path('update_supplier_account/<int:user_id>/', views.update_supplier_account, name='update_supplier_account'),
    path('exportar-excel/', views.export_suppliers_to_excel, name='export_suppliers_to_excel'),
    path('import_suppliers_from_excel/', views.import_suppliers_from_excel, name='import_suppliers_from_excel'),
    path('registro/', SupplierWizard.as_view([UserForm, SupplierFiscalForm, SupplierBankForm]), name='supplier_wizard'),
    path('verify_supplier/<str:verification_token>/', views.verify_supplier, name='verify_supplier'),
    path('upload_docs/<str:verification_token>/', views.upload_docs, name='upload_docs'),
    # Cargar documento individual
    path('supplier/<int:supplier_id>/document/<int:document_type_id>/upload/', views.upload_document, name='upload_document'),
    # Actualizar estado de documento
    path('document/<int:document_id>/update-status/', views.update_document_status, name='update_document_status'),
    # Eliminar documento
    path('supplier/document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    # Nueva URL para ver el documento
    path('document/<int:document_id>/view/', views.view_document, name='view_document'),
]
