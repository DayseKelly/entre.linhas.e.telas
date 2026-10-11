from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from obras.models import Obra

class Avaliacao(models.Model):
    nota = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avaliacoes')
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='avaliacoes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'obra'], name='avaliacao_unica_por_usuario_obra'),
        ]

    def __str__(self):
        return f"Nota {self.nota} por {self.usuario.username}"
