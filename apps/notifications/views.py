"""Vistas para el manejo de notificaciones."""
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from apps.notifications.models import Notification


@login_required
def get_notifications(request):
    """Retorna las notificaciones no leídas del usuario en formato JSON."""
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-priority', '-created_at')

    data = [
        {
            "id": n.id,
            "title": n.title,
            "description": n.description,
            "link": n.link,
            "notification_type": n.notification_type,
            "priority": n.priority,
            "created_at": n.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_by": n.created_by.get_full_name() or n.created_by.username
        }
        for n in notifications
    ]

    return JsonResponse({"notifications": data})


@login_required
def mark_notification_as_read(request, notification_id):
    """Marca una notificación como leída."""
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user  # Cambiado de user a recipient
    )
    notification.mark_as_read()
    return JsonResponse({"message": "Notificación marcada como leída"})


@login_required
def unread_notifications_count(request):
    """Retorna la cantidad de notificaciones no leídas del usuario."""
    unread_count = Notification.objects.filter(recipient=request.user.id,is_read=False).count()
    return JsonResponse({"unread_count": unread_count})
