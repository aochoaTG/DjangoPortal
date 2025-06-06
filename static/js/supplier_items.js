document.addEventListener('DOMContentLoaded', function () {

    // Vamos a crear la lógica para cuando se muestre el modal productModal
    const productModal = document.getElementById('productModal');
    productModal.addEventListener('show.bs.modal', event => {
        $('#productModalContent').html(''); // Limpiar el contenido del modal
        let button = $(event.relatedTarget); // Botón que abre el modal

        // Obtenemos el valor de data-action del botón que abre el modal
        let action = button.data('action');

        if (action === 'create') {
            $.ajax({
                url: "/items/productModal/",
                data: {
                    'action': action
                },
                method: 'GET',
                success: function (data) {
                    // Buscamos el elemento con el id #reqDetailsModalContent
                    $('#productModalContent').html(data.html);
                }
            });
        } else {
            id = button.data('id');
            $.ajax({
                url: "/items/productModal/",
                data: {
                    'id': id,
                    'action': action
                },
                method: 'GET',
                success: function (data) {
                    // Buscamos el elemento con el id #reqDetailsModalContent
                    $('#productModalContent').html(data.html);
                }
            });
        }


    })

    const input = document.querySelector('input[type="file"][name="image"]');

    if (input) {
        input.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const allowedExtensions = ['jpg', 'jpeg', 'png'];
                const fileExtension = file.name.split('.').pop().toLowerCase();

                if (!allowedExtensions.includes(fileExtension)) {
                    alert('❌ Solo se permiten archivos con extensión .jpg o .png');
                    this.value = '';  // Limpia el input
                }
            }
        });
    }
});