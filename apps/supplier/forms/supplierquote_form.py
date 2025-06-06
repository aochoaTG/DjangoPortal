from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from apps.supplier.models import SupplierQuote

class SupplierQuoteForm(forms.ModelForm):
    class Meta:
        model = SupplierQuote
        # Campos visibles para el proveedor
        fields = [
            'quote_number', 'validity_date', 'delivery_time', 'payment_terms',
            'subtotal', 'tax', 'total', 'currency',
            'quote_file_1', 'quote_file_2', 'notes',
        ]
        widgets = {
            'validity_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'delivery_time': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5 días hábiles', 'class': 'form-control'}),
            'payment_terms': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'quote_file_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'quote_file_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'quote_number': "Número de Cotización",
            'validity_date': "Fecha de Validez",
            'delivery_time': "Tiempo de Entrega",
            'payment_terms': "Condiciones de Pago",
            'subtotal': "Subtotal",
            'tax': "Impuestos",
            'total': "Total",
            'currency': "Moneda",
            'quote_file_1': "Archivo de Cotización 1",
            'quote_file_2': "Archivo de Cotización 2",
            'notes': "Notas",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.label_class = 'fw-bold'
        self.helper.form_tag = True
        # self.helper.add_input(Submit('submit', 'Guardar Cotización'))

        self.helper.layout = Layout(
            Row(
                Column('quote_number', css_class='col-md-4'),
                Column('validity_date', css_class='col-md-4'),
                Column('delivery_time', css_class='col-md-4'),
            ),
            Row(
                Column('payment_terms', css_class='col-md-12'),
            ),
            Row(
                Column('subtotal', css_class='col-md-4'),
                Column('tax', css_class='col-md-4'),
                Column('total', css_class='col-md-4'),
            ),
            Row(
                Column('currency', css_class='col-md-4'),
                Column('quote_file_1', css_class='col-md-4'),
                Column('quote_file_2', css_class='col-md-4'),
            ),
            'notes'
        )
        for field in self.fields.values():
            field.help_text = ''

    def clean(self):
        cleaned_data = super().clean()
        file1 = cleaned_data.get("quote_file_1")
        file2 = cleaned_data.get("quote_file_2")

        if not file1 and not file2:
            raise forms.ValidationError("Debes adjuntar al menos un archivo de cotización (PDF o DOCX).")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance