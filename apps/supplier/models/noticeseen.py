from django.db import models
from django.contrib.auth.models import User  # El modelo User de Django
from .notice import Notice

class NoticeSeen(models.Model):
    notice = models.ForeignKey(Notice,on_delete=models.CASCADE,verbose_name="Comunicado")
    provider = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Proveedor")
    seen = models.BooleanField(default=False,verbose_name="Visto")
    do_not_show_again = models.BooleanField(default=False,verbose_name="No mostrar de nuevo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Comunicado Visto"
        verbose_name_plural = "Comunicados Vistos"

    def __str__(self):
        return f"{self.provider.company_name} - {self.notice.title}"