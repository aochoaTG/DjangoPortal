$(document).ready(function () {
    let notices_table = $('#notices_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/suppliers/notices_table",
        },
        columns: [
            { "data": "id" },
            { "data": "title" },
            { "data": "text" },
            { "data": "published_at" }, // Permiso CRE
            { "data": "visible_until" },
            { "data": "created_by_id" },
            { "data": "created_at" },
            { "data": "actions" },
        ],
        // Vamos a agregar el campo id como id de la fila
        createdRow: function (row, data, dataIndex) {
            $(row).attr('id', 'row_' + data.id);
            $(row).attr('data-id', data.id);
        },
        initComplete: function () {
            addDataTableFilter('notices_table');
        }
    });

    let requisitions_table = $('#requisitions_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip',
        paging: true,
        info: true,
        buttons: ['copy', 'excel'],
        orderCellsTop: true,
        fixedHeader: true,
        ajax: {
            url: "/suppliers/requisitions_table",
        },
        columns: [
            { data: 'Empresa' },
            { data: 'Folio' },
            { data: 'Lineas' },
            { data: 'TotalCosto', render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            { data: 'FechaRequisicion' },
            { data: 'usuarioSolicita' },
            { data: 'empleadoSolicita' },
            { data: 'dirigidoA' },
            { data: 'Referencia' },
            { data: 'Estado' },
            { data: 'empleadoLibero' },
            { data: 'Fecha_liberacion' },
            { data: 'Cotizó' },
            { data: 'Actions' },
        ],
        initComplete: function () {
            addDataTableFilter('requisitions_table');
        }
    });

    $('#showNoticeModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Botón que abre el modal
        // Extraer los atributos data-* del botón/enlace
        let title = button.data('title');
        let text = button.data('text');
        let image = button.data('image');
        let publishedAt = button.data('published_at');

        // Actualizar el contenido del modal
        $('#show_title').text(title);
        $('#show_text').text(text);
        $('#show_image').attr('src', image);
        $('#show_published_at').text(`Fecha de publicación: ` + publishedAt);
    });

    $('#reqDetailsModal').on('show.bs.modal', function (event) {
        $('#reqDetailsModalContent').html(''); // Limpiar el contenido del modal
        // SELECT * FROM vt_req_mat_dash
        let button = $(event.relatedTarget); // Botón que abre el modal
        // Extraer los atributos data-* del botón/enlace
        let id = button.data('id');
        let company = button.data('company');

        // Vamos a mandar a pedir los datos del formulario por medio de AJAX
        $.ajax({
            url: "/suppliers/requisitions/" + id + '/' + company + "/details",
            method: 'GET',
            success: function (data) {
                console.log(data);
                // Buscamos el elemento con el id #reqDetailsModalContent
                $('#reqDetailsModalContent').html(data.html);
            }
        });
    });

    let purchase_orders_table = $('#purchase_orders_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true,
        fixedHeader: true,
        ajax: {
            url: "/suppliers/purchase_orders_table",
            data: {
                company: $('#company').val(),
                from_date: $('#from_date').val(),
                until_date: $('#until_date').val(),
            }
        },
        columns: [
            { "data": 'Orden Compra' },
            { "data": 'Proveedor' },
            { "data": 'Company' },
            { "data": 'Requisición' },
            { "data": 'Fecha OC' },
            { "data": 'Subtotal', render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            { "data": 'Impuestos', render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            { "data": 'Total', render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            { "data": 'CXP Registrada' },
            { "data": 'Factura' },
            { "data": 'Estatus Factura' },
            { "data": 'Estatus' },
            { "data": 'Actions' },
        ],
        // Cuando se cree la fila
        createdRow: function (row, data, dataIndex) {
            if (data['Estatus'] === 'AFECTADO') {
                // Vamos a pinta la celda de la columna 'Estatus' de color rojo
                $('td', row).eq(11).css('background-color', '#ffb848').css('color', 'white');
            }
            if (data['Estatus'] === 'CERRADO') {
                // Vamos a pinta la celda de la columna 'Estatus' de color rojo
                $('td', row).eq(11).css('background-color', '#6610f2').css('color', 'white');
            }
        },
        initComplete: function () {
            // Índices de las columnas a filtrar
            var filterableColumns = [1, 2, 5, 9, 11]; // Columnas: Compañía, Estatus, Proveedor

            // Iterar sobre las columnas filtrables
            filterableColumns.forEach(function (columnIndex) {
                var headerCell = $('#purchase_orders_table thead tr td').eq(columnIndex);
                var filterButton = $('<a href="javascript:void(0);"><i class="mdi mdi-filter"></i></a>')
                    .css('margin-left', '5px')
                    .on('click', function () {
                        showFilterSelect(columnIndex);
                    });
                headerCell.append(filterButton);

                // Crear y ocultar el select dinámico
                var filterSelect = $('<select class="filter-select" style="display:none;"></select>')
                    .on('change', function () {
                        var selectedValue = $(this).val();
                        // Aplicar filtro en la columna correspondiente
                        purchase_orders_table.column(columnIndex).search(selectedValue || '', true, false).draw();
                        updateFilterButtonState(filterButton, selectedValue); // Actualizar el estado del botón
                        $(this).hide(); // Esconder el select después de filtrar
                    });

                headerCell.append(filterSelect);

                // Llenar el select con valores únicos de la columna correspondiente incluyendo la opción "Todos"
                var uniqueValues = purchase_orders_table.column(columnIndex).data().unique().sort();
                filterSelect.append('<option value="">Todos</option>');
                uniqueValues.each(function (value) {
                    filterSelect.append('<option value="' + value + '">' + value + '</option>');
                });


                // Mostrar el select
                function showFilterSelect(index) {
                    $('.filter-select').hide(); // Esconder todos los selects visibles
                    var select = headerCell.find('.filter-select');
                    select.show();
                    select.focus();
                }

                // Actualizar el estado del botón (agregar o quitar la clase .text-success)
                function updateFilterButtonState(button, value) {
                    if (value && value.trim() !== "") {
                        button.find('i').addClass('text-success');
                    } else {
                        button.find('i').removeClass('text-success');
                    }
                }
            });
        }
    });

    let requisition_lines_table = $('#requisition_lines_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/suppliers/requisition_lines_table/",
            "data": function (d) {
                // Agregar los parámetros del formulario a la solicitud AJAX
                d.company = $('#company').val();
                d.from = $('#from').val();
                d.until = $('#until').val();
            }
        },
        columns: [
            {
                "data": null,
                "render": function (data, type, row) {
                    return '<input type="checkbox" class="select-checkbox" id="checkbox_' + row.id_req_mat_det + '" data-id="' + row.id_req_mat + '_' + row.id_req_mat_det + '_' + row.Cantidad + '_' + row.udm + '_' + row.Costo + '">';
                },
                "orderable": false
            },
            { "data": "Empresa" },
            { "data": "id_req_mat_det" },
            { "data": "id_req_mat" },
            { "data": "FechaRequisicion" },
            { "data": "EmpleadoSolicita", "render": function (data, type, row) { return data ? data.replace(/\b\w/g, function (char) { return char.toUpperCase(); }) : ''; } },
            { "data": "Concepto", "render": function (data, type, row) { return data ? data.replace(/\b\w/g, function (char) { return char.toUpperCase(); }) : ''; } },
            { "data": "nota_desc", "render": function (data, type, row) { return data ? data.replace(/\b\w/g, function (char) { return char.toUpperCase(); }) : ''; } },
            { "data": "udm" },
            { "data": "Cantidad" },
            { "data": "Costo", render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            { "data": "CostoTotal", render: $.fn.dataTable.render.number(',', '.', 2, '$') },
            {
                "data": "Estado", render: function (data, type, row) {
                    let colores = {
                        'SIN LIBERAR': '⏳',
                        'APROBADA': '✅',
                        'LIBERADA': '🔓',
                        'EN COTIZACIÓN': '💰',
                        'EN ORDEN': '🔄',
                    };
                    return `<p class="m-0 p-0 text-nowrap">${colores[data]} ${data}</p>`;
                }
            },
            { "data": "CentroDeCostos" },
            { "data": "EmpleadoDirigido", "render": function (data, type, row) { return data ? data.replace(/\b\w/g, function (char) { return char.toUpperCase(); }) : ''; } },
            { "data": "prov1" },
            { "data": "prov2" },
            { "data": "prov3" },
            { "data": "action" },
        ],
        initComplete: function () {
            addDataTableFilter('requisition_lines_table');
        }
    });

    // Seleccionar/deseleccionar todos los checkboxes
    $('#select-all').on('click', function () {
        let rows = requisition_lines_table.rows({ 'search': 'applied' }).nodes();
        $('input[type="checkbox"]', rows).prop('checked', this.checked);
    });

    // Verificar si todos los checkboxes están seleccionados
    $('#requisition_lines_table tbody').on('change', 'input[type="checkbox"]', function () {
        if (!this.checked) {
            let el = $('#select-all').get(0);
            if (el && el.checked && ('indeterminate' in el)) {
                el.indeterminate = true;
            }
        }
    });

    // Cuando el formulario #request_quote_form se envía
    $('#request_quote_form').on('submit', function (e) {
        // Vamos a agregar un loader en el botón de submit
        $('#request_quote_submit').html(`
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Enviando...
        `).prop('disabled', true);
        $('#request_quote_cancel').prop('disabled', true);
    });
});