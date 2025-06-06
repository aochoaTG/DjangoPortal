"""Vistas de proveedores."""
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from apps.supplier.forms import SupplierForm
from apps.supplier.models import Supplier


@login_required
def index(request):
    """Vista de inicio."""
    return render(request, 'administrator/index.html')


def index_supplier(request):
    """Vista de inicio de proveedores."""
    return render(request, 'supplier/index.html')


@login_required
def supplier_update(request, user_id):
    """Vista de edición de proveedores."""
    user = get_object_or_404(User, id=user_id)

    try:
        # Intenta obtener el proveedor asociado al usuario
        supplier = Supplier.objects.get(user=user)
    except Supplier.DoesNotExist:
        # Redirige al formulario de creación si no existe el proveedor
        return redirect('supplier_create', user_id=user.id)

    return render(request, 'supplier/supplier_update.html', {'supplier': supplier})


@login_required
def supplier_create(request, user_id):
    """Vista de creación de proveedores."""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'supplier/supplier_create.html', {'user': user})
