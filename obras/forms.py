from django import forms
from .models import Obra

class ObraForm(forms.ModelForm):    
        class Meta:
                model = Obra
                fields = ['titulo', 'autor', 'tipo', 'resumo', 'temas', 'link', 'pdf_url', 'arquivo_pdf', 'capa', 'capa_url']
                labels = {
                        'titulo': 'Título',
                        'autor': 'Autor ou responsável',
                        'tipo': 'Tipo de repertório',
                        'resumo': 'Anotações de estudo',
                        'temas': 'Temas relacionados',
                        'link': 'Link de acesso',
                            'pdf_url': 'Link para PDF oficial ou de domínio público',
                        'arquivo_pdf': 'Enviar PDF',
                        'capa': 'Imagem de capa',
                            'capa_url': 'Link direto da capa',
                }
                help_texts = {
                        'temas': 'Você pode selecionar mais de um tema.',
                        'arquivo_pdf': 'Envie somente arquivos que você tem autorização para compartilhar.',
                            'capa_url': 'Opcional: use uma imagem pública; se ficar indisponível, será exibida uma capa tipográfica.',
                            'pdf_url': 'Use apenas PDFs disponibilizados legalmente pelo autor, editora ou domínio público.',
                }

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields.values():
                        widget = field.widget
                        css_class = 'form-select' if isinstance(widget, (forms.Select, forms.SelectMultiple)) else 'form-control'
                        widget.attrs['class'] = f'{widget.attrs.get("class", "")} {css_class}'.strip()
                        if isinstance(widget, forms.SelectMultiple):
                                widget.attrs['size'] = 8