$(document).ready(function () {
    let quote_requests_table = $('#quote_requests_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/suppliers/quote_requests_table/"
        },
        columns: [
            { "data": "id" },
            { "data": "supplier" },
            { "data": "user" },
            { "data": "company" },
            { "data": "notes" },
            { "data": "status" },
            { "data": "created_at" },
            { "data": "lines" },
            { "data": "qty_requested" },
            { "data": "price_total", "render": $.fn.dataTable.render.number(',', '.', 2, '$') },
            { "data": "actions" },
        ],
        createdRow: function (row, data, dataIndex) {
            if (data.status === "VISTA") {
                $('td', row).eq(5).addClass('bg-warning');
            }
            if (data.status === "PENDIENTE") {
                $('td', row).eq(5).addClass('bg-info text-light');
            }
            if (data.status === "RECHAZADA") {
                $('td', row).eq(5).addClass('bg-danger text-light');
            }

        },
        initComplete: function () {
            addDataTableFilter('quote_requests_table');
        }
    });

    let quotes_table = $('#quotes_table').DataTable({
        colReorder: true,
        pageLength: 25,
        dom: 'tip', // Muestra la tabla (t), la información (i), y la paginación (p)
        paging: true, // Si quieres mantener la paginación
        info: true, // Si quieres mostrar la información de "Mostrando X a Y de Z entradas"
        buttons: ['copy', 'excel'], // Si quieres mostrar los botones de copiar, excel y pdf
        orderCellsTop: true, // Hace que solo la primera fila del thead controle el ordenamiento
        fixedHeader: true,   // Mantiene los filtros visibles cuando haces scroll
        ajax: {
            "url": "/suppliers/quotes_table/"
        },
        columns: [
            { "data": "id" },
            { "data": "supplier" },
            { "data": "user" },
            { "data": "company" },
            { "data": "notes" },
            { "data": "status" },
            { "data": "created_at" },
            { "data": "lines" },
            { "data": "qty_requested" },
            { "data": "price_total" },
            { "data": "actions" },
        ],
        initComplete: function () {
            addDataTableFilter('quotes_table');
        }
    });


});

function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}

function reject_request(request_id) {
    // Vamos a recibir el id de la solicitud de cotización y a lanzar un confirm
    Swal.fire({
        title: "¿Estás segur@?",
        text: "Al rechazar esta solicitud no podras participar en la cotización",
        icon: "warning",
        showCancelButton: true,
        // Vamos a cambiar el texto del boton de cancelar
        cancelButtonText: "Cancelar",
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Sí, rechazar"
    }).then((result) => {
        if (result.isConfirmed) {
            // Vamos a hacer un ajax para rechazar la solicitud
            $.ajax({
                url: "/suppliers/reject_request/" + request_id + "/",
                type: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken() // Agregamos el CSRF token
                },
                success: function (data) {
                    if (data.status === "success") {
                        Swal.fire({
                            title: "¡Solicitud rechazada!",
                            text: "Se notificará al cliente que has rechazado la solicitud",
                            icon: "success"
                        }).then(() => {
                            $('#quote_requests_table').DataTable().ajax.reload();
                        });
                    } else {
                        Swal.fire({
                            title: "¡Error!",
                            text: "Hubo un error al rechazar la solicitud",
                            icon: "error"
                        });
                    }
                },
                error: function () {
                    Swal.fire({
                        title: "¡Error!",
                        text: "No se pudo conectar con el servidor",
                        icon: "error"
                    });
                }
            });

            Swal.fire({
                title: "¡Solicitud rechazada!",
                text: "Se notificará al cliente que has rechazado la solicitud",
                icon: "success"
            });
        }
    });
}

