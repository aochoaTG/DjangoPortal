"""URLs para la aplicaciones de suppliers."""
from django.urls import path
from . import views

app_name = 'supplier_items'

urlpatterns = [
    path('', views.list, name='list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('productModal/', views.product_modal, name='product_modal'),
]
