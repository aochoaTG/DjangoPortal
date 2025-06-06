"""Supplier items forms."""
from django import forms
from django.core.validators import FileExtensionValidator
from apps.supplier_items.models import Product

CURRENCY_CHOICES = [
    ('MXN', 'Peso Mexicano (MXN)'),
    ('USD', 'Dólar Estadounidense (USD)'),
]


class ProductForm(forms.ModelForm):
    """Product form."""
    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
        label="Moneda",
    )

    class Meta:
        """Meta class."""
        model = Product
        fields = [
            'name', 'type', 'description', 'price',
            'currency', 'category', 'unit', 'notes', 'is_available', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            # Nuevo campo
            'unit': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            # Nuevo campo
            'notes': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm', 'accept': 'image/jpeg, image/png'}),
        }

    image = forms.ImageField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])],
        label="Imagen"
    )

    def clean(self):
        cleaned_data = super().clean()

        is_available = cleaned_data.get('is_available')
        if is_available is None:
            raise forms.ValidationError(
                "El campo 'disponibilidad' es obligatorio.")

        return cleaned_data
