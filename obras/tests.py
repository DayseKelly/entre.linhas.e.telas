from django.test import TestCase

from .models import Obra


class ArtigosConstituicaoTests(TestCase):
	def test_artigos_sao_repertorios_com_link_oficial_e_temas(self):
		artigos = Obra.objects.filter(titulo__startswith='Constituição Federal — Art.')

		self.assertEqual(artigos.count(), 13)
		self.assertTrue(all(artigo.link.startswith('https://www.planalto.gov.br/') for artigo in artigos))
		self.assertFalse(artigos.filter(temas__isnull=True).exists())


class LinksDeRepertorioTests(TestCase):
	def test_musicas_abrem_youtube_e_livros_abrem_edicoes_digitais(self):
		musicas = Obra.objects.filter(tipo__icontains='música')
		livros = Obra.objects.filter(tipo__icontains='livro')

		self.assertTrue(musicas.exists())
		self.assertTrue(livros.exists())
		self.assertTrue(all(item.link.startswith('https://www.youtube.com/results?') for item in musicas))
		self.assertTrue(all(item.link.startswith('https://books.google.com/books?') for item in livros))
