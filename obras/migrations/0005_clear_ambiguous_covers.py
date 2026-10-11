from django.db import migrations


def clear_title_only_covers(apps, schema_editor):
    Obra = apps.get_model('obras', 'Obra')
    Obra.objects.filter(capa_url__startswith='https://covers.openlibrary.org/b/title/').update(capa_url='')


class Migration(migrations.Migration):
    dependencies = [
        ('obras', '0004_artigos_constituicao'),
    ]

    operations = [
        migrations.RunPython(clear_title_only_covers, migrations.RunPython.noop),
    ]