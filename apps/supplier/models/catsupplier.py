from django.db import models

class CatSupplier(models.Model):
    software_origin = models.CharField(max_length=100, verbose_name="Origen del software")
    company         = models.CharField(max_length=150, verbose_name="Empresa")
    external_id     = models.IntegerField(verbose_name="ID Externo")
    name            = models.CharField(max_length=200, verbose_name="Nombre", null=True, blank=True)
    rfc             = models.CharField(max_length=13, verbose_name="RFC")
    postal_code     = models.CharField(max_length=10, verbose_name="Código postal", null=True, blank=True)
    city            = models.CharField(max_length=100, verbose_name="Ciudad", null=True, blank=True)
    state           = models.CharField(max_length=100, verbose_name="Estado", null=True, blank=True)
    email           = models.EmailField(max_length=254, verbose_name="Correo electrónico", null=True, blank=True)
    bank            = models.CharField(max_length=100, verbose_name="Banco", null=True, blank=True)
    account_number  = models.CharField(max_length=50, verbose_name="Número de cuenta", null=True, blank=True)
    clabe           = models.CharField(max_length=18, verbose_name="CLABE", null=True, blank=True)
    payment_method  = models.CharField(max_length=50, verbose_name="Forma de pago", null=True, blank=True)
    currency        = models.CharField(max_length=10, verbose_name="Moneda", null=True, blank=True)
    website         = models.URLField(max_length=200, verbose_name="Sitio web", blank=True, null=True)
    notes           = models.TextField(verbose_name="Notas", blank=True, null=True)
    category        = models.CharField(max_length=100, verbose_name="Categoría", null=True, blank=True)
    active          = models.BooleanField(default=True, verbose_name="Activo")
    created_at      = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at      = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "CatProveedor"
        verbose_name_plural = "CatProveedores"

    def __str__(self):
        return self.name