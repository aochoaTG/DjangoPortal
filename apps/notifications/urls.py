"""URLs para la app de notificaciones."""
from django.urls import path
from .views import get_notifications, mark_notification_as_read, unread_notifications_count

urlpatterns = [
    path('get-notifications/', get_notifications, name='get_notifications'),
    path('mark-as-read/<int:notification_id>/',
         mark_notification_as_read, name='mark_notification_as_read'),
    path('unread-count/', unread_notifications_count,
         name='unread_notifications_count'),
]
