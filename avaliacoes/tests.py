from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from obras.models import Obra
from .models import Avaliacao

class AvaliacoesTests(TestCase):
	def setUp(self):
		self.usuario = get_user_model().objects.create_user(username='leitora', password='senha-segura-123')
		self.outra_pessoa = get_user_model().objects.create_user(username='leitor', password='senha-segura-123')
		self.obra = Obra.objects.create(titulo='Livro de teste', autor='Autora', resumo='')
		self.client.force_login(self.usuario)

	def test_usuario_publica_e_atualiza_comentario_na_ficha(self):
		url = reverse('detalhe_obra', args=[self.obra.pk])
		dados = {'nota': '8.5', 'comentario': 'Uma leitura importante.'}

		resposta = self.client.post(url, dados)
		self.assertRedirects(resposta, url)
		self.assertEqual(Avaliacao.objects.filter(usuario=self.usuario, obra=self.obra).count(), 1)

		dados['nota'] = '9'
		dados['comentario'] = 'Atualizei minha leitura.'
		resposta = self.client.post(url, dados)
		self.assertRedirects(resposta, url)
		avaliacao = Avaliacao.objects.get(usuario=self.usuario, obra=self.obra)
		self.assertEqual(avaliacao.nota, 9)
		self.assertEqual(avaliacao.comentario, 'Atualizei minha leitura.')

	def test_formulario_avaliacao_redireciona_para_obra(self):
		resposta = self.client.post(reverse('criar_avaliacao'), {
			'obra': self.obra.pk,
			'nota': '8',
			'comentario': 'Gostei da leitura.',
		})
		self.assertRedirects(resposta, reverse('detalhe_obra', args=[self.obra.pk]))


	def test_aba_mostra_apenas_comentarios_da_conta_atual(self):
		Avaliacao.objects.create(usuario=self.usuario, obra=self.obra, nota=8, comentario='Meu comentário visível.')
		outra_obra = Obra.objects.create(titulo='Outro livro', autor='Outro autor', resumo='')
		Avaliacao.objects.create(usuario=self.outra_pessoa, obra=outra_obra, nota=7, comentario='Comentário alheio.')

		resposta = self.client.get(reverse('minhas_avaliacoes'))

		self.assertContains(resposta, 'Meu comentário visível.')
		self.assertNotContains(resposta, 'Comentário alheio.')
