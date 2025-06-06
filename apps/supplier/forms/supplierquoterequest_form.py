from django import forms
from apps.supplier.models import SupplierQuoteRequest, Supplier


class SupplierQuoteRequestForm(forms.ModelForm):
    supplier = forms.ModelMultipleChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.SelectMultiple(
            attrs={'class': 'form-select w-100', 'role': 'combobox', 'id': 'supplier-select'}),
        required=True
    )

    company = forms.ChoiceField(
        choices=[],
        widget=forms.Select(
            attrs={'class': 'form-select w-100', 'id': 'company-select'}),
        required=True
    )

    class Meta:
        model = SupplierQuoteRequest
        fields = ['supplier', 'company', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir opciones del campo company desde companies_processor
        self.fields['company'].choices = [
            (key, value) for key, value in {
                '1G_TGS_AHUMADA': 'Villa Ahumada',
                '1G_TGS_CASTANO': 'Castaño',
                '1G_TGS_CLARA': 'Clara',
                '1G_TGS_GASOMEX': 'Gasomex',
                '1G_TGS_INMO': 'INMO',
                '1G_TGS_JARUDO': 'Jarudo',
                '1G_TGS_PETROTAL': 'Petrotal',
                '1G_TGS_PICACHOS': 'Picachos',
                '1G_TGS_SERVICIOSYC': 'SYC',
                '1G_TGS_VENTANAS': 'VENTANAS',
                '1G_TGS_ZAID': 'ZAID',
                '1G_TOTALGAS': 'Diaz Gas',
                '1G_TOTALGAS_EC': 'EC',
                '1G_TOTALGAS_MCP': '1G_TOTALGAS_MCP',
                '1G_TOTALGAS_TSA': 'TSA',
                '1G_TGS_FORMULAGAS': 'FG',
                
            }.items()
        ]

    def save(self, commit=True):
        """Crea un registro diferente por cada proveedor seleccionado."""
        instances = []
        company = self.cleaned_data['company']
        notes = self.cleaned_data['notes']

        for supplier in self.cleaned_data['supplier']:
            instance = SupplierQuoteRequest(
                supplier=supplier, company=company, notes=notes)
            if commit:
                instance.save()
            instances.append(instance)

        return instances  # Retorna una lista de los registros creados

class SupplierQuoteRequestCreateForm(forms.Form):
    """Formulario para seleccionar múltiples proveedores sin estar ligado a un modelo"""
    supplier = forms.ModelMultipleChoiceField(
        queryset=Supplier.objects.all(),
        label="Proveedor(es)",
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select w-100',
                'role': 'combobox',
                'id': 'supplier-select'
            }
        ),
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    
    company = forms.ChoiceField(
        label="Compañía",
        choices=[
            ('1G_TOTALGAS', 'Diaz Gas'),
            ('1G_TGS_AHUMADA', 'Villa Ahumada'),
            ('1G_TGS_CASTANO', 'Castaño'),
            ('1G_TGS_CLARA', 'Clara'),
            ('1G_TGS_GASOMEX', 'Gasomex'),
            ('1G_TGS_INMO', 'INMO'),
            ('1G_TGS_JARUDO', 'Jarudo'),
            ('1G_TGS_PETROTAL', 'Petrotal'),
            ('1G_TGS_PICACHOS', 'Picachos'),
            ('1G_TGS_SERVICIOSYC', 'SYC'),
            ('1G_TGS_VENTANAS', 'VENTANAS'),
            ('1G_TGS_ZAID', 'ZAID'),
            ('1G_TOTALGAS_EC', 'EC'),
            ('1G_TOTALGAS_MCP', '1G_TOTALGAS_MCP'),
            ('1G_TOTALGAS_TSA', 'TSA'),
            ('1G_TGS_FORMULAGAS', 'FormulaGas'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-select w-100', 'id': 'company-select'}
        ),
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    notes = forms.CharField(
        label="Notas",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        required=False
    )

class SupplierQuoteRequestModelForm(forms.ModelForm):
    class Meta:
        model = SupplierQuoteRequest
        fields = ['supplier', 'company', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-select w-100',
                'id': 'supplier-select',
            }),
            'company': forms.Select(attrs={
                'class': 'form-select w-100',
                'id': 'company-select',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1,
            }),
        }
        labels = {
            'supplier': 'Proveedor',
            'company': 'Compañía',
            'notes': 'Notas',
        }


# forms.py
class SupplierQuoteRequestEditForm(forms.Form):
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        label="Proveedor",
        widget=forms.Select(
            attrs={'class': 'form-select w-100', 'id': 'supplier-select'}
        ),
        required=True
    )
    company = forms.ChoiceField(
        label="Compañía",
        choices=[
            ('1G_TOTALGAS', 'Diaz Gas'),
            ('1G_TGS_AHUMADA', 'Villa Ahumada'),
            ('1G_TGS_CASTANO', 'Castaño'),
            ('1G_TGS_CLARA', 'Clara'),
            ('1G_TGS_GASOMEX', 'Gasomex'),
            ('1G_TGS_INMO', 'INMO'),
            ('1G_TGS_JARUDO', 'Jarudo'),
            ('1G_TGS_PETROTAL', 'Petrotal'),
            ('1G_TGS_PICACHOS', 'Picachos'),
            ('1G_TGS_SERVICIOSYC', 'SYC'),
            ('1G_TGS_VENTANAS', 'VENTANAS'),
            ('1G_TGS_ZAID', 'ZAID'),
            ('1G_TOTALGAS_EC', 'EC'),
            ('1G_TOTALGAS_MCP', '1G_TOTALGAS_MCP'),
            ('1G_TOTALGAS_TSA', 'TSA'),
            ('1G_TGS_FORMULAGAS', 'FormulaGas'),
        ],
        widget=forms.Select(
            attrs={'class': 'form-select w-100', 'id': 'company-select'}
        ),
        required=True,
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    notes = forms.CharField(
        label="Notas",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        required=False
    )
