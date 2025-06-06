from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentType(models.Model):
    """Modelo para definir los tipos de documentos que pueden subir los proveedores"""
    name = models.CharField(max_length=255, verbose_name=_("Nombre"))
    code = models.CharField(max_length=100, unique=True, verbose_name=_("Código"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Descripción"))
    is_required = models.BooleanField(default=False, verbose_name=_("Es obligatorio"))
    upload_path = models.CharField(
        max_length=255, 
        verbose_name=_("Ruta de subida"),
        help_text=_("Ruta relativa donde se almacenarán los archivos")
    )
    
    class Meta:
        verbose_name = _("Tipo de documento")
        verbose_name_plural = _("Tipos de documentos")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SupplierDocument(models.Model):
    """Modelo para almacenar documentos asociados a proveedores"""
    STATUS_CHOICES = [
        ('pending', _('Pendiente')),
        ('approved', _('Aprobado')),
        ('rejected', _('Rechazado')),
    ]
    
    supplier = models.ForeignKey(
        'Supplier', 
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_("Proveedor")
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name='supplier_documents',
        verbose_name=_("Tipo de documento")
    )
    file = models.FileField(
        upload_to='supplier_documents/',
        verbose_name=_("Archivo")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_("Estado")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de carga")
    )
    reviewed_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Fecha de revisión")
    )
    rejection_reason = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Motivo de rechazo")
    )
    
    class Meta:
        verbose_name = _("Documento de proveedor")
        verbose_name_plural = _("Documentos de proveedores")
        unique_together = ['supplier', 'document_type']
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.supplier} - {self.document_type}"
    
    def save(self, *args, **kwargs):
        """Personaliza la ruta de carga basada en el tipo de documento"""
        if self.document_type and not self.id:  # Solo al crear un nuevo documento
            upload_path = self.document_type.upload_path
            if upload_path:
                self.file.field.upload_to = f'supplier_files/{upload_path}/'
        
        super().save(*args, **kwargs)


# Datos iniciales para los tipos de documentos (puedes usar esto en una migración)
DOCUMENT_TYPES = [
    {
        'name': 'Constancia de Situación Fiscal',
        'code': 'fiscal_situation',
        'description': 'Archivo de la constancia de situación fiscal',
        'is_required': True,
        'upload_path': 'fiscal_situation'
    },
    {
        'name': 'Comprobante de Domicilio',
        'code': 'address_proof',
        'description': 'Archivo del comprobante de domicilio',
        'is_required': True,
        'upload_path': 'address_proof'
    },
    {
        'name': 'Carátula Bancaria',
        'code': 'bank_statement',
        'description': 'Archivo de la carátula bancaria',
        'is_required': True,
        'upload_path': 'bank_statement'
    },
    {
        'name': 'Opinión Positiva del SAT',
        'code': 'sat_positive_opinion',
        'description': 'Archivo de la opinión positiva del SAT',
        'is_required': True,
        'upload_path': 'sat_positive_opinion'
    },
    {
        'name': 'Acta Constitutiva',
        'code': 'incorporation_act',
        'description': 'Archivo del acta constitutiva',
        'is_required': False,
        'upload_path': 'incorporation_act'
    },
    {
        'name': 'Poder Legal',
        'code': 'legal_power',
        'description': 'Archivo del poder legal',
        'is_required': False,
        'upload_path': 'legal_power'
    },
    {
        'name': 'Identificación',
        'code': 'identification',
        'description': 'Archivo de identificación oficial',
        'is_required': True,
        'upload_path': 'identification'
    },
    {
        'name': 'Opinión del IMSS',
        'code': 'imss_opinion',
        'description': 'Archivo de la opinión del IMSS',
        'is_required': False,
        'upload_path': 'imss_opinion'
    },
    {
        'name': 'Opinión del INFONAVIT',
        'code': 'infonavit_opinion',
        'description': 'Archivo de la opinión del INFONAVIT',
        'is_required': False,
        'upload_path': 'infonavit_opinion'
    },
    {
        'name': 'Solicitud Alta de Proveedor',
        'code': 'supplier_registration_request',
        'description': 'Archivo de la solicitud de alta de proveedor',
        'is_required': True,
        'upload_path': 'supplier_registration_request'
    },
    {
        'name': 'REPSE',
        'code': 'repse',
        'description': 'Archivo del REPSE',
        'is_required': False,
        'upload_path': 'repse'
    },
    {
        'name': 'Acta de Confidencialidad',
        'code': 'confidentiality_agreement',
        'description': 'Archivo del acta de confidencialidad',
        'is_required': False,
        'upload_path': 'confidentiality_agreement'
    },
    {
        'name': 'F-06-01-05 Curso de Inducción',
        'code': 'induction_course',
        'description': 'Archivo del curso de inducción',
        'is_required': False,
        'upload_path': 'induction_course'
    },
]