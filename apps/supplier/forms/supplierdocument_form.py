# forms.py
from django import forms
from django.core.exceptions import ValidationError
from apps.supplier.models import SupplierDocument, DocumentType

class SupplierDocumentForm(forms.ModelForm):
    """Formulario para cargar un documento individual de proveedor"""
    
    class Meta:
        model = SupplierDocument
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'fileHelp'
            }),
        }
    
    def __init__(self, *args, document_type=None, supplier=None, instance=None, **kwargs):
        self.document_type = document_type
        self.supplier = supplier
        
        if instance is None and document_type and supplier:
            # Intentar obtener un documento existente
            instance = SupplierDocument.objects.filter(
                supplier=supplier,
                document_type=document_type
            ).first()
        
        super().__init__(*args, instance=instance, **kwargs)
        
        # Agregar mensaje de ayuda dinámico basado en el tipo de documento
        if document_type:
            self.fields['file'].help_text = document_type.description
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file and self.document_type and self.document_type.is_required and not self.instance.pk:
            raise ValidationError(f"El documento '{self.document_type.name}' es obligatorio.")
        
        # Aquí podrías agregar validaciones adicionales como tamaño máximo,
        # tipos de archivo permitidos, etc.
        
        return file
    
    def save(self, commit=True):
        document = super().save(commit=False)
        
        if not document.pk:  # Es un nuevo documento
            document.supplier = self.supplier
            document.document_type = self.document_type
            document.status = 'pending'
        
        if commit:
            document.save()
        
        return document