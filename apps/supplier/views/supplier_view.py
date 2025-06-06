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

    # # Si el proveedor existe, permite editar
    # if request.method == 'POST':
    #     form = SupplierForm(request.POST, request.FILES, instance=supplier)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(
    #             request, f'¡El proveedor {form.cleaned_data.get('company_name')} fue actualizado correctamente!')
    #         # '/' es la página de fallback
    #         return redirect(request.META.get('HTTP_REFERER', '/'))
    # else:
    #     form = SupplierForm(instance=supplier)

    return render(request, 'supplier/supplier_update.html', {'form': form, 'supplier': supplier})


@login_required
def supplier_create(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # if request.method == 'POST':
    #     form = SupplierForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         supplier = form.save(commit=False)
    #         supplier.user = user  # Asocia el proveedor con el usuario
    #         supplier.save()
    #         messages.success(
    #             request, f'¡El proveedor {form.cleaned_data.get('company_name')} fue actualizado correctamente!')
    #         # Redirige a la vista de edición después de crear
    #         return redirect('supplier_update', user_id=user.id)
    # else:
    #     form = SupplierForm()

    return render(request, 'supplier/supplier_create.html', {'form': form, 'user': user})
