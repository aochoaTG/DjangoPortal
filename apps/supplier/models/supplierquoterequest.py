from django.db import models
from django.contrib.auth.models import User
from .supplier import Supplier
# Vamos a importar el modelo RFQ desde su ubicación
from .requestforquote import RFQ

class SupplierQuoteRequest(models.Model):
    id = models.AutoField(
        primary_key=True,
        help_text="Identificador único para cada solicitud de cotización"
    )
    rfq = models.ForeignKey(
        RFQ,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name='RFQ asociada',
        help_text='Solicitud de cotización (cabecera) a la que pertenece este registro',
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='quote_requests',
        db_column='supplier_id',
        verbose_name='Proveedor',
        help_text="Proveedor al que se le solicita la cotización. Se eliminarán todas las solicitudes si se elimina el proveedor"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='supplier_quote_requests',
        db_column='user_id',
        verbose_name='Usuario',
        help_text="Usuario que genera la solicitud de cotización. Se eliminarán todas las solicitudes si se elimina el usuario"
    )
    company = models.CharField(
        max_length=100,
        verbose_name='Empresa',
        help_text="Nombre de la empresa para la que se solicita la cotización"
    )
    viewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Visualización',
        help_text="Fecha y hora en que el proveedor visualizó la solicitud por primera vez"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Notas',
        help_text="Notas o comentarios adicionales sobre la solicitud de cotización"
    )
    status = models.CharField(
        max_length=50,
        null=True,
        default='PENDIENTE',
        verbose_name='Estatus',
        help_text="Estado actual de la solicitud. Por defecto es 'PENDIENTE'"
    )
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Actualización',
        help_text="Fecha y hora de la última actualización de la solicitud"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación',
        help_text="Fecha y hora en que se creó la solicitud. Se establece automáticamente"
    )

    class Meta:
        db_table = 'supplier_quote_request'
        verbose_name = 'Solicitud de Cotización del Proveedor'
        verbose_name_plural = 'Solicitudes de Cotización de Proveedores'

    def __str__(self):
        return f"Solicitud de {self.company} para {self.supplier.company_name}"