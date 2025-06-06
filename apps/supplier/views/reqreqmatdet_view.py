"""Vista para la tabla de líneas de requisición de materiales"""
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from apps.supplier.models import ReqReqMatDet, Supplier


@login_required
def requisition_lines_table(request):
    """Vista para la tabla de líneas de requisición de materiales"""
    # Vamos a obtener los datos de GET
    from_date = request.GET.get('from')
    until_date = request.GET.get('until')
    company = request.GET.get('company')

    lines = ReqReqMatDet().get_all_lines(from_date=from_date,
                                         until_date=until_date, company=company)
    return JsonResponse({"data": lines}, safe=False)


@login_required
def requisition_lines(request):
    """Vista para la tabla de líneas de requisición de materiales"""
    # Obtener fechas desde GET si existen, de lo contrario calcular valores por defecto
    from_date = request.GET.get('from', (timezone.now() - timedelta(days=3)).strftime('%Y-%m-%d'))
    until_date = request.GET.get('until', timezone.now().strftime('%Y-%m-%d'))

    # Vamos a setear la variable company, si existe en GET de lo contrario será 0
    company = request.GET.get('company', '1G_TOTALGAS')

    # suppliers = Supplier.objects.all() # SELECT * FROM [SuppliersPortal].[dbo].[supplier_supplier]
    suppliers = Supplier.objects.filter(user__is_active=True)

    # Lógica para solicitud GET
    return render(request, 'administrator/requisition_lines.html', {'from': from_date, 'until': until_date, 'company': company, 'suppliers': suppliers})
