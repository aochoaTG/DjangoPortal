$(document).ready(function () {
    let staffusers_table = $('#staffusers_table').DataTable(
        {
            colReorder: true,
            pageLength: 10,
            dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
            paging: true, // Si quieres mantener la paginación
            info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
            buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
            orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
            fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
            ajax: {
                "url": "/accounts/staffusers_table",
            },
            columns: [
                { 'data': 'id' },
                { 'data': 'username' },
                { 'data': 'name' },
                { 'data': 'superuser' },
                { 'data': 'email' },
                { 'data': 'status' },
                { 'data': 'last_login' },
                { 'data': 'actions' },
            ],
            initComplete: function () {
                addDataTableFilter('staffusers_table');
            }
        }
    );

    let catSuppliersUsersTable = $('#catSuppliersUsersTable').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/accounts/show_table_catsuppliers",
        },
        columns: [
            { "data": "id" },
            { "data": "name" },
            { "data": "rfc" },
            { "data": "postal_code" }, // Permiso CRE
            { "data": "city" },
            { "data": "state" },
            { "data": "email" },
            { "data": "bank" },
            { "data": "account_number" },
            { "data": "clabe" },
            { "data": "payment_method" },
            { "data": "currency" },
            { "data": "website" },
            { "data": "category" },
            { "data": "active" },
            { "data": "notes" },
            { "data": "digital_file" },
            { "data": "actions" },
        ],
        initComplete: function () {
            addDataTableFilter('catSuppliersUsersTable');
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


    let suppliersUsersTable = $('#suppliersUsersTable').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/accounts/show_suppliers_table",
        },
        columns: [
            { "data": "id" },
            { "data": "username" },
            { "data": "name" },
            { "data": "superuser" }, // Permiso CRE
            { "data": "email" },
            { "data": "is_active" },
            { "data": "last_login" },
            { "data": "actions" },
        ],
        initComplete: function () {
            addDataTableFilter('suppliersUsersTable');
        }
    });
});