from django.db import models
from django.conf import settings
from obras.models import Obra

class UsuarioObra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='minhas_obras')
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='usuarios_interagiram')
    
    # (true or false) do diagrama
    favorito = models.BooleanField(default=False)
    lido = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'obra'], name='usuario_obra_unica_por_conta'),
        ]

    def __str__(self):
        return f"{self.usuario.username} - Obra: {self.obra.titulo}"