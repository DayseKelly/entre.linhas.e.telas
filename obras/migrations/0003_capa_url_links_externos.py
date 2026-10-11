from urllib.parse import quote_plus

from django.db import migrations, models


def update_material_links(apps, schema_editor):
    Obra = apps.get_model('obras', 'Obra')

    for obra in Obra.objects.all().iterator():
        query = quote_plus(f'{obra.titulo} {obra.autor}')
        if obra.titulo == 'ECA':
            obra.link = 'https://www.planalto.gov.br/ccivil_03/leis/l8069.htm'
        elif obra.titulo == 'Constituição Federal':
            obra.link = 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm'
        elif obra.tipo == 'Música':
            obra.link = f'https://www.youtube.com/results?search_query={query}'
        elif 'Livro' in obra.tipo:
            obra.link = f'https://openlibrary.org/search?q={query}'
            obra.capa_url = f'https://covers.openlibrary.org/b/title/{quote_plus(obra.titulo)}-L.jpg?default=false'
        elif obra.tipo in ('Filme', 'Documentário', 'Curta-metragem', 'Filme ou série'):
            obra.link = f'https://www.youtube.com/results?search_query={quote_plus(obra.titulo + " trailer")}'
        else:
            obra.link = f'https://www.google.com/search?q={query}'
        obra.save(update_fields=['link', 'capa_url'])


class Migration(migrations.Migration):
    dependencies = [
        ('obras', '0002_catalogo_temas_links_pdfs'),
    ]

    operations = [
        migrations.AddField(
            model_name='obra',
            name='capa_url',
            field=models.URLField(blank=True),
        ),
        migrations.RunPython(update_material_links, migrations.RunPython.noop),
    ]