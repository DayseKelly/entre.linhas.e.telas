from django.db import migrations


ARTIGOS = [
    ('1º, III', 'Dignidade da pessoa humana', 'Fundamento constitucional para discutir respeito, autonomia e condições dignas de vida.', ['Inclusão de pessoas neurodivergentes', 'Desigualdade no acesso à saúde']),
    ('3º, IV', 'Combate à discriminação', 'Princípio constitucional que orienta o enfrentamento de preconceitos e desigualdades.', ['Combate ao preconceito contra neurodivergentes', 'Violência contra a juventude negra', 'Desigualdade social e violência']),
    ('5º', 'Direitos e garantias fundamentais', 'Referência para abordar igualdade perante a lei, liberdade e proteção de direitos individuais.', ['Combate ao preconceito contra neurodivergentes', 'Adultização infantil nas redes sociais', 'Exposição de crianças na internet']),
    ('6º', 'Direitos sociais', 'Reúne direitos como educação, saúde, alimentação, lazer, segurança e proteção à infância.', ['Combate à fome no Brasil', 'Alimentação como direito', 'Democratização do acesso ao esporte', 'Desigualdade no acesso ao lazer', 'Desigualdade no acesso à saúde']),
    ('144', 'Segurança pública', 'Define a segurança pública como dever do Estado e direito e responsabilidade de todos.', ['Violência urbana no Brasil', 'Violência contra a juventude negra', 'Juventude periférica e violência', 'Sistema prisional brasileiro', 'Desigualdade social e violência']),
    ('196', 'Direito à saúde', 'Estabelece a saúde como direito de todos e dever do Estado, garantida por políticas públicas.', ['Saúde mental dos jovens', 'Desigualdade no acesso à saúde', 'Saúde pública brasileira', 'Saúde e saneamento básico']),
    ('205', 'Direito à educação', 'Apresenta a educação como direito de todos e responsabilidade compartilhada entre Estado, família e sociedade.', ['Desigualdade educacional', 'Educação como transformação social', 'Educação pública brasileira', 'Tecnologia na educação']),
    ('208, III', 'Atendimento educacional especializado', 'Prevê atendimento educacional especializado, preferencialmente na rede regular de ensino.', ['Neurodivergência na educação', 'Inclusão de pessoas neurodivergentes']),
    ('215', 'Direitos culturais', 'Protege o exercício dos direitos culturais e o acesso às fontes da cultura nacional.', ['Preservação das culturas indígenas', 'Invisibilidade dos povos originários']),
    ('217', 'Esporte e lazer', 'Reconhece o dever estatal de fomentar práticas desportivas como direito de cada pessoa.', ['Democratização do acesso ao esporte', 'Esporte como instrumento de inclusão social', 'Desigualdade no acesso ao lazer', 'Esporte e juventude periférica']),
    ('225', 'Meio ambiente equilibrado', 'Reconhece o direito ao meio ambiente equilibrado e o dever coletivo de protegê-lo.', ['Enfrentamento das mudanças climáticas', 'Justiça climática', 'Exploração ambiental', 'Desastres ambientais', 'Consumismo e degradação ambiental', 'Saberes indígenas e preservação ambiental']),
    ('227', 'Proteção integral à criança e ao adolescente', 'Estabelece prioridade absoluta para direitos, proteção e desenvolvimento de crianças e adolescentes.', ['Adultização infantil nas redes sociais', 'Exposição de crianças na internet', 'Pressão estética sobre crianças e adolescentes', 'Perda da infância na sociedade contemporânea', 'Influência do consumo sobre crianças']),
    ('231', 'Direitos dos povos indígenas', 'Reconhece a organização social, costumes, línguas, crenças, tradições e direitos territoriais indígenas.', ['Preservação das culturas indígenas', 'Proteção dos territórios indígenas', 'Saberes indígenas e preservação ambiental', 'Invisibilidade dos povos originários', 'Conflitos entre povos indígenas e exploração econômica']),
]


def seed_artigos(apps, schema_editor):
    Obra = apps.get_model('obras', 'Obra')
    Tema = apps.get_model('obras', 'Tema')

    for numero, titulo, resumo, nomes_temas in ARTIGOS:
        titulo_completo = f'Constituição Federal — Art. {numero}: {titulo}'
        obra, _ = Obra.objects.get_or_create(
            titulo=titulo_completo,
            defaults={
                'autor': 'Constituição Federal de 1988',
                'tipo': 'Legislação',
                'resumo': resumo,
                'link': f'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm#art{numero.split(",")[0].replace("º", "")}',
            },
        )
        obra.temas.set(Tema.objects.filter(nome__in=nomes_temas))


class Migration(migrations.Migration):
    dependencies = [
        ('obras', '0003_capa_url_links_externos'),
    ]

    operations = [
        migrations.RunPython(seed_artigos, migrations.RunPython.noop),
    ]