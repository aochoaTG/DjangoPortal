from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from apps.supplier.models import ReqReqMat, ReqReqMatDet


@login_required
def requisitions(request):
    companies = ['Villa Ahumada', 'Castaño', 'Clara', 'Gasomex', 'INMO', 'Jarudo', 'Petrotal',
                 'Picachos', 'SYC', 'VENTANAS', 'ZAID', 'Diaz Gas', 'EC', '1G_TOTALGAS_MCP', 'TSA']
    return render(request, 'administrator/requisitions.html', {'requisitions': requisitions, 'companies': companies})


@login_required
def requisition_details(request, id, company):
    # Vamos a obtener los detalles de la requisición
    lines = ReqReqMatDet().get_lines(id, company)
    return JsonResponse({'success': True, 'html': render(request, 'supplier/modals/requisition_details.html', {'lines': lines}).content.decode('utf-8')})


@login_required
def requisitions_table(request):
    # Llamar al metodo get_all_requisitions() desde el modelo
    requisitions = ReqReqMat().get_all_requisitions()

    # Definimos un diccionario para los estados
    estado_map = {
        'CANCELADA': {'class': 'bg-danger', 'text': 'CANCELADA'},  # CANCELADA
        'LIBERADA': {'class': 'bg-info', 'text': 'LIBERADA'},  # LIBERADA
        'CONCLUIDA': {'class': 'bg-success', 'text': 'CONCLUIDA'},  # CONCLUIDA
        # SIN LIBERAR
        'SIN LIBERAR': {'class': 'bg-warning', 'text': 'SIN LIBERAR'},
        'RECHAZADA': {'class': 'bg-danger', 'text': 'RECHAZADA'},  # RECHAZADA
        # LIBERADA PARCIALMENTE
        'LIBERADA PARCIALMENTE': {'class': 'bg-dark', 'text': 'LIBERADA PARCIALMENTE'},
        # SIN AFECTAR
        'SIN AFECTAR': {'class': 'bg-secondary', 'text': 'SIN AFECTAR'},
    }

    # Construimos el listado de requisiciones
    requisitions_data = []

    # Convertir cada objeto a un diccionario con los atributos de cada campo
    for req in requisitions:
        # Construir acciones dinámicamente
        actions = f'''
            <div class="btn-group">
              <button type="button" class="btn btn-primary btn-sm dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">Acciones</button>
              <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="javascript:void(0);" data-bs-toggle="modal" data-bs-target="#reqDetailsModal" data-id="{req.Folio}" data-company="{req.Company}">Ver partidas</a></li>
        '''

        # Acciones por estado
        if req.Estado == 'LIBERADA':
            actions += f'''
                <li><a class="dropdown-item" href="/requisition/details/{req.Folio}">Solicitud de Cotización</a></li>
            '''
        elif req.Estado == 'CANCELADA':
            actions += '''
                <li><a class="dropdown-item" href="#">Reactivar requisición</a></li>
            '''
        else:
            actions += '''
                <li><a class="dropdown-item" href="#">Acción general</a></li>
            '''

        # Cerrar las acciones
        actions += '''
              </ul>
            </div>
        '''

        # Construir cada objeto requisición
        requisitions_data.append({
            'Empresa': req.Empresa,
            'Folio': req.Folio,
            'Lineas': req.Lineas,
            'TotalCosto': req.TotalCosto,
            'FechaRequisicion': req.FechaRequisicion.strftime('%Y-%m-%d'),
            'usuarioSolicita': req.usuarioSolicita,
            'empleadoSolicita': req.empleadoSolicita,
            'dirigidoA': req.dirigidoA,
            'Referencia': req.Referencia,
            'Estado': f'''
                <span class="badge {estado_map.get(req.Estado, {'class': 'bg-dark', 'text': 'Unknown'})['class']}">
                    {estado_map.get(req.Estado, {'class': 'bg-dark', 'text': 'Unknown'})['text']}
                </span>
            ''',
            'empleadoLibero': req.empleadoLibero,
            'Fecha_liberacion': req.Fecha_liberacion,
            'Cotizó': req.Cotizó,
            'Actions': actions
        })

    # Retornar los datos como respuesta JSON
    return JsonResponse({'data': requisitions_data})
