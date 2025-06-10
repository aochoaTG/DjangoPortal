# apps/supplier/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RFQ(models.Model):
    folio = models.CharField(
        max_length=100,
        verbose_name="Folio",
        help_text="Nombre descriptivo de la solicitud de cotización"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Información adicional sobre la solicitud"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rfqs_created",
        verbose_name="Usuario creador",
        help_text="Usuario que generó la solicitud de cotización"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Momento en que se creó la RFQ"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
        help_text="Última vez que se actualizó la RFQ"
    )

    class Meta:
        verbose_name = "Solicitud de cotización"
        verbose_name_plural = "Solicitudes de cotización"

    def __str__(self):
        return self.folio