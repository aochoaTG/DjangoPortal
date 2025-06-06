""" Vistas para la creación y gestión de solicitudes de cotización. """
import os
import io
from django.urls import reverse
from django.middleware.csrf import get_token
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum, F
from django.forms import modelformset_factory
from reportlab.lib import colors
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.notifications.models import Notification
from PyPDF2 import PdfReader, PdfWriter
from datetime import timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from apps.supplier.models import Supplier, SupplierQuoteRequest, SupplierQuoteRequestItem
from apps.supplier.services import sql_scripts
from apps.supplier.forms import *
from common.utils import *


@login_required
def request_quote(request):
    suppliers = request.POST.getlist('suppliers[]')
    lines = request.POST.getlist('lines[]')
    company = request.POST.get('company')

    if not suppliers or not lines:
        messages.error(
            request, "Error: No se han recibido proveedores o líneas.")
        # Obtiene la URL anterior desde HTTP_REFERER
        previous_url = request.META.get('HTTP_REFERER')

        # Verifica si la URL anterior es el login, en cuyo caso redirige a otra página
        if previous_url and '/login/' in previous_url:  # Ajusta '/login/' según tu URL de login
            # Redirige a la página principal o donde desees
            return redirect('notices')

        return redirect(previous_url or 'default-url')

    try:
        supplier_requests = {}  # Para almacenar solicitudes existentes o nuevas
        items_created = {}  # Para contar los ítems creados por cada solicitud

        # 🔹 Buscar o crear `SupplierQuoteRequest` para cada proveedor
        for supplier_id in suppliers:
            supplier_instance = get_object_or_404(Supplier, id=supplier_id)
            # ⚠️ Buscar si ya existe una solicitud para el proveedor
            quote_request, created = SupplierQuoteRequest.objects.get_or_create(
                supplier=supplier_instance,
                user=request.user,
                company=company
            )

            supplier_requests[supplier_id] = quote_request
            # Inicializar contador de ítems
            items_created[quote_request.id] = 0

        # 🔹 Crear `SupplierQuoteRequestItem` evitando duplicados
        for line in lines:
            line_items = line.split(',')

            for item in line_items:
                try:
                    line_id, requisition_id, qty, udm, cost = item.split('_')
                except ValueError:
                    messages.error(
                        request, "Error en el formato de las líneas.")
                    return redirect(request.META.get('HTTP_REFERER', 'default-url'))

                for supplier_id, quote_request in supplier_requests.items():
                    # Verificar si el item ya existe en **cualquier solicitud del mismo proveedor**
                    existing_item = SupplierQuoteRequestItem.objects.filter(
                        quote_request__supplier=supplier_id,  # Verificación global por proveedor
                        requisition_id=requisition_id,
                        requisition_line=line_id
                    ).exists()

                    if not existing_item:
                        # Crear el item solo si no existe
                        SupplierQuoteRequestItem.objects.create(
                            quote_request=quote_request,
                            requisition_id=requisition_id,
                            requisition_line=line_id,
                            description=f"Línea {line_id} de la requisición {requisition_id}",
                            quantity=int(qty),
                            unit_of_measurement=udm,
                            # Vamos a cambiar el tipo de dato a float
                            price=float(cost),
                            currency='MXN'
                        )
                        items_created[quote_request.id] += 1

        # Remove empty quote requests and create notifications
        for quote_request_id, count in items_created.items():
            if count == 0 and supplier_requests[supplier_id].created_at == supplier_requests[supplier_id].updated_at:
                quote_request = SupplierQuoteRequest.objects.get(
                    id=quote_request_id)
                quote_request.delete()
                messages.warning(
                    request, f"Se eliminó la solicitud para el proveedor {quote_request.supplier} porque no tenía líneas válidas.")
            elif count > 0:
                # Create notification for suppliers with quote requests
                quote_request = SupplierQuoteRequest.objects.get(
                    id=quote_request_id)

                # Assuming the supplier has a user associated with it
                # Notification.objects.create(
                #     user=quote_request.supplier.user,  # Make sure your Supplier model has a user field
                #     supplier=quote_request.supplier,
                #     title="Nueva Solicitud de Cotización",
                #     description="Has recibido una nueva solicitud de cotización.",
                #     link=f"/quote-requests/{quote_request.id}/",
                #     notification_type="info",
                #     priority=10,
                #     expires_at=timezone.now() + timezone.timedelta(days=7),
                #     action_text="Ver Solicitud"
                # )

        if any(count > 0 for count in items_created.values()):
            messages.success(
                request, "Solicitudes de cotización creadas exitosamente.")
        else:
            messages.warning(
                request, "No se crearon solicitudes de cotización porque todas las líneas ya existían.")

        return redirect(request.META.get('HTTP_REFERER', 'default-url'))

    except Exception as e:
        messages.error(request, f"Error inesperado: {str(e)}")
        return redirect(request.META.get('HTTP_REFERER', 'default-url'))


@login_required
def quote_requests(request):
    """ Vista para mostrar las solicitudes de cotización del proveedor. """
    return render(request, 'supplier/quote_requests.html')


def delete_quote_request(request, id):
    if request.method == 'POST':
        try:
            quote_request = get_object_or_404(SupplierQuoteRequest, id=id)
            quote_request.delete()
            messages.success(
                request, f'¡La solicitud de cotización para el proveedor {quote_request.supplier} fue eliminada correctamente!')
            return redirect('quote_requests')
        except SupplierQuoteRequest.DoesNotExist:
            messages.error(request, '¡La solicitud de cotización no existe!')
            return redirect('quote_requests')


@login_required
def quote_requests_table(request):

    if request.user.is_staff:
        quote_requests = SupplierQuoteRequest.objects.all()
    else:
        supplier = Supplier.objects.get(user=request.user)
        # Vamos a imprimir los datos de supplier
        quote_requests = SupplierQuoteRequest.objects.filter(supplier=supplier).order_by('created_at')

    # Obtener todas las solicitudes con datos agregados
    quote_requests = quote_requests.annotate(
        total_items=Count('items'),  # Cuenta el número de ítems por solicitud
        total_providers=Count('supplier', distinct=True),  # Cuenta el número de proveedores distintos por solicitud
        total_quantity=Sum('items__quantity'),  # Suma total de cantidades de ítems
        total_price=Sum(F('items__quantity') * F('items__price'))  # Calcula el total de todas las líneas
    )

    data = []

    for quote in quote_requests:
        # Botón "Ver" siempre está disponible
        acciones = f'''
            <a class="dropdown-item" href="{reverse('generate_rfq_pdf', args=[quote.id])}" target="_blank"><i class="mdi mdi-eye"></i> Ver solicitud</a>
        '''

        # Si el usuario es staff, permitir también "Editar" y "Eliminar"
        if request.user.is_staff:
            acciones += f'''
                <a class="dropdown-item" href="{reverse('edit_quote_request', args=[quote.id])}"><i class="mdi mdi-pencil"></i> Editar</a>
                <form method="POST" action="{reverse('delete_quote_request', args=[quote.id])}" class="dropdown-item">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{get_token(request)}">
                    <button type="submit" class="btn btn-link text-danger p-0 m-0" style="border: none; background: none;">Eliminar</button>
                </form>
            '''
        else:
            # Si el usuario no es staff, permitir "Cargar cotización" y "Rechazar"
            acciones += f'''
                <a class="dropdown-item" href="javascript:void(0);" data-bs-toggle="modal" data-bs-target="#loadQuoteModal"><i class="mdi mdi-upload"></i> Cotizar</a>
                <a class="dropdown-item" href="javascript:void(0);" onClick="reject_request({quote.id});"><i class="mdi mdi-delete"></i> Rechazar</a>
            '''

        # Agrega el bloque de botones
        actions_html = f'''
            <div class="btn-group btn-group-sm">
                <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Acciones</button>
                <div class="dropdown-menu">
                    {acciones}
                </div>
            </div>
        '''

        data.append({
            'id': str(quote.id),
            'supplier': str(quote.supplier),
            'user': str(quote.user),
            'company': quote.company,
            'notes': quote.notes or '',
            'status': quote.status,
            'created_at': quote.created_at.strftime("%Y-%m-%d"),
            'lines': int(quote.total_items or 0),
            'qty_requested': int(quote.total_quantity or 0),
            'price_total': str(quote.total_price or '0.00'),
            'actions': actions_html,
        })

    return JsonResponse({'data': data})

@login_required
def edit_quote_request(request, pk):
    quote_request = get_object_or_404(SupplierQuoteRequest, pk=pk)

    if not request.user.is_staff:
        return HttpResponse("No tienes permiso para editar esta solicitud.")

    ItemFormSet = modelformset_factory(
        SupplierQuoteRequestItem,
        form=SupplierQuoteRequestItemForm,
        fields=['description', 'quantity', 'unit_of_measurement', 'price', 'currency', 'notes'],
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        header_form = SupplierQuoteRequestEditForm(request.POST)
        formset = ItemFormSet(request.POST, queryset=quote_request.items.all())

        if header_form.is_valid() and formset.is_valid():
            # ✅ Validar que al menos una línea no esté marcada para eliminar
            remaining_forms = [
                form for form in formset.forms
                if not form.cleaned_data.get('DELETE', False)
            ]
            if len(remaining_forms) == 0:
                messages.error(request, "Debe quedar al menos una línea en la solicitud.")
                return render(request, 'supplier/rfq_form.html', {
                    'quote_form': header_form,
                    'item_formset': formset,
                    'mode': 'editar',
                    'quote_id': quote_request.id
                })

            # 👇 Guardado manual de los datos del formulario no-modelo
            supplier = header_form.cleaned_data['supplier']
            company = header_form.cleaned_data['company']
            notes = header_form.cleaned_data['notes']

            quote_request.company = company
            quote_request.notes = notes
            quote_request.supplier = supplier
            quote_request.save()

            # 👇 Guardado del formset de ítems
            for form in formset:
                if form.cleaned_data:
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        form.instance.delete()
                    else:
                        item = form.save(commit=False)
                        item.quote_request = quote_request
                        item.save()

            return redirect('quote_requests')
        else:
            messages.error(request, "Formulario o formset no válidos. Por favor, corrige los errores.")
            return render(request, 'supplier/rfq_form.html', {
                'quote_form': header_form,
                'item_formset': formset,
                'mode': 'editar',
                'quote_id': quote_request.id
            })
    else:
        header_form = SupplierQuoteRequestEditForm(initial={
            'supplier': quote_request.supplier,
            'company': quote_request.company,
            'notes': quote_request.notes,
        })
        formset = ItemFormSet(queryset=quote_request.items.all())

    return render(request, 'supplier/rfq_form.html', {
        'quote_form': header_form,
        'item_formset': formset,
        'mode': 'editar',
        'quote_id': quote_request.id
    })

@login_required
def quotes(request):
    form = SupplierQuoteForm
    # Vamos a obtener las cotizaciones del usuario
    return render(request, 'supplier/quotes.html', {'form': form})

@login_required
def supplier_rfq(request):
    """
    Muestra el formulario para que un proveedor genere una cotización (RFQ)
    y, en POST, procesa el envío guardando la cotización.
    """
    if request.method == 'POST':
        # --------------------------------------------------
        # 1. Si es POST, bind de datos y archivos al formulario
        # --------------------------------------------------
        form = SupplierQuoteForm(request.POST, request.FILES)
        if form.is_valid():
            # --------------------------------------------------
            # 2. Guardamos la instancia sin hacer commit (para asignar user)
            # --------------------------------------------------
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            # --------------------------------------------------
            # 3. Mensaje de éxito (opcional)
            # --------------------------------------------------
            messages.success(request, "Tu cotización se ha enviado correctamente.")
            return redirect('quote_requests')
        else:
            # --------------------------------------------------
            # 4. Si no es válido, caemos al render final mostrando errores
            # --------------------------------------------------
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        # --------------------------------------------------
        # 5. Si es GET, instanciamos el formulario vacío
        # --------------------------------------------------
        form = SupplierQuoteForm()

    # ------------------------------------------------------
    # 6. Renderizamos la plantilla (para GET o POST inválido)
    # ------------------------------------------------------
    return render(request, 'supplier/supplier_rfq.html', {'form': form})

@login_required
def quotes_table(request):
    """
    Devuelve un JSON con las solicitudes de cotización del proveedor,
    incluyendo datos agregados como total de ítems, proveedores, cantidad total y precio total.
    """
    supplier = Supplier.objects.get(user=request.user)
    quote_requests = SupplierQuoteRequest.objects.filter(supplier_id=supplier).annotate(
        total_items=Count('items'),
        total_providers=Count('supplier', distinct=True),
        total_quantity=Sum('items__quantity'),
        total_price=Sum(F('items__quantity') * F('items__price'))
    )

    status_map = {
        'PENDIENTE': '<span class="badge bg-warning">🆕 Por cotizar</span>',
        'VISTA': '<span class="badge bg-primary">👀 Vista</span>',
        'EN REVISION': '<span class="badge bg-info">⏳ En revisión</span>',
        'ACEPTADA': '<span class="badge bg-success">✅ Aceptada</span>',
        'RECHAZADA': '<span class="badge bg-danger">❌ Rechazada</span>',
        'EXPIRADA': '<span class="badge bg-danger">⏲️ Expirada</span>',
    }

    data = [
        {
            'id': f'{quote.id}',
            'supplier': f'{quote.supplier}',
            'user': f'{quote.user}',
            'company': f'{quote.company}',
            'notes': f'{quote.notes}',
            # Mapeo del estado
            'status': f'{status_map.get(quote.status, quote.status)}',
            'created_at': f'{quote.created_at}',
            'lines': f'{int(quote.total_items or 0)}',
            'qty_requested': f'{int(quote.total_quantity or 0)}',
            'price_total': f'{quote.total_price}',
            'actions': f'''
                <div class="btn-group btn-group-sm">
                    <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Acciones</button>
                    <div class="dropdown-menu">
                    <a class="dropdown-item" href="{reverse('generate_rfq_pdf', args=[quote.id])}" target="_blank"><i class="mdi mdi-eye"></i> Ver</a>
                    <a class="dropdown-item" href="javascript:void(0);" data-bs-toggle="modal" data-bs-target="#loadQuoteModal" data-quote-id="{quote.id}"><i class="mdi mdi-upload"></i> Cargar cotización</a>
                    <a class="dropdown-item" href="javascript:void(0);" onClick="reject_request({quote.id});"><i class="mdi mdi-delete"></i>Rechazar</a>
                    </div>
                </div>
            ''',
        }
        for quote in quote_requests
    ]

    return JsonResponse({'data': data})


@login_required
def generate_rfq_pdf(request, id):
    """
    Genera un PDF de Solicitud de Cotización (RFQ) para un proveedor,
    utilizando una plantilla base y agregando datos dinámicamente.
    """

    # 📌 1️⃣ Cargar la plantilla base del PDF
    template_path = os.path.join(settings.BASE_DIR, "static/pdf/RFQ.pdf")
    pdf_reader = PdfReader(template_path)  # Lee el PDF base

    # 📌 2️⃣ Obtener los datos necesarios para la cotización
    quote_request = get_object_or_404(
        SupplierQuoteRequest, id=id)  # Cotización
    # Cambiamos el status de la solicitud a Visto
    quote_request.status = 'VISTA'
    quote_request.viewed_at = timezone.now()
    quote_request.save(
        update_fields=['status', 'viewed_at']
    )

    company_data = sql_scripts.get_company_data(request, quote_request.company)  # Datos de la empresa
    supplier_data = Supplier.objects.filter(user=quote_request.supplier.user)  # Datos del proveedor

    # 📌 3️⃣ Crear un buffer para el PDF generado
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)  # Se crea un lienzo PDF

    # 📌 4️⃣ Agregar información en el PDF (Fecha, título y empresa)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(
        250, 750, f"Fecha de emisión: {quote_request.created_at.strftime('%Y/%m/%d')}")

    p.setFont("Helvetica-Bold", 18)
    p.setFillColorRGB(150, 150, 150)  # Color gris
    p.drawString(50, 700, "SOLICITUD DE COTIZACIÓN")

    # 📌 5️⃣ Agregar los datos de la empresa solicitante
    p.setFont("Helvetica", 10)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(
        50, 650, f"{company_data[0]['Nombre'].title()} - {company_data[0]['rfc']}")
    p.drawString(
        50, 630, f"{company_data[0]['CalleLower'].title()}, {company_data[0]['ColoniaLower'].title()}")
    p.drawString(
        50, 610, f"{company_data[0]['CiudadLower'].title()}, {company_data[0]['EstadoLower'].title()}, C.P. {company_data[0]['CP']}")

    # 📌 6️⃣ Agregar información de la solicitud de cotización
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, 650, "Folio:")
    p.setFont("Helvetica", 10)
    p.drawString(480, 650, f"RFQ-{quote_request.id}")

    # Fecha límite de respuesta
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, 630, "Fecha límite:")
    p.setFont("Helvetica", 10)
    p.drawString(
        480, 630, f"{(quote_request.created_at + timedelta(days=15)).strftime('%Y/%m/%d')}")

    # Teléfono de contacto
    p.setFont("Helvetica-Bold", 10)
    p.drawString(400, 610, "Teléfono:")
    p.setFont("Helvetica", 10)
    if company_data and 'Tel1' in company_data[0]:
        p.drawString(480, 610, f"{company_data[0]['Tel1']}")
    else:
        p.drawString(480, 610, "Teléfono no disponible")

    # 📌 7️⃣ Agregar mensaje al proveedor
    p.setFont("Helvetica-Bold", 11)
    p.setFillColorRGB(0, 0, 0)
    if supplier_data:
        p.drawString(50, 570, f"Estimado {supplier_data[0].company_name},")
    else:
        p.drawString(50, 570, "Estimado proveedor,")

    p.setFont("Helvetica", 10)
    p.drawString(
        50, 550, "Actualmente estamos en el proceso de búsqueda de cotizaciones. Nos gustaría conocer más sobre los productos")
    p.drawString(
        50, 530, "y servicios que su empresa ofrece, por lo que le solicitamos amablemente una cotización detallada para los")
    p.drawString(50, 510, "siguientes artículos/servicios:")

    # 📌 8️⃣ Crear una tabla con los ítems de la solicitud
    styles = getSampleStyleSheet()
    data = [['ID', 'Descripción Producto/Servicio', 'Cantidad', 'UdM', 'Moneda']]

    # Vamos a agregar un ciclo for de 9 elementos
    for i in range(9):
        try:
            item = quote_request.items.all()[i]
            data.append([
                item.requisition_id,
                item.description,
                item.quantity,
                item.unit_of_measurement,
                item.currency
            ])
        except IndexError:
            data.append(['--', '--', '--', '--', '--'])

    # Aqui agregar una validacion, de que si son mas de 9 elementos, se agregue una nueva pagina

    # 📌 9️⃣ Configurar la tabla con estilos
    t = Table(data, colWidths=[40, 275, 65, 65, 65])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B57A4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2B57A4')),
        # Vamos a poner solo el borde inferior de cada fila
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#2B57A4')),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # 📌 🔟 Ajustar la posición de la tabla
    table_width, table_height = t.wrap(500, 500)
    x_position = 50
    y_position = 500
    new_y_position = y_position - table_height  # Evitar que cubra texto anterior

    # Dibujar la tabla
    t.drawOn(p, x_position, new_y_position)

    p.setFont("Helvetica", 7)
    # 📌 1️⃣5️⃣ Dibujar segundo recuadro (DERECHA)
    # Vamos a rellener el rectangulo de amarillo
    p.setFillColorRGB(169, 202, 72)
    p.rect(320, 40, 240, 70, fill=1)  # Segundo recuadro

    # Texto del segundo recuadro
    text2 = """Evaluaremos las propuestas en función del precio, la calidad y la capacidad de su empresa para 
    satisfacer nuestras necesidades específicas. Si requiere información adicional, contactenos.
    """

    # Crear el párrafo con ajuste automático
    paragraph2 = Paragraph(text2, styles["Normal"])
    # Se ajusta dentro del recuadro (ancho=230, alto=65)
    paragraph2.wrapOn(p, 230, 65)
    paragraph2.drawOn(p, 325, 50)  # Posición dentro del recuadro

    # 📌 1️⃣1️⃣ Finalizar y guardar el PDF
    p.showPage()
    p.save()

    # 📌 1️⃣2️⃣ Combinar la plantilla con el nuevo contenido
    buffer.seek(0)
    overlay_pdf = PdfReader(buffer)
    output_pdf = PdfWriter()

    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        if page_number == 0:  # Solo modificar la primera página
            page.merge_page(overlay_pdf.pages[0])
        output_pdf.add_page(page)

    # 📌 1️⃣3️⃣ Retornar el PDF como respuesta HTTP
    output_buffer = io.BytesIO()
    output_pdf.write(output_buffer)
    output_buffer.seek(0)

    response = HttpResponse(output_buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="output.pdf"'
    return response


@login_required
def addQuoteModal(request):
    # Se define un formset basado en el modelo de los ítems de la cotización
    ItemFormSet = modelformset_factory(
        SupplierQuoteRequestItem,
        form=SupplierQuoteRequestItemForm,
        fields=['description', 'quantity', 'unit_of_measurement', 'price', 'currency', 'notes'],
        extra=1,  # Se muestra una fila vacía por defecto
        can_delete=False  # No se permite eliminar desde aquí (puedes cambiarlo si quieres)
    )

    if request.method == 'POST':
        # Se carga el formulario del encabezado (sin modelo ligado)
        header_form = SupplierQuoteRequestCreateForm(request.POST)

        # Se carga el formset con los ítems
        item_formset = ItemFormSet(request.POST)

        # Si ambos formularios son válidos
        if header_form.is_valid() and item_formset.is_valid():
            suppliers = header_form.cleaned_data['supplier']  # Lista de proveedores seleccionados
            company = header_form.cleaned_data['company']
            notes = header_form.cleaned_data['notes']

            # Reunimos los datos válidos de los ítems
            items_data = []
            for form in item_formset:
                if form.cleaned_data and form.cleaned_data.get('description'):
                    items_data.append(form.cleaned_data)

            # Si no hay ítems válidos, se muestra error en el formulario
            if not items_data:
                header_form.add_error(None, "Debe agregar al menos un ítem para enviar la solicitud.")
            else:
                # Se crea una solicitud por cada proveedor
                for supplier in suppliers:
                    quote_request = SupplierQuoteRequest.objects.create(
                        supplier=supplier,
                        company=company,
                        notes=notes,
                        user=request.user
                    )

                    # Se crean los ítems para la solicitud recién creada
                    for item_data in items_data:
                        SupplierQuoteRequestItem.objects.create(
                            quote_request=quote_request,
                            description=item_data['description'],
                            quantity=item_data['quantity'],
                            price=item_data['price'],
                            unit_of_measurement=item_data['unit_of_measurement'],
                            currency=item_data['currency'],
                            notes=item_data.get('notes', '')
                        )

                # Se muestra mensaje de éxito
                messages.success(request, f"Se han creado {len(suppliers)} solicitud(es) de cotización correctamente.")
                return redirect('quote_requests')

    else:
        # Si el método es GET, se inicializa el formulario vacío
        header_form = SupplierQuoteRequestCreateForm()
        item_formset = ItemFormSet(queryset=SupplierQuoteRequestItem.objects.none())

    # Render del formulario en la plantilla
    return render(request, 'supplier/rfq_form.html', {
        'quote_form': header_form,
        'item_formset': item_formset,
        'mode': 'crear'
    })

def reject_request(request, id):
    """ Rechaza una solicitud de cotización y notifica al proveedor. """
    if request.method == 'POST':
        quote_request = get_object_or_404(SupplierQuoteRequest, id=id)
        quote_request.status = 'RECHAZADA'
        quote_request.save(update_fields=['status'])
        # Agregar notificación al administrador
        
        # Vamos a retornar un json con un mensaje de éxito y status
        return JsonResponse({'status': 'success', 'message': 'Solicitud rechazada exitosamente.'})
    
def upload_quote(request):
    if request.method == 'POST':
        # Vamos a recuperar los datos del formulario
        quote_request_id = request.POST.get('quote_request_id')
        quote_file = request.FILES.get('quote_file')
        quote_valid_until = request.POST.get('quote_valid_until')
        quote_promise_date = request.POST.get('quote_promise_date')
        quote_notes = request.POST.get('quote_notes')

        # Vamos a validar que se haya enviado un archivo
        if not quote_file:
            return JsonResponse({'status': 'error', 'message': 'No se ha enviado un archivo.'})
        else:
            # Vamos a guardar el archivo en el sistema de archivos
            quote_request = get_object_or_404(SupplierQuoteRequest, id=quote_request_id)
            quote_request.quote_file = quote_file
            quote_request.quote_valid_until = quote_valid_until
            quote_request.quote_promise_date = quote_promise_date
            quote_request.quote_notes = quote_notes
            quote_request.status = 'EN REVISION'

def load_quote(request, quote_request_id):
    if request.method == 'POST':
        quote_request_id = request.POST.get('quote_request_id')
        quote_file = request.FILES.get('quote_file')

        if not quote_file:
            return JsonResponse({'status': 'error', 'message': 'No se ha enviado un archivo.'})

        # Guardar el archivo en la solicitud de cotización
        quote_request = get_object_or_404(SupplierQuoteRequest, id=quote_request_id)
        quote_request.quote_file = quote_file
        quote_request.status = 'EN REVISION'
        quote_request.save()

        return JsonResponse({'status': 'success', 'message': 'Cotización cargada exitosamente.'})
    
    # Si no es una solicitud POST, entonces vanmos a retornar el formulario form = SupplierQuoteForm aprovechando que nos llego el id de la solicitud
    quote_request = get_object_or_404(SupplierQuoteRequest, id=quote_request_id)
    form = SupplierQuoteForm(instance=quote_request)
    return render(request, 'supplier/modals/load_quote_form.html', {'form': form})