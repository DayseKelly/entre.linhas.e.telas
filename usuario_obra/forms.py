from django import forms
from .models import UsuarioObra

class UsuarioObraForm(forms.ModelForm):
    class Meta:
        model = UsuarioObra
        fields = ['usuario', 'obra', 'favorito', 'lido']