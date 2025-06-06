"""Vistas para el módulo de comunicados de proveedores."""
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.middleware.csrf import get_token
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from apps.supplier.models import Notice, Supplier,SupplierDocument, DocumentType
from apps.supplier.forms import NoticeForm as notice_form
from apps.notifications.models import Notification
from apps.supplier.models.catsupplier import CatSupplier

# Diccionario para mapear códigos a columnas
DOCUMENT_CODE_TO_COLUMN = {
    'fiscal_situation': 'csf',
    'address_proof': 'comprobante_domicilio',
    'bank_statement': 'caracter_bancario',
    'sat_positive_opinion': 'opinion_sat',
    'incorporation_act': 'acta_constitutiva',
    'legal_power': 'poder_legal',
    'identification': 'identificacion_oficial',
    'imss_opinion': 'opinion_imss',
    'infonavit_opinion': 'opinion_infonavit',
    'supplier_registration_request': 'solicitud_alta',
    'repse': 'repse',
    'confidentiality_agreement': 'confidencialidad',
    'induction_course': 'induccion',
}

# Inversa para obtener code desde columna (opcional si lo necesitas después)
COLUMN_TO_DOCUMENT_CODE = {v: k for k, v in DOCUMENT_CODE_TO_COLUMN.items()}

@login_required
def notices(request):
    """Vista para la tabla de comunicados de proveedores."""
    if request.method == 'GET':
        # Lógica para solicitud GET
        current_date_plus_10 = datetime.now() + timedelta(days=10)
        # Vamos a darle el formato yyyy-mm-dd a la fecha
        current_date_plus_10 = current_date_plus_10.strftime('%Y-%m-%d')
        form = notice_form()
        return render(request, 'supplier/notices.html', {'current_date_plus_10': current_date_plus_10, 'form': form})
    elif request.method == 'POST':
        # Lógica para solicitud POST
        form = notice_form(request.POST, request.FILES)
        if form.is_valid():
            # No guardes aún en la base de datos
            notice = form.save(commit=False)
            notice.created_by = request.user  # Asigna el usuario logueado
            notice.save()  # Ahora guarda con el usuario asignado
            # ahora crearemos una notificacion para cada uno de los usuarios que is_staff sea False y is_active sea True
            for user in User.objects.filter(is_staff=False, is_active=True):
                Notification.objects.create(
                    created_by=request.user,
                    recipient=user,
                    title='Nuevo comunicado de TotalGas',
                    description='¡TotalGas ha publicado un nuevo comunicado! ¡No te lo pierdas!',
                    link='/supplier/profile',
                    notification_type='info',
                    priority=10,
                    expires_at=notice.visible_until,
                    action_text='Ver comunicado',   
                )

                # Tambien vamos a enviar un correo electrónico a cada uno de los usuarios que is_staff sea False y is_active sea True
                send_mail(
                    subject = 'Nuevo comunicado de TotalGas',
                    message = f"¡TotalGas ha publicado un nuevo comunicado! ¡No te lo pierdas! \n\n{notice.title}\n\n{notice.text}\n\n¡No te lo pierdas!",
                    from_email=None,
                    recipient_list=[user.email],
                    html_message='',  # El mensaje en HTML
                )


            # Vamos a redirigir a la vista anterior
            messages.success(
                request, f'¡El comunicado con el título "{notice.title}" fue creado correctamente!')
            # Vamos a retornar un json con success true y el id del comunicado
            return JsonResponse({'success': True, 'id': notice.id})
        else:
            # Si el formulario no es válido, vamos a retornar un json con success false y los errores
            return JsonResponse({'success': False, 'errors': form.errors})

def notices_supplier(request):
    if request.method == 'GET':
        return render(request, 'supplier/notices_supplier.html')
    


@login_required
def notices_table(request):
    """Vista para la tabla de comunicados de proveedores."""
    notices = Notice.objects.all()
    csrf_token = get_token(request)  # Obtén el token CSRF
    # Vamos a crear una nueva lista

    data = [
        {
            'id': notice.id,
            'title': notice.title.strip(),  # Quita espacios en blanco al inicio y al final
            'text': notice.text,  # Quita espacios en blanco al inicio y al final
            # Vamos a formatear la fecha
            'published_at': notice.published_at.strftime('%Y-%m-%d'),
            # Vamos a formatear la fecha
            'visible_until': notice.visible_until.strftime('%Y-%m-%d'),
            'created_by_id': notice.created_by.username,
            # Vamos a formatear la fecha
            'created_at': notice.created_at.strftime('%Y-%m-%d'),
            'actions': f'''
                <div class="btn-group btn-group-sm">
                    <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Acciones</button>
                    <div class="dropdown-menu">
                    <a class="dropdown-item" href="javascript:void(0);" data-bs-toggle="modal" data-bs-target="#showNoticeModal" data-title="{notice.title}" data-text="{notice.text}" data-image="{notice.image.url if notice.image and hasattr(notice.image, 'url') else '/media/notices/default.png'}" data-published_at="{notice.published_at}">Ver</a>
                    <a class="dropdown-item" href="javascript:void(0);" data-bs-toggle="modal" data-bs-target="#editNoticeModal" data-title="{notice.id}" data-url="/suppliers/edit_notice/{notice.id}/">Editar</a>
                    <form method="POST" id="delete-form-{notice.id}" action="/suppliers/delete_notice/{notice.id}/" class="dropdown-item" onsubmit="confirm_delete({notice.id});">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                        <button type="submit" class="btn btn-link text-danger p-0 m-0" style="border: none; background: none;">Eliminar</button>
                    </form>
                    </div>
                </div>
            ''',
        }
        for notice in notices
    ]
    return JsonResponse({'data': data})

def notices_table_supplier(request):
    pass


@login_required
def delete_notice(request, notice_id):
    """Vista para eliminar un comunicado."""
    if request.method == 'POST':
        # Lógica para solicitud POST
        try:
            notice = get_object_or_404(Notice, id=notice_id)
            notice.delete()
            messages.success(
                request, f'¡El comunicado con el título "{notice.title}" fue eliminado correctamente!')
            return redirect('notices')
        except Notice.DoesNotExist:
            messages.error(
                request, '¡Hubo un error al eliminar el comunicado!')
            return redirect('notices')

def edit_notice(request, notice_id):
    """Vista para editar un comunicado."""
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = notice_form(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'¡El comunicado con el título "{notice.title}" fue editado correctamente!')
            return redirect('notices')
        else:
            messages.error(
                request, '¡Hubo un error al editar el comunicado!')
    else:
        # Vamos a retornar el formulario con los datos del comunicado en un archivo html
        form = notice_form(instance=notice)
        return render(request, 'supplier/modals/edit_notice.html', {'form': form, 'notice': notice})

def docs_validation(request):
    """Vista para la validación de documentos."""
    if request.method == 'GET':
        return render(request, 'supplier/docs_validation.html')


def docs_validation_table(request):
    suppliers = Supplier.objects.prefetch_related(
        Prefetch(
            'documents',
            queryset=SupplierDocument.objects.select_related('document_type'),
            to_attr='documentos'
        )
    )

    data = []
    for supplier in suppliers:
        row = {
            'id': supplier.id,
            'razon_social': supplier.company_name,
        }

        # Inicializa cada columna con "No enviado" y sin URL
        for column in DOCUMENT_CODE_TO_COLUMN.values():
            row[column] = {
                'status': 'No enviado',
                'url': None,
                'code': COLUMN_TO_DOCUMENT_CODE[column]  # 👈 se usa para los botones
            }

        # Llena campos reales si hay documento cargado
        for doc in supplier.documentos:
            code = doc.document_type.code
            column_name = DOCUMENT_CODE_TO_COLUMN.get(code)
            if column_name:
                row[column_name] = {
                    'status': doc.get_status_display(),
                    'url': doc.file.url if doc.file else None,
                    'code': code  # 👈 muy importante para saber qué aprobar/rechazar
                }

        data.append(row)

    return JsonResponse(data, safe=False, encoder=DjangoJSONEncoder)

@csrf_exempt
def approve_document_view(request, supplier_id, doc_code):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    supplier = get_object_or_404(Supplier, pk=supplier_id)
    doc_type = get_object_or_404(DocumentType, code=doc_code)

    try:
        document = SupplierDocument.objects.get(supplier=supplier, document_type=doc_type)
    except SupplierDocument.DoesNotExist:
        return JsonResponse({'error': 'Documento no encontrado'}, status=404)

    document.status = 'approved'
    document.reviewed_at = timezone.now()
    document.rejection_reason = None
    document.save()

    # Aqui vamos a notificarle al proveedor que su documento fue aprobado
    Notification.objects.create(
        created_by=request.user,
        recipient=supplier.user,
        title='Documento aprobado',
        description=f'Su documento {doc_type.name} ha sido aprobado.',
        link='/supplier/profile',
        notification_type='info',
        priority=10,
        expires_at=timezone.now() + timedelta(days=30),  # Expira en 30 días
        action_text='Ver documento',
    )

    # Enviar correo electrónico al proveedor
    send_mail(
        subject='Documento aprobado',
        message=f'Su documento {doc_type.name} ha sido aprobado.',
        from_email=None,
        recipient_list=[supplier.user.email],
        html_message='',  # El mensaje en HTML
    )

    return JsonResponse({'status': 'ok', 'new_status': 'Aprobado'})

@csrf_exempt
def reject_document_view(request, supplier_id, doc_code):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])

    try:
        body = json.loads(request.body)
        reason = body.get('reason')
        if not reason:
            return JsonResponse({'error': 'Motivo de rechazo requerido.'}, status=400)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("JSON inválido")

    supplier = get_object_or_404(Supplier, pk=supplier_id)
    doc_type = get_object_or_404(DocumentType, code=doc_code)

    try:
        document = SupplierDocument.objects.get(supplier=supplier, document_type=doc_type)
    except SupplierDocument.DoesNotExist:
        return JsonResponse({'error': 'Documento no encontrado.'}, status=404)

    document.status = 'rejected'
    document.rejection_reason = reason
    document.reviewed_at = timezone.now()
    document.save()

    # Aqui vamos a notificarle al proveedor que su documento fue rechazado
    Notification.objects.create(
        created_by=request.user,
        recipient=supplier.user,
        title='Documento rechazado',
        description=f'Su documento {doc_type.name} ha sido rechazado. Motivo: {reason}',
        link='/supplier/profile',
        notification_type='info',
        priority=10,
        expires_at=timezone.now() + timedelta(days=30),  # Expira en 30 días
        action_text='Ver documento',
    )

    # Enviar correo electrónico al proveedor
    send_mail(
        subject='Documento rechazado',
        message=f'Su documento {doc_type.name} ha sido rechazado. Motivo: {reason}',
        from_email=None,
        recipient_list=[supplier.user.email],
        html_message='',  # El mensaje en HTML
    )

    return JsonResponse({'status': 'ok'})