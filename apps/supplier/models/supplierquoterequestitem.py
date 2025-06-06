"""Modelo de los ítems de una solicitud de cotización a proveedores."""
from django.db import models
from .supplierquoterequest import SupplierQuoteRequest


class SupplierQuoteRequestItem(models.Model):
    """ Modelo de los ítems de una solicitud de cotización a proveedores. """
    CURRENCY_CHOICES = [
        ('MXN', 'Pesos'),
        ('USD', 'Dólares'),
        ('EUR', 'Euros'),
    ]

    id = models.AutoField(
        primary_key=True,
        help_text="Identificador único para cada ítem de la solicitud"
    )
    quote_request = models.ForeignKey(
        SupplierQuoteRequest,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Solicitud de Cotización',
        help_text="Solicitud de cotización a la que pertenece este ítem. Se eliminará si se elimina la solicitud"
    )
    requisition_id = models.IntegerField(
        verbose_name='ID de Requisición',
        help_text="Identificador de la requisición asociada a este ítem",
        null=True,
        blank=True,
        default=0
    )
    requisition_line = models.IntegerField(
        verbose_name='Línea de Requisición',
        help_text="Número de línea de la requisición asociada a este ítem",
        null=True,
        blank=True,
        default=0
    )

    description = models.TextField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name='Descripción',
        help_text="Descripción del ítem solicitado"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Cantidad',
        help_text="Cantidad solicitada del ítem. Permite hasta 2 decimales"
    )
    unit_of_measurement = models.CharField(
        null=True,
        blank=True,
        max_length=50,
        verbose_name='Unidad de Medida',
        help_text="Unidad de medida en la que se solicita el ítem"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Unitario',
        help_text="Precio unitario del ítem. Permite hasta 2 decimales"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='MXN',
        verbose_name='Moneda',
        help_text="Moneda en la que se cotiza el ítem. Puede ser MXN (Pesos), USD (Dólares) o EUR (Euros)"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total',
        help_text="Total calculado automáticamente (cantidad × precio). Permite hasta 2 decimales"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Notas',
        help_text="Notas o comentarios adicionales sobre este ítem específico"
    )

    class Meta:
        """Opciones del modelo."""
        db_table = 'supplier_quote_request_item'
        verbose_name = 'Detalle de Solicitud de Cotización'
        verbose_name_plural = 'Detalles de Solicitudes de Cotización'

    def __str__(self):
        return f"Ítem en la solicitud {self.quote_request.id} - Cantidad: {self.quantity}"

    def save(self, *args, **kwargs):
        """Calcula automáticamente el total antes de guardar."""
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
