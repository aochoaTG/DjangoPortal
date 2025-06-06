"""Vistas para la sección de Órdenes de Compra de Proveedores."""
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from apps.supplier.services import sql_scripts

def validate_date(date_str):
    try:
        return date_str if date_str else None
    except ValueError:
        return None
    
@cache_page(10)  # Cache por 15 minutos
@login_required
def purchase_orders(request):
    default_days_ago = 3
    default_company = '1G_TOTALGAS'
    
    if request.method == 'GET':
        context = {
            'from_date': validate_date(request.GET.get('from_date', (timezone.now() - timedelta(days=default_days_ago)).strftime('%Y-%m-%d'))),
            'until_date': validate_date(request.GET.get('until_date', timezone.now().strftime('%Y-%m-%d'))),
            'company': request.GET.get('company', default_company)
        }
    else:
        context = {
            'from_date': validate_date(request.POST.get('from_date')),
            'until_date': validate_date(request.POST.get('until_date')),
            'company': request.POST.get('company', default_company)
        }
    
    return render(request, 'supplier/purchase_orders.html', context)

@login_required
def purchase_orders_table(request):
    """Vista para obtener los datos de la tabla de Órdenes de Compra de Proveedores."""
    # Lista de parámetros para las consultas
    company = request.GET.get('company')
    from_date = request.GET.get('from_date')
    until_date = request.GET.get('until_date')


    if company == '0':
        company_ids = ['1G_TGS_AHUMADA', '1G_TGS_CASTANO', '1G_TGS_CLARA', '1G_TGS_GASOMEX', '1G_TGS_INMO', '1G_TGS_JARUDO', '1G_TGS_PETROTAL',
                    '1G_TGS_PICACHOS', '1G_TGS_SERVICIOSYC', '1G_TGS_VENTANAS', '1G_TGS_ZAID', '1G_TOTALGAS', '1G_TOTALGAS_EC', '1G_TOTALGAS_MCP', '1G_TOTALGAS_TSA', '1G_TGS_FORMULAGAS']
    else:
        company_ids = [company]

    # Inicializamos una lista para guardar los resultados
    all_purchase_orders = []

    # Iteramos sobre los IDs y ejecutamos la consulta
    for company_id in company_ids:
        pos = sql_scripts.get_purchase_orders(request, company_id, from_date, until_date)
        # Agregamos los resultados a la lista principal
        all_purchase_orders.extend(pos)

    data = []
    for po in all_purchase_orders:

        # Construir acciones dinámicamente
        actions = '<div class="btn-group"><button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">Acciones</button><ul class="dropdown-menu">'
        actions += '<li><a class="dropdown-item" href="#">Acción general</a></li>'
        # Cerrar las acciones
        actions += '</ul></div>'

        data.append({
            'Company': po['company'],
            'Requisición': po['Requisicion'],
            'Estatus': po['Estatus'],
            'Orden Compra': po['Orden Compra'],
            'Fecha OC': po['Fecha OC'],
            'Proveedor': po['Proveedor'],
            'Subtotal': po['SubTotal'],
            'Impuestos': po['Imptos.'],
            'Total': po['Total'],
            'CXP Registrada': po['CXP Registrada'],
            'Factura': po['Factura'],
            'Estatus Factura': po['Estatus Factura'],
            'Actions': actions,
        })

    return JsonResponse({'data': data})
