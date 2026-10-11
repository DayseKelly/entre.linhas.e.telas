from urllib.parse import quote_plus

from django.db import migrations, models


REPERTORIOS = {
    'O Dilema das Redes': ('Jeff Orlowski-Yang', 'Documentário'),
    '13 Reasons Why': ('Jay Asher', 'Livro e série'),
    'Admirável Chip Novo — Pitty': ('Pitty', 'Música'),
    'A Acompanhante': ('Obra audiovisual', 'Filme ou série'),
    'Fahrenheit 451': ('Ray Bradbury', 'Livro'),
    'Her': ('Spike Jonze', 'Filme'),
    'Tempos Modernos': ('Charlie Chaplin', 'Filme'),
    'Construção — Chico Buarque': ('Chico Buarque', 'Música'),
    'Menino Maluquinho': ('Ziraldo', 'Livro'),
    'ECA': ('Brasil', 'Legislação'),
    '1984': ('George Orwell', 'Livro'),
    'A Flor do Buriti': ('João Salaviza e Renée Nader Messora', 'Filme'),
    'Ideias para Adiar o Fim do Mundo': ('Ailton Krenak', 'Livro'),
    'Xote Ecológico': ('Luiz Gonzaga', 'Música'),
    'Quarto de Despejo': ('Carolina Maria de Jesus', 'Livro'),
    'Asa Branca': ('Luiz Gonzaga e Humberto Teixeira', 'Música'),
    'A Queda do Céu': ('Davi Kopenawa e Bruce Albert', 'Livro'),
    'Ailton Krenak': ('Ailton Krenak', 'Pensador e autor'),
    'O Território': ('Alex Pritz', 'Documentário'),
    'A Lei da Água': ('André D’Elia', 'Documentário'),
    'Vidas Secas': ('Graciliano Ramos', 'Livro'),
    'Ilha das Flores': ('Jorge Furtado', 'Curta-metragem'),
    'Wall-E': ('Andrew Stanton', 'Filme'),
    'Comida': ('Titãs', 'Música'),
    'Atypical': ('Robia Rashid', 'Série'),
    'Extraordinário': ('R. J. Palacio', 'Livro'),
    'Tudo Que Quero': ('Ben Lewin', 'Filme'),
    'Como Estrelas na Terra': ('Aamir Khan e Amole Gupte', 'Filme'),
    'Paulo Freire': ('Paulo Freire', 'Educador e autor'),
    'Djamila Ribeiro': ('Djamila Ribeiro', 'Filósofa e autora'),
    'Josué de Castro': ('Josué de Castro', 'Médico, geógrafo e autor'),
    'Pelé': ('Pelé', 'Biografia'),
    'Sabotage': ('Sabotage', 'Música e trajetória'),
    'Constituição Federal': ('Brasil', 'Legislação'),
    'Coach Carter': ('Thomas Carter', 'Filme'),
    'Racionais MC’s': ('Racionais MC’s', 'Música e trajetória'),
    'Cidade de Deus': ('Paulo Lins', 'Livro e filme'),
    'Tropa de Elite': ('José Padilha', 'Filme'),
    'Medida Provisória': ('Lázaro Ramos', 'Filme'),
    'Negro Drama': ('Racionais MC’s', 'Música'),
    'Carandiru': ('Drauzio Varella e Hector Babenco', 'Livro e filme'),
    'Diário de um Detento': ('Racionais MC’s', 'Música'),
    'Saneamento Básico, o Filme': ('Jorge Furtado', 'Filme'),
    'Byung-Chul Han': ('Byung-Chul Han', 'Filósofo e autor'),
    'Que Horas Ela Volta?': ('Anna Muylaert', 'Filme'),
    'Nunca Me Sonharam': ('Cacau Rhoden', 'Documentário'),
    'Barbie': ('Greta Gerwig', 'Filme'),
    'A Hora da Estrela': ('Clarice Lispector', 'Livro'),
    'O Auto da Compadecida': ('Ariano Suassuna', 'Peça e filme'),
    'Central do Brasil': ('Walter Salles', 'Filme'),
    'Torto Arado': ('Itamar Vieira Junior', 'Livro'),
    'O Quinze': ('Rachel de Queiroz', 'Livro'),
    'Capitães da Areia': ('Jorge Amado', 'Livro'),
    'Pequeno Manual Antirracista': ('Djamila Ribeiro', 'Livro'),
    'A Carne': ('Elza Soares', 'Música'),
    'Sampa': ('Caetano Veloso', 'Música'),
    'Filipe Ret': ('Filipe Ret', 'Música e trajetória'),
}


TEMAS = [
    ('1. Redes sociais, IA e tecnologia', 'Impactos das redes sociais na saúde mental', ['O Dilema das Redes', '13 Reasons Why', 'Admirável Chip Novo — Pitty']),
    ('1. Redes sociais, IA e tecnologia', 'Desafios éticos da inteligência artificial', ['A Acompanhante', 'O Dilema das Redes', 'Fahrenheit 451']),
    ('1. Redes sociais, IA e tecnologia', 'Inteligência artificial e relações humanas', ['A Acompanhante', 'Her', 'Admirável Chip Novo — Pitty']),
    ('1. Redes sociais, IA e tecnologia', 'IA e mercado de trabalho', ['Tempos Modernos', 'A Acompanhante', 'Construção — Chico Buarque']),
    ('1. Redes sociais, IA e tecnologia', 'Adultização e exposição infantil nas redes', ['O Dilema das Redes', 'Menino Maluquinho', 'ECA']),
    ('1. Redes sociais, IA e tecnologia', 'Desinformação na sociedade digital', ['Fahrenheit 451', 'O Dilema das Redes', '1984']),
    ('2. Meio ambiente e aquecimento global', 'Enfrentamento das mudanças climáticas', ['A Flor do Buriti', 'Ideias para Adiar o Fim do Mundo', 'Xote Ecológico']),
    ('2. Meio ambiente e aquecimento global', 'Justiça climática', ['A Flor do Buriti', 'Quarto de Despejo', 'Asa Branca']),
    ('2. Meio ambiente e aquecimento global', 'Exploração ambiental', ['A Flor do Buriti', 'A Queda do Céu', 'Xote Ecológico']),
    ('2. Meio ambiente e aquecimento global', 'Desastres ambientais', ['A Lei da Água', 'Vidas Secas', 'A Flor do Buriti']),
    ('2. Meio ambiente e aquecimento global', 'Consumismo e degradação ambiental', ['Ilha das Flores', 'Wall-E', 'Comida']),
    ('3. Neurodivergência', 'Inclusão de pessoas neurodivergentes', ['Atypical', 'Extraordinário', 'Tudo Que Quero']),
    ('3. Neurodivergência', 'Neurodivergência na educação', ['Como Estrelas na Terra', 'Extraordinário', 'Paulo Freire']),
    ('3. Neurodivergência', 'Combate ao preconceito contra neurodivergentes', ['Atypical', 'Tudo Que Quero', 'Djamila Ribeiro']),
    ('3. Neurodivergência', 'Inclusão de neurodivergentes no mercado de trabalho', ['Tudo Que Quero', 'Tempos Modernos']),
    ('4. Povos originários', 'Preservação das culturas indígenas', ['A Flor do Buriti', 'A Queda do Céu', 'Ailton Krenak']),
    ('4. Povos originários', 'Proteção dos territórios indígenas', ['A Flor do Buriti', 'O Território', 'Ailton Krenak']),
    ('4. Povos originários', 'Saberes indígenas e preservação ambiental', ['A Queda do Céu', 'Ideias para Adiar o Fim do Mundo']),
    ('4. Povos originários', 'Invisibilidade dos povos originários', ['A Flor do Buriti', 'O Território']),
    ('4. Povos originários', 'Conflitos entre povos indígenas e exploração econômica', ['A Flor do Buriti', 'O Território']),
    ('5. Esporte e lazer', 'Democratização do acesso ao esporte', ['Pelé', 'Sabotage', 'Constituição Federal']),
    ('5. Esporte e lazer', 'Esporte como instrumento de inclusão social', ['Coach Carter', 'Pelé', 'Sabotage']),
    ('5. Esporte e lazer', 'Desigualdade no acesso ao lazer', ['Quarto de Despejo', 'Sabotage']),
    ('5. Esporte e lazer', 'Esporte e juventude periférica', ['Sabotage', 'Racionais MC’s', 'Cidade de Deus']),
    ('5. Esporte e lazer', 'Esporte e saúde mental', ['13 Reasons Why', 'Coach Carter']),
    ('6. Insegurança alimentar', 'Combate à fome no Brasil', ['Quarto de Despejo', 'Josué de Castro', 'Comida']),
    ('6. Insegurança alimentar', 'Insegurança alimentar e desigualdade', ['Vidas Secas', 'Quarto de Despejo']),
    ('6. Insegurança alimentar', 'Desperdício de alimentos', ['Ilha das Flores', 'Comida']),
    ('6. Insegurança alimentar', 'Alimentação como direito', ['Quarto de Despejo', 'Constituição Federal']),
    ('6. Insegurança alimentar', 'Fome e vulnerabilidade social', ['Quarto de Despejo', 'Vidas Secas']),
    ('7. Adultização', 'Adultização infantil nas redes sociais', ['O Dilema das Redes', 'ECA', 'Admirável Chip Novo — Pitty']),
    ('7. Adultização', 'Exposição de crianças na internet', ['O Dilema das Redes', 'ECA']),
    ('7. Adultização', 'Pressão estética sobre crianças e adolescentes', ['Barbie', 'O Dilema das Redes']),
    ('7. Adultização', 'Perda da infância na sociedade contemporânea', ['Menino Maluquinho', 'O Dilema das Redes']),
    ('7. Adultização', 'Influência do consumo sobre crianças', ['Wall-E', 'Menino Maluquinho']),
    ('8. Segurança pública', 'Violência urbana no Brasil', ['Cidade de Deus', 'Tropa de Elite', 'Racionais MC’s']),
    ('8. Segurança pública', 'Violência contra a juventude negra', ['Medida Provisória', 'Negro Drama']),
    ('8. Segurança pública', 'Juventude periférica e violência', ['Cidade de Deus', 'Sabotage']),
    ('8. Segurança pública', 'Sistema prisional brasileiro', ['Carandiru', 'Diário de um Detento']),
    ('8. Segurança pública', 'Desigualdade social e violência', ['Quarto de Despejo', 'Cidade de Deus']),
    ('9. Saúde', 'Saúde mental dos jovens', ['13 Reasons Why', 'O Dilema das Redes', 'Byung-Chul Han']),
    ('9. Saúde', 'Desigualdade no acesso à saúde', ['Quarto de Despejo', 'Constituição Federal']),
    ('9. Saúde', 'Saúde pública brasileira', ['Saneamento Básico, o Filme', 'Constituição Federal']),
    ('9. Saúde', 'Saúde e saneamento básico', ['Ilha das Flores', 'Saneamento Básico, o Filme']),
    ('9. Saúde', 'Saúde mental na sociedade da produtividade', ['Byung-Chul Han', 'Tempos Modernos', 'Construção — Chico Buarque']),
    ('10. Educação', 'Desigualdade educacional', ['Quarto de Despejo', 'Que Horas Ela Volta?', 'Paulo Freire']),
    ('10. Educação', 'Educação como transformação social', ['Paulo Freire', 'Nunca Me Sonharam']),
    ('10. Educação', 'Educação pública brasileira', ['Nunca Me Sonharam', 'Que Horas Ela Volta?']),
    ('10. Educação', 'Formação do pensamento crítico', ['Fahrenheit 451', 'Paulo Freire']),
    ('10. Educação', 'Tecnologia na educação', ['O Dilema das Redes', 'Fahrenheit 451', 'Paulo Freire']),
    ('11. Banco complementar', 'Repertórios brasileiros para ampliar o banco', ['A Hora da Estrela', 'O Auto da Compadecida', 'Central do Brasil', 'Torto Arado', 'O Quinze', 'Capitães da Areia', 'Pequeno Manual Antirracista', 'A Carne', 'Sampa', 'Filipe Ret']),
]


def seed_catalogo(apps, schema_editor):
    Obra = apps.get_model('obras', 'Obra')
    Tema = apps.get_model('obras', 'Tema')

    repertorios = {}
    for titulo, (autor, tipo) in REPERTORIOS.items():
        if titulo == 'ECA':
            link = 'https://www.planalto.gov.br/ccivil_03/leis/l8069.htm'
        elif titulo == 'Constituição Federal':
            link = 'https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm'
        else:
            link = 'https://www.google.com/search?q=' + quote_plus(f'{titulo} {autor}')
        obra, _ = Obra.objects.get_or_create(
            titulo=titulo,
            defaults={'autor': autor, 'tipo': tipo, 'link': link, 'resumo': ''},
        )
        repertorios[titulo] = obra

    for area, nome, titulos in TEMAS:
        tema, _ = Tema.objects.get_or_create(area=area, nome=nome)
        tema.repertorios.set(repertorios[titulo] for titulo in titulos if titulo in repertorios)


class Migration(migrations.Migration):
    dependencies = [
        ('obras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=100)),
                ('nome', models.CharField(max_length=180)),
            ],
            options={'ordering': ['area', 'nome']},
        ),
        migrations.AddConstraint(
            model_name='tema',
            constraint=models.UniqueConstraint(fields=('area', 'nome'), name='tema_unico_por_area'),
        ),
        migrations.AddField(
            model_name='obra',
            name='tipo',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='obra',
            name='resumo',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='obra',
            name='temas',
            field=models.ManyToManyField(blank=True, related_name='repertorios', to='obras.tema'),
        ),
        migrations.AddField(
            model_name='obra',
            name='link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='obra',
            name='pdf_url',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='obra',
            name='arquivo_pdf',
            field=models.FileField(blank=True, upload_to='repertorios/pdfs/'),
        ),
        migrations.RunPython(seed_catalogo, migrations.RunPython.noop),
    ]