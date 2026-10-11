from django.db import migrations


CAMPI = (
    ('IF BAIANO - CAMPUS ALAGOINHAS', 'Alagoinhas', None),
    ('IF BAIANO - CAMPUS BOM JESUS DA LAPA', 'Bom Jesus da Lapa', None),
    ('IF BAIANO - CAMPUS CATU', 'Catu', None),
    ('IF BAIANO - CAMPUS GOVERNADOR MANGABEIRA', 'Governador Mangabeira', None),
    ('IF BAIANO - CAMPUS GUANAMBI', 'Guanambi', '29339227'),
    ('IF BAIANO - CAMPUS ITABERABA', 'Itaberaba', None),
    ('IF BAIANO - CAMPUS ITAPETINGA', 'Itapetinga', None),
    ('IF BAIANO - CAMPUS SANTA INÊS', 'Santa Inês', None),
    ('IF BAIANO - CAMPUS SENHOR DO BONFIM', 'Senhor do Bonfim', None),
    ('IF BAIANO - CAMPUS SERRINHA', 'Serrinha', None),
    ('IF BAIANO - CAMPUS TEIXEIRA DE FREITAS', 'Teixeira de Freitas', None),
    ('IF BAIANO - CAMPUS URUÇUCA', 'Uruçuca', None),
    ('IF BAIANO - CAMPUS VALENÇA', 'Valença', None),
    ('IF BAIANO - CAMPUS XIQUE-XIQUE', 'Xique-Xique', None),
)


def seed_campi(apps, schema_editor):
    Escola = apps.get_model('escolas', 'Escola')
    escolas = Escola.objects.using(schema_editor.connection.alias)

    for nome, cidade, codigo_inep in CAMPI:
        valores = {'nome': nome, 'cidade': cidade, 'estado': 'BA'}
        if codigo_inep:
            escolas.update_or_create(codigo_inep=codigo_inep, defaults=valores)
        else:
            escolas.get_or_create(**valores)


class Migration(migrations.Migration):
    dependencies = [
        ('escolas', '0003_escola_codigo_inep_alter_escola_cidade_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_campi, migrations.RunPython.noop),
    ]