from django.db import models
from django.contrib.auth.models import User
from .supplierquoterequest import SupplierQuoteRequest
from .supplier import Supplier

class SupplierQuote(models.Model):
    """Modelo para almacenar las cotizaciones enviadas por los proveedores."""
    
    STATUS_CHOICES = [
        ('ENVIADA', 'Enviada'),
        ('ACEPTADA', 'Aceptada'),
        ('RECHAZADA', 'Rechazada'),
        ('VENCIDA', 'Vencida'),
    ]
    
    id = models.AutoField(
        primary_key=True,
        help_text="Identificador único para cada cotización del proveedor",
        verbose_name="ID"
    )
    quote_request = models.ForeignKey(
        SupplierQuoteRequest,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name='Solicitud de Cotización',
        help_text="Solicitud de cotización a la que responde esta cotización. Se eliminará si se elimina la solicitud"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='quotes',
        db_column='supplier_id',
        verbose_name='Proveedor',
        help_text="Proveedor que envía la cotización. Se eliminarán todas las cotizaciones si se elimina el proveedor"
    )
    quote_number = models.CharField(
        max_length=100,
        verbose_name='Número de Cotización',
        help_text="Número o referencia de la cotización asignado por el proveedor",
        null=True,
        blank=True
    )
    validity_date = models.DateField(
        verbose_name='Fecha de Validez',
        help_text="Fecha hasta la cual es válida la cotización",
        null=True,
        blank=True
    )
    delivery_time = models.CharField(
        max_length=100,
        verbose_name='Tiempo de Entrega',
        help_text="Tiempo estimado de entrega ofrecido por el proveedor",
        null=True,
        blank=True
    )
    payment_terms = models.CharField(
        max_length=200,
        verbose_name='Condiciones de Pago',
        help_text="Condiciones de pago ofrecidas por el proveedor",
        null=True,
        blank=True
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Subtotal',
        help_text="Subtotal de la cotización sin impuestos",
        default=0
    )
    tax = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Impuestos',
        help_text="Monto total de impuestos aplicados a la cotización",
        default=0
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Total',
        help_text="Monto total de la cotización incluyendo impuestos",
        default=0
    )
    currency = models.CharField(
        max_length=3,
        choices=[('MXN', 'Pesos'), ('USD', 'Dólares'), ('EUR', 'Euros')],
        default='MXN',
        verbose_name='Moneda',
        help_text="Moneda en la que se cotiza. Puede ser MXN (Pesos), USD (Dólares) o EUR (Euros)"
    )
    
    # Archivos adjuntos para cotizaciones en PDF o DOCX
    quote_file_1 = models.FileField(
        upload_to='supplier_quotes/',
        null=True,
        blank=True,
        verbose_name='Archivo de Cotización 1',
        help_text="Primer archivo adjunto de la cotización (PDF o DOCX)"
    )
    quote_file_2 = models.FileField(
        upload_to='supplier_quotes/',
        null=True,
        blank=True,
        verbose_name='Archivo de Cotización 2',
        help_text="Segundo archivo adjunto de la cotización (opcional, PDF o DOCX)"
    )

    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Notas',
        help_text="Notas o comentarios adicionales sobre la cotización"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='ENVIADA',
        verbose_name='Estatus',
        help_text="Estado actual de la cotización. Por defecto es 'ENVIADA'"
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Recepción',
        help_text="Fecha y hora en que se recibió la cotización. Se establece automáticamente"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización',
        help_text="Fecha y hora de la última actualización de la cotización. Se actualiza automáticamente"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación',
        help_text="Fecha y hora de creación de la cotización. Se establece automáticamente"
    )

    class Meta:
        db_table = 'supplier_quote'
        verbose_name = 'Cotización de Proveedor'
        verbose_name_plural = 'Cotizaciones de Proveedores'
        
    def __str__(self):
        return f"Cotización {self.quote_number} de {self.supplier.company_name}"
        
    def save(self, *args, **kwargs):
        """Actualiza automáticamente los totales antes de guardar."""        
        super().save(*args, **kwargs)
