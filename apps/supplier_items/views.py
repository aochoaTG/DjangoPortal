"""Vistas de la app supplier_items."""
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.supplier_items.models import Product
from apps.supplier_items.forms import ProductForm


@login_required()
def list(request):
    """Muestra la lista de productos."""
    products = Product.objects.select_related('category').all()
    return render(request, 'supplier_items/list.html', {'products': products})


@login_required()
def product_detail(request, pk):
    """Muestra el detalle de un producto."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'supplier_items/product_detail.html', {'product': product})


@login_required
def product_create(request):
    """Crea un nuevo producto."""
    if request.method == 'POST':
        # <-- Asegúrate de incluir request.FILES
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Producto creado exitosamente")
            return redirect('supplier_items:product_detail', pk=product.pk)
        else:
            messages.error(
                request, "Hubo un error en el formulario. Por favor, revisa los campos.")
            # Vamos a guardar los errores en una variable de sesión para mostrarlos en el formulario
            return redirect('supplier_items:product_create')
    else:
        # '/' es la página de fallback
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required()
def product_update(request, pk):
    """Actualiza un producto."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Producto actualizado exitosamente")
            return redirect('supplier_items:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'supplier_items/product_form.html', {'form': form, 'action': 'update'})


@login_required()
def product_delete(request, pk):
    """Elimina un producto."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Producto eliminado exitosamente")
        return redirect('supplier_items:list')  # ✅ Redirección correcta
    return redirect('supplier_items:list')  # ✅ Sin `pk`


@login_required()
def product_modal(request):
    """Muestra el modal de un producto."""
    action = request.GET.get('action')
    # Si recibimos el ID del producto, lo cargamos
    if request.GET.get('id'):
        product = get_object_or_404(Product, pk=request.GET.get('id'))
        form = ProductForm(instance=product)
        return JsonResponse({'success': True, 'html': render(request, 'supplier_items/modals/product_modal.html', {'form': form, 'product': product, 'action': action}).content.decode('utf-8')})
    else:
        form = ProductForm()
        return JsonResponse({'success': True, 'html': render(request, 'supplier_items/modals/product_modal.html', {'form': form, 'action': action}).content.decode('utf-8')})
