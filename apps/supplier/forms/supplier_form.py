from django import forms
from apps.supplier.models import Supplier
from django.core.exceptions import ValidationError


# class SupplierForm(forms.ModelForm):
#     class Meta:
#         model = Supplier
#         fields = ['fiscal_situation', 'address_proof', 'bank_statement', 'sat_positive_opinion', 'incorporation_act', 'legal_power', 'identification', 'imss_opinion', 'infonavit_opinion', 'supplier_registration_request', 'repse', 'confidentiality_agreement', 'induction_course',
#                   ]
#         widgets = {
#             'address_proof': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'bank_statement': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'sat_positive_opinion': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'incorporation_act': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'legal_power': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'identification': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'imss_opinion': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'infonavit_opinion': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'supplier_registration_request': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'repse': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'confidentiality_agreement': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#             'induction_course': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
#         }

#     def clean_fiscal_situation(self):
#         fiscal_situation = self.cleaned_data.get('fiscal_situation')
#         if fiscal_situation:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = fiscal_situation.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return fiscal_situation

#     def clean_address_proof(self):
#         address_proof = self.cleaned_data.get('address_proof')
#         if address_proof:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = address_proof.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return address_proof

#     def clean_bank_statement(self):
#         bank_statement = self.cleaned_data.get('bank_statement')
#         if bank_statement:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = bank_statement.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return bank_statement

#     def clean_sat_positive_opinion(self):
#         sat_positive_opinion = self.cleaned_data.get('sat_positive_opinion')
#         if sat_positive_opinion:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = sat_positive_opinion.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return sat_positive_opinion

#     def clean_incorporation_act(self):
#         incorporation_act = self.cleaned_data.get('incorporation_act')
#         if incorporation_act:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = incorporation_act.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return incorporation_act

#     def clean_legal_power(self):
#         legal_power = self.cleaned_data.get('legal_power')
#         if legal_power:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = legal_power.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return legal_power

#     def clean_identification(self):
#         identification = self.cleaned_data.get('identification')
#         if identification:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = identification.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return identification

#     def clean_imss_opinion(self):
#         imss_opinion = self.cleaned_data.get('imss_opinion')
#         if imss_opinion:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = imss_opinion.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return imss_opinion

#     def clean_infonavit_opinion(self):
#         infonavit_opinion = self.cleaned_data.get('infonavit_opinion')
#         if infonavit_opinion:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = infonavit_opinion.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return infonavit_opinion

#     def clean_supplier_registration_request(self):
#         supplier_registration_request = self.cleaned_data.get(
#             'supplier_registration_request')
#         if supplier_registration_request:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = supplier_registration_request.name.split(
#                 '.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return supplier_registration_request

#     def clean_repse(self):
#         repse = self.cleaned_data.get('repse')
#         if repse:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = repse.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return repse

#     def clean_confidentiality_agreement(self):
#         confidentiality_agreement = self.cleaned_data.get(
#             'confidentiality_agreement')
#         if confidentiality_agreement:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = confidentiality_agreement.name.split(
#                 '.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return confidentiality_agreement

#     def clean_induction_course(self):
#         induction_course = self.cleaned_data.get('induction_course')
#         if induction_course:
#             valid_extensions = ['jpg', 'jpeg', 'png', 'pdf']
#             file_extension = induction_course.name.split('.')[-1].lower()
#             if file_extension not in valid_extensions:
#                 raise ValidationError(
#                     f"Solo se permiten archivos con extensiones: {', '.join(valid_extensions)}")
#         return induction_course
