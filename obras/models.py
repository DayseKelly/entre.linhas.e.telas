from django.db import models

class Tema(models.Model):
    area = models.CharField(max_length=100)
    nome = models.CharField(max_length=180)

    class Meta:
        ordering = ['area', 'nome']
        constraints = [
            models.UniqueConstraint(fields=['area', 'nome'], name='tema_unico_por_area'),
        ]

    def __str__(self):
        return f'{self.area} - {self.nome}'


class Obra(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    tipo = models.CharField(max_length=40, blank=True)
    resumo = models.TextField(blank=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    capa_url = models.URLField(blank=True)
    temas = models.ManyToManyField(Tema, blank=True, related_name='repertorios')
    link = models.URLField(blank=True)
    pdf_url = models.URLField(blank=True)
    arquivo_pdf = models.FileField(upload_to='repertorios/pdfs/', blank=True)

    def __str__(self):
        return self.titulo