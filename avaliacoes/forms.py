from django import forms
from .models import Avaliacao

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario', 'obra']
        labels = {
            'nota': 'Nota de 0 a 10',
            'comentario': 'Comentário',
            'obra': 'Repertório',
        }
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.5}),
            'comentario': forms.Textarea(attrs={'rows': 4}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        labels = {
            'nota': 'Nota de 0 a 10',
            'comentario': 'Seu comentário',
        }
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.5}),
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Compartilhe sua leitura desta obra…'}),
        }