// Habilitar tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

$('#customSearch').on('keyup', function () {
    var tableId = $(this).data('table-id');  // Obtén el ID de la tabla desde el atributo 'data-table-id'
    var table = $(tableId).DataTable();      // Accede a la tabla correspondiente
    table.search(this.value).draw();         // Filtra la tabla según el valor del input
});

function setTableLength(tableSelector, length) {
    var table = $(tableSelector).DataTable(); // Selecciona la tabla
    table.page.len(length).draw(); // Cambia la cantidad de entradas y redibuja
}

function exportExcel(tableSelector) {
    var table = $(tableSelector).DataTable();
    table.button('.buttons-excel').trigger(); // Llama al botón interno de DataTables
}

function copyTable(tableSelector) {
  var table = $(tableSelector).DataTable();
  table.button('.buttons-copy').trigger(); // Llama al botón interno de copiado
}

function refreshTable(tableSelector) {
    var table = $(tableSelector).DataTable();
    // Vamos a limpiar la tabla
    table.clear().draw();
    table.ajax.reload(); // Recarga los datos desde la fuente AJAX
}

$('#passwordModal').on('show.bs.modal', function (event) {
    // Vamos a capturar el id que viene en el atributo data-id
    var button = $(event.relatedTarget);
    var id = button.data('id');

    // Vamos a crear dinámicamente el action del formulario
    $('#password_change_form').attr('action', '/accounts/password_change_modal/' + id + '/');

    // Vamos a mandar a pedir los datos del formulario por medio de AJAX
    $.ajax({
        url: '/accounts/password_change_modal/' + id,
        method: 'GET',
        success: function(data) {
            console.log(data);
            // Buscamos el formulario co el id #password_change_form
            $('#password_change_form').html(data.html);
        }
    });
});

$('#profileModal').on('show.bs.modal', function (event) {
    // Vamos a capturar el id que viene en el atributo data-id
    var button = $(event.relatedTarget);
    var id = button.data('id');

    // Vamos a crear dinámicamente el action del formulario
    $('#profile_change_form').attr('action', '/accounts/profile_modal/' + id + '/');

    // Vamos a mandar a pedir los datos del formulario por medio de AJAX
    $.ajax({
        url: '/accounts/profile_modal/' + id,
        method: 'GET',
        success: function(data) {
            console.log(data);
            // Buscamos el formulario co el id #profile_change_form
            $('#profile_change_form').html(data.html);
        }
    });
});

function addDataTableFilter(tableId) {
    const tableSelector = tableId.startsWith('#') ? tableId : '#' + tableId; // Verificamos que el ID incluya el #

    const dataTableInstance = $(tableSelector).DataTable(); // Obtenemos la instancia de DataTable directamente

    $(tableSelector + ' thead').append( // Clonar el thead y agregar los inputs de filtrado
        $(tableSelector + ' thead tr').clone().addClass('filter')
    );

    $(tableSelector + ' thead tr.filter th').each(function() { // Agregar los inputs de filtrado
        $(this).addClass('text-center p-0');
        $(this).html('<input type="text" class="form-control form-control-sm"/>');
    });

    $(tableSelector + ' thead tr.filter th input').on('keyup change', function() { // Agregar el evento de filtrado a los inputs
        let index = $(this).parent().index();
        dataTableInstance.column(index).search(this.value).draw();
    });
}