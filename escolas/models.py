from django.db import models

class Escola(models.Model):
    codigo_inep = models.CharField(max_length=8, unique=True, null=True, blank=True)
    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    def __str__(self):
        return f"{self.nome} - {self.cidade}/{self.estado}"