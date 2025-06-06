"""Modelos de la aplicación de ítems de proveedor."""
from django.db import models


class Category(models.Model):
    """Modelo de categoría de productos y servicios."""
    name = models.CharField(
        max_length=100,
        verbose_name="nombre",
        help_text="Nombre de la categoría"
    )
    description = models.TextField(
        verbose_name="descripción",
        help_text="Descripción de la categoría",
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="fecha de actualización"
    )

    class Meta:
        """Clase Meta."""
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ['name']

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """Modelo de producto o servicio."""
    PRODUCT_TYPES = [
        ('product', 'Producto'),
        ('service', 'Servicio'),
    ]

    UNIT_CHOICES = [
        ('unit', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('lb', 'Libra'),
        ('oz', 'Onza'),
        ('lt', 'Litro'),
        ('ml', 'Mililitro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('mm', 'Milímetro'),
        ('ft', 'Pie'),
        ('in', 'Pulgada'),
        ('pkg', 'Paquete'),
        ('box', 'Caja'),
        ('roll', 'Rollo'),
        ('dozen', 'Docena'),
        ('set', 'Juego'),
        ('pair', 'Par'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="nombre",
        help_text="Nombre del producto o servicio"
    )
    type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPES,
        verbose_name="tipo",
        help_text="Tipo de ítem (producto o servicio)"
    )
    description = models.TextField(
        verbose_name="descripción",
        help_text="Descripción detallada"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="precio",
        help_text="Precio del producto o servicio"
    )
    currency = models.CharField(
        max_length=3,
        default='MXN',
        verbose_name="moneda",
        help_text="Moneda del precio"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="categoría",
        help_text="Categoría del producto o servicio"
    )
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='unit',
        verbose_name="unidad de medida",
        help_text="Unidad de medida del producto"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="notas",
        help_text="Notas adicionales sobre el producto o servicio"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="fecha de actualización"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="disponible",
        help_text="Indica si el producto o servicio está disponible"
    )
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="imagen",
        help_text="Imagen del producto o servicio"
    )

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ['name']

    def __str__(self):
        return str(f"{self.name} ({self.get_type_display()})")
