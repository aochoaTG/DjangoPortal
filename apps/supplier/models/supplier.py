import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class Supplier(models.Model):
    """ Modelo de proveedor """
    class SupplierType(models.TextChoices):
        PRODUCT = 'product', 'Productos'
        SERVICE = 'service', 'Servicios'
        PRODUCTSERVICE = 'product_service', 'Productos y Servicios'

    class TaxRegime(models.TextChoices):
        """ Régimen Fiscal """
        INDIVIDUAL = 'individual', 'Persona Física'
        CORPORATION = 'corporation', 'Persona Moral'
        RESICO = 'resico', 'Régimen Simplificado de Confianza'

    class Currency(models.TextChoices):
        """ Monedas """
        MXN = 'MXN', 'Pesos Mexicanos'
        USD = 'USD', 'Dólares Americanos'
        EUR = 'EUR', 'Euros'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="supplier_profile",
        verbose_name="Usuario",
        help_text="Usuario asociado al proveedor"
    )
    company_name = models.CharField(
        max_length=150,
        verbose_name="Nombre de la Empresa",
        help_text="Razón social o nombre comercial"
    )
    rfc = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="RFC",
        help_text="Registro Federal de Contribuyentes (RFC) de la empresa"
    )
    address = models.TextField(
        verbose_name="Dirección Fiscal",
        help_text="Dirección fiscal completa de la empresa"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Teléfono",
        help_text="Teléfono principal de la empresa"
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="Correo Electrónico",
        help_text="Correo electrónico de contacto"
    )
    contact_person = models.CharField(
        max_length=100,
        verbose_name="Persona de Contacto",
        help_text="Nombre de la persona encargada del contacto"
    )
    contact_phone = models.CharField(
        max_length=10,
        blank=True, null=True,
        verbose_name="Teléfono de Contacto",
        help_text="Número de teléfono de contacto, 10 dígitos"
    )
    supplier_type = models.CharField(
        max_length=20,
        choices=SupplierType.choices,
        verbose_name="Tipo de Proveedor",
        help_text="Especifica si provee productos, servicios o ambos"
    )
    tax_regime = models.CharField(
        max_length=20,
        choices=TaxRegime.choices,
        verbose_name="Régimen Fiscal",
        help_text="Régimen fiscal bajo el cual tributa"
    )

    # 📌 Nuevos Campos Bancarios
    bank_name = models.CharField(
        max_length=100,
        verbose_name="Banco",
        help_text="Nombre del banco para recepción de pagos"
    )
    account_number = models.CharField(
        max_length=20,
        verbose_name="Número de Cuenta",
        help_text="Número de cuenta bancaria"
    )
    clabe = models.CharField(
        max_length=18,
        verbose_name="CLABE Interbancaria",
        help_text="CLABE interbancaria de 18 dígitos"
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        verbose_name="Moneda",
        help_text="Moneda en la que se realizarán los pagos"
    )

    # Agregamos el nuevo campo con un UUID único, sin el default
    verification_token = models.UUIDField(default=uuid.uuid4, unique=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha en que se creó el proveedor"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización",
        help_text="Fecha de la última actualización del proveedor"
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['company_name']

    def __str__(self):
        return str(self.company_name)

# Signal para generar el UUID antes de guardar
@receiver(pre_save, sender=Supplier)
def set_verification_token(sender, instance, **kwargs):
    if not instance.verification_token:
        instance.verification_token = uuid.uuid4()
