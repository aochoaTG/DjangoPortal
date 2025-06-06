document.addEventListener("DOMContentLoaded", function () {

    loadNotifications();

    function loadNotifications() {
        fetch("/notifications/get-notifications/")
            .then(response => response.json())
            .then(data => {
                const dropdown = document.getElementById("notification-dropdown");
                dropdown.innerHTML = ""; // Limpiar contenido previo

                if (data.notifications.length === 0) {
                    dropdown.innerHTML = '<li class="p-2 text-center">No hay notificaciones</li>';
                } else {
                    data.notifications.forEach(notification => {
                        const notificationItem = `
                            <a href="${notification.link}" class="link border-top notification-item" data-id="${notification.id}">
                                <div class="d-flex no-block align-items-center p-10">
                                    <span class="btn btn-${getNotificationColor(notification.notification_type)} btn-circle d-flex align-items-center justify-content-center">
                                        <i class="mdi ${getNotificationIcon(notification.notification_type)} text-white fs-4"></i>
                                    </span>
                                    <div class="ms-2">
                                        <h5 class="mb-0">${notification.title}</h5>
                                        <span class="mail-desc">${notification.description}</span>
                                    </div>
                                </div>
                            </a>`;
                        dropdown.innerHTML += notificationItem;
                    });
                    attachReadEvent();
                }
            });
    }

    function attachReadEvent() {
        document.querySelectorAll(".notification-item").forEach(item => {
            item.addEventListener("click", function () {
                const notificationId = this.getAttribute("data-id");
                fetch(`/notifications/mark-as-read/${notificationId}/`, { method: "POST", headers: { "X-CSRFToken": getCSRFToken() } })
                    .then(response => response.json())
                    .then(() => loadNotifications());
            });
        });
    }

    function getNotificationColor(type) {
        const colors = { info: "primary", warning: "warning", success: "success", error: "danger" };
        return colors[type] || "secondary";
    }

    function getNotificationIcon(type) {
        const icons = { info: "mdi-information", warning: "mdi-alert", success: "mdi-check-circle", error: "mdi-alert-circle" };
        return icons[type] || "mdi-bell";
    }

    function getCSRFToken() {
        return document.querySelector("meta[name='csrf-token']").getAttribute("content");
    }

    function updateNotificationCount() {
        fetch("/notifications/unread-count/")
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById("notification-badge");
                if (data.unread_count > 0) {
                    badge.textContent = data.unread_count > 99 ? "99+" : data.unread_count;
                    badge.classList.remove("d-none"); // Mostrar el badge si hay notificaciones
                } else {
                    badge.classList.add("d-none"); // Ocultar si no hay notificaciones
                }
            })
            .catch(error => console.error("Error al obtener las notificaciones:", error));
    }

    // Opcional: Recargar el contador cada cierto tiempo (ejemplo: cada 10 segundos)
    setInterval(updateNotificationCount, 10000);

    updateNotificationCount();
});
