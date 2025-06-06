from django import forms
from django.utils.timezone import now, timedelta
from apps.supplier.models import Notice


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'text', 'image', 'published_at', 'visible_until']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del comunicado', 'max': '50'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Texto del comunicado', 'max': '500'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'published_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'visible_until': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            today = now().date()
            self.fields['published_at'].initial = today.strftime('%Y-%m-%d')
            self.fields['visible_until'].initial = (today + timedelta(days=3)).strftime('%Y-%m-%d')