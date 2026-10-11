from django.db import models
from django.conf import settings
from escolas.models import Escola

class Usuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    data_nasc = models.DateField()
    rg = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14, unique=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='usuarios')
    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return self.user.username