"""Modelos de la aplicación de notificaciones."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_default_user():
    """Obtiene el primer superadministrador del sistema."""
    return User.objects.filter(is_superuser=True).first()


class Notification(models.Model):
    """Modelo de notificación."""
    NOTIFICATION_TYPES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('success', 'Éxito'),
        ('error', 'Error'),
    ]

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_notifications",
        verbose_name="Creado por",
        help_text="Usuario que crea la notificación (por defecto el primer superadministrador)",
        default=get_default_user
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_notifications",
        verbose_name="Destinatario",
        help_text="Usuario que recibe la notificación"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título corto y descriptivo de la notificación"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción",
        help_text="Descripción detallada de la notificación (opcional)"
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace",
        help_text="URL relacionada con la notificación (opcional)"
    )

    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name="Tipo de Notificación",
        help_text="Categoría de la notificación: información, advertencia, éxito o error"
    )

    priority = models.IntegerField(
        default=0,
        verbose_name="Prioridad",
        help_text="Nivel de prioridad de la notificación. Mayor número indica mayor prioridad"
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Expiración",
        help_text="Fecha y hora en que la notificación dejará de ser válida (opcional)"
    )

    action_text = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Texto del botón de acción",
        help_text="Texto que se mostrará en el botón de acción de la notificación (opcional)"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Leído",
        help_text="Indica si la notificación ha sido leída por el usuario"
    )

    viewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Visualización",
        help_text="Fecha y hora en que la notificación fue vista por primera vez"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que se creó la notificación"
    )

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        indexes = [
            models.Index(fields=['created_by', '-created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.title} - {self.recipient.username}"

    def mark_as_read(self):
        """Marca la notificación como leída."""
        self.is_read = True
        self.viewed_at = timezone.now()
        self.save()

    @property
    def is_expired(self):
        """Indica si la notificación ha expirado."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
