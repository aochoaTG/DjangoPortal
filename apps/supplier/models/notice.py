from django.db import models
from django.contrib.auth.models import User  # El modelo User de Django
from django.utils import timezone

class Notice(models.Model):
    title = models.CharField(max_length=50,verbose_name="Título", help_text="Máximo 50 caracteres")
    text = models.TextField(max_length=500,verbose_name="Texto", help_text="Máximo 500 caracteres")
    image = models.ImageField(upload_to='notices/',blank=True,null=True,verbose_name="Imagen")
    published_at = models.DateTimeField(default=timezone.now,verbose_name="Fecha de publicación")
    visible_until = models.DateTimeField(null=True,blank=True,verbose_name="Visible hasta")
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name="Creado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Cominicado"
        verbose_name_plural = "Comunicados"

    def __str__(self):
        return self.title