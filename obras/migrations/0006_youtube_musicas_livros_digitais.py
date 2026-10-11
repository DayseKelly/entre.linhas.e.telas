from urllib.parse import quote_plus

from django.db import migrations


def update_book_and_music_links(apps, schema_editor):
    Obra = apps.get_model('obras', 'Obra')

    for obra in Obra.objects.all().iterator():
        tipo = (obra.tipo or '').casefold()
        titulo_musical = obra.titulo.split(' — ', 1)[0].split(' – ', 1)[0]

        if 'música' in tipo:
            consulta = quote_plus(f'{titulo_musical} {obra.autor}')
            obra.link = f'https://www.youtube.com/results?search_query={consulta}'
            obra.save(update_fields=['link'])
        elif 'livro' in tipo:
            consulta = quote_plus(f'{obra.titulo} {obra.autor}')
            obra.link = f'https://books.google.com/books?q={consulta}'
            obra.save(update_fields=['link'])


class Migration(migrations.Migration):
    dependencies = [
        ('obras', '0005_clear_ambiguous_covers'),
    ]

    operations = [
        migrations.RunPython(update_book_and_music_links, migrations.RunPython.noop),
    ]