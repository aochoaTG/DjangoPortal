""" Serializers for the supplier_items app """
from django.contrib import admin
from apps.supplier_items.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Admin view for the Category model """
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin view for the Product model """
    # Agregar los nuevos campos a list_display
    list_display = ['name', 'type', 'price', 'currency',
                    'is_available', 'category', 'created_at', 'image']
    # Agregar filtros por tipo y disponibilidad de producto
    list_filter = ['type', 'category', 'is_available']
    # Buscar también por nuevos campos
    search_fields = ['name', 'description', 'currency']
    # Mostrar una vista previa de la imagen en el admin
    readonly_fields = ['image_preview']

    # Agregar una función para previsualizar la imagen en el admin
    def image_preview(self, obj):
        """ Muestra una vista previa de la imagen en el admin """
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'
