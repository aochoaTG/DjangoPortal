"""Formularios para la aplicación de cuentas de usuario"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from apps.supplier.models import Supplier
from apps.accounts.models import Profile
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    """Formulario para la creación de un usuario"""
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}),
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
        label="Confirmación de Contraseña"
    )

    class Meta:
        """Metaclase para el formulario"""
        model = User
        fields = ['username', 'email']
        labels = {
            'username': "Nombre de usuario",
            'email': "Correo electrónico",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre de usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # Establecer el usuario como inactivo por defecto
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")

        return cleaned_data

    def clean_email(self):
        """Valida que el correo electrónico no esté en uso"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return email


# Formulario para la Pestaña 2: Datos Fiscales y Empresariales
class SupplierFiscalForm(forms.ModelForm):
    """Formulario para la creación de un proveedor"""
    class Meta:
        """Metaclase para el formulario"""
        model = Supplier
        fields = ['company_name', 'address',
                  'tax_regime', 'rfc', 'supplier_type']
        labels = {
            'company_name': "Razón Social",
            'address': "Domicilio Fiscal",
            'tax_regime': "Régimen Fiscal",
            'rfc': "RFC",
            'supplier_type': "Tipo de Proveedor",
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la razón social'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese el domicilio fiscal'}),
            'tax_regime': forms.Select(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RFC'}),
            'supplier_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_rfc(self):
        """Valida que el RFC no esté en uso"""
        rfc = self.cleaned_data.get('rfc')
        if Supplier.objects.filter(rfc=rfc).exists():
            raise ValidationError("Este RFC ya está registrado en el sistema.")
        return rfc


# Formulario para la Pestaña 3: Información Bancaria
class SupplierBankForm(forms.ModelForm):
    """Formulario para la creación de un proveedor"""
    class Meta:
        model = Supplier
        fields = ['bank_name', 'account_number', 'clabe', 'currency']
        labels = {
            'bank_name': "Banco",
            'account_number': "Número de Cuenta",
            'clabe': "CLABE Interbancaria",
            'currency': "Moneda",
        }
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del banco'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de cuenta'}),
            'clabe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la CLABE interbancaria'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }


class CustomSupplierCreationForm(UserCreationForm):
    """Formulario personalizado para la creación de un proveedor con Bootstrap 5"""
    
    # Campos de contacto
    email = forms.EmailField(
        required=True, 
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )
    
    contact_person = forms.CharField(
        required=True, 
        label=_("Nombre de contacto"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    phone_number = forms.CharField(
        required=True, 
        label=_("Teléfono de contacto"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'})
    )
    
    # Campos de información fiscal
    company = forms.CharField(
        required=True, 
        label=_("Razón social"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    address = forms.CharField(
        required=True, 
        label=_("Domicilio fiscal"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
    )
    
    tax_regime = forms.ChoiceField(
        required=True,
        choices=[
            ('', _('Seleccione una opción')),
            ('individual', _('Persona Física')), 
            ('corporation', _('Persona Moral')), 
            ('resico', _('Régimen Simplificado de Confianza')),
            ('general', _('Régimen General')),
        ],
        label=_("Tipo de régimen"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    rfc_regex = r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$'
    rfc = forms.CharField(
        required=True, 
        label=_("RFC"),
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'XXXX000000XXX',
            'minlength': 12,
            'maxlength': 13
        }),
        help_text=_("RFC válido con homoclave (será usado como nombre de usuario)"),
        validators=[RegexValidator(rfc_regex, message=_("Formato de RFC inválido"))]
    )
    
    supplier_type = forms.ChoiceField(
        required=True,
        choices=[
            ('', _('Seleccione una opción')),
            ('product', _('Productos')), 
            ('service', _('Servicios')),
            ('product_service', _('Ambos')),
        ],
        label=_("Tipo de proveedor"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Definimos los campos de contraseña
    password1 = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=_("La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números.")
    )
    
    password2 = forms.CharField(
        label=_("Confirmación de contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        # Excluimos username de los campos visibles
        fields = [
            'email', 'contact_person', 'phone_number',
            'password1', 'password2', 'company', 'address', 
            'tax_regime', 'rfc', 'supplier_type'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminar el campo username del formulario
        if 'username' in self.fields:
            del self.fields['username']
            
        # Agregar clases para los mensajes de error
        for field in self.fields:
            self.fields[field].error_messages = {'required': _('Este campo es obligatorio')}
            if self.fields[field].required:
                self.fields[field].label = f"{self.fields[field].label} *"
    
    def save(self, commit=True):
        # No usamos super().save() directamente porque estamos modificando el proceso
        user = self.instance
        user.username = self.cleaned_data['rfc'].upper()  # Usar RFC como username
        user.email = self.cleaned_data['email']
        user.is_active = False  # Desactivar el usuario por defecto
        
        # Establecer la contraseña manualmente
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
            
        if commit:
            user.save()
        return user

    def clean_email(self):
        """Valida que el correo electrónico no esté en uso"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este correo electrónico ya está en uso."))
        return email

    def clean_rfc(self):
        """Valida que el RFC no esté en uso y lo utiliza como username"""
        rfc = self.cleaned_data.get('rfc').upper()
        
        # Validar si ya existe un usuario con este RFC como nombre de usuario
        if User.objects.filter(username=rfc).exists():
            raise ValidationError(_("Este RFC ya está registrado en el sistema."))
        
        # Validar si ya existe un proveedor con este RFC
        if Supplier.objects.filter(rfc=rfc).exists():
            raise ValidationError(_("Este RFC ya está registrado en el sistema."))
        
        # Validar formato de RFC
        if not self.validate_rfc_format(rfc):
            raise ValidationError(_("El formato del RFC no es válido."))
            
        return rfc
    
    def validate_rfc_format(self, rfc):
        """Valida el formato del RFC (versión simplificada)"""
        import re
        # Expresión regular para validar RFC mexicano (versión simplificada)
        rfc_pattern = r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$'
        return bool(re.match(rfc_pattern, rfc.upper()))

    def clean_email(self):
        """Valida que el correo electrónico no esté en uso"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Este correo electrónico ya está en uso."))
        return email

    def clean_rfc(self):
        """Valida que el RFC no esté en uso"""
        rfc = self.cleaned_data.get('rfc')
        if Supplier.objects.filter(rfc=rfc).exists():
            raise ValidationError(_("Este RFC ya está registrado en el sistema."))
        # Validar formato de RFC
        if not self.validate_rfc_format(rfc):
            raise ValidationError(_("El formato del RFC no es válido."))
        return rfc
    
    def validate_rfc_format(self, rfc):
        """Valida el formato del RFC (versión simplificada)"""
        import re
        # Expresión regular para validar RFC mexicano (versión simplificada)
        rfc_pattern = r'^[A-Z&Ñ]{3,4}[0-9]{6}[A-Z0-9]{3}$'
        return bool(re.match(rfc_pattern, rfc.upper()))


class StaffUserCreationForm(UserCreationForm):
    """Formulario para crear un usuario de tipo staff"""
    # Campos personalizados para el formulario
    username = forms.CharField(label="Usuario", max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre(s)", max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido(s)", max_length=150,
                                required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    # Campos adicionales que se pondrán automáticamente a 1
    is_staff = forms.BooleanField(
        required=False, initial=True, widget=forms.HiddenInput())
    is_active = forms.BooleanField(
        required=False, initial=True, widget=forms.HiddenInput())

    class Meta:
        """Metaclase para el formulario"""
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Asegurar que 'is_staff' y 'is_active' están a True
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()
        return user


class StaffUserEditForm(forms.ModelForm):
    """Formulario para editar un usuario de tipo staff"""
    username = forms.CharField(label="Usuario", max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre(s)", max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido(s)", max_length=150,
                                required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label="Activo", required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']


class SupplierUserCreationForm(UserCreationForm):
    """Formulario para crear un usuario de tipo proveedor"""
    # Campos personalizados para el formulario
    username = forms.CharField(label="Usuario", max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre(s)", max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido(s)", max_length=150,
                                required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    # Campos adicionales que se pondrán automáticamente a 1
    is_staff = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput())
    is_active = forms.BooleanField(
        required=False, initial=True, widget=forms.HiddenInput())

    class Meta:
        """Metaclase para el formulario"""
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'is_staff', 'is_active']

    def save(self, commit=True):
        """ Método para guardar el usuario """
        user = super().save(commit=False)
        # Asegurar que 'is_staff' y 'is_active' están a True
        user.is_staff = False
        user.is_active = True
        if commit:
            user.save()
        return user


class SupplierUserEditForm(forms.ModelForm):
    """Formulario para editar un usuario de tipo proveedor"""
    username = forms.CharField(label="Usuario", max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre(s)", max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido(s)", max_length=150,
                                required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label="Activo", required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar la información de perfil de un usuario"""
    # Campos relacionados con el modelo `User`
    username = forms.CharField(label="Usuario", max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Nombre(s)", max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Apellido(s)", max_length=150,
                                required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo electrónico", required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    # Campo adicional para la imagen de perfil (modelo `Profile`)
    profile_picture = forms.ImageField(required=False, label="Foto de Perfil", widget=forms.FileInput(
        attrs={'class': 'custom-file-input'}))

    class Meta:
        """Metaclase para el formulario"""
        model = Profile
        fields = ['profile_picture']  # Solo los campos del modelo `Profile`
        widgets = {'profile_picture': forms.ClearableFileInput(
            attrs={'class': 'custom-file-input'}), }

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            self.fields['username'].initial = user_instance.username
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['email'].initial = user_instance.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Usuario")
    first_name = forms.CharField(max_length=30, label="Nombre")
    last_name = forms.CharField(max_length=150, label="Apellido")
    email = forms.EmailField(label="Correo electrónico")
    profile_picture = forms.ImageField(required=False, label="Foto de perfil")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture']

    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)

        # Agregar clases de Bootstrap 5
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.widgets.FileInput):
                field.widget.attrs.update({'class': 'form-control form-control-sm'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        if profile_instance:
            self.fields['profile_picture'].initial = profile_instance.profile_picture

    def save(self, commit=True, profile_instance=None):
        user = super().save(commit)
        if profile_instance:
            profile_instance.profile_picture = self.cleaned_data.get('profile_picture')
            if commit:
                profile_instance.save()
        return user
