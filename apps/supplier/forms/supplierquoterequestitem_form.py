from django import forms
from apps.supplier.models import SupplierQuoteRequestItem


class SupplierQuoteRequestItemForm(forms.ModelForm):
    UNIT_CHOICES = [
        ('pza', 'Pieza'),
        ('kg', 'Kilogramo'),
        ('lb', 'Libra'),
        ('lt', 'Litro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('ml', 'Mililitro'),
        ('unidad', 'Unidad'),
    ]

    unit_of_measurement = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Unidad de Medida'
    )

    CURRENCY_CHOICES = [
        ('MXN', 'Pesos'),
        ('USD', 'Dólares'),
    ]

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Moneda'
    )

    class Meta:
        model = SupplierQuoteRequestItem
        fields = ['description', 'quantity', 'unit_of_measurement', 'price', 'currency', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }
        labels = {
            'description': 'Descripción',
            'quantity': 'Cantidad',
            'unit_of_measurement': 'Unidad de Medida',
            'price': 'Precio',
            'currency': 'Moneda',
            'notes': 'Notas',
        }
        error_messages = {
            'description': {'required': 'Por favor ingrese una descripción.'},
            'quantity': {'required': 'Por favor ingrese una cantidad.', 'invalid': 'Ingrese un número válido.'},
            'price': {'required': 'Por favor ingrese un precio.', 'invalid': 'Ingrese un número válido.'},
            'unit_of_measurement': {'required': 'Seleccione una unidad de medida.'},
            'currency': {'required': 'Seleccione una moneda.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'Textarea':  # Evita sobreescribir los Textarea
                field.widget.attrs['class'] = 'form-control'
