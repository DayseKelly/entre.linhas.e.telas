from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from escolas.models import Escola
from .models import Usuario


class AreaPessoalTests(TestCase):
	def test_area_pessoal_abre_sem_perfil_cadastral(self):
		usuario = get_user_model().objects.create_user(username='leitora', password='senha-segura-123')
		self.client.force_login(usuario)

		resposta = self.client.get(reverse('minha_area'))

		self.assertEqual(resposta.status_code, 200)
		self.assertContains(resposta, 'Meus favoritos')
		self.assertContains(resposta, 'Meus comentários')
		
class GestaoUsuariosTests(TestCase):
	def setUp(self):
		self.administrador = get_user_model().objects.create_superuser(
			username='admin',
			email='admin@example.test',
			password='senha-segura-123',
		)
		self.escola = Escola.objects.get(codigo_inep='29339227')
		self.client.force_login(self.administrador)

	def test_lista_e_cadastro_de_usuario_usam_perfil_separado(self):
		resposta = self.client.get(reverse('listar_usuarios'))
		self.assertEqual(resposta.status_code, 200)

		resposta = self.client.post(reverse('criar_usuario'), {
			'username': 'nova_leitora',
			'password': 'senha-segura-456',
			'data_nasc': '2005-06-15',
			'rg': '1234567',
			'cpf': '123.456.789-01',
			'escola': self.escola.pk,
		})

		self.assertRedirects(resposta, reverse('listar_usuarios'))
		perfil = Usuario.objects.select_related('user').get(user__username='nova_leitora')
		self.assertTrue(perfil.user.check_password('senha-segura-456'))

	def test_cadastro_rejeita_nome_de_usuario_repetido(self):
		get_user_model().objects.create_user(username='existente', password='senha-segura-123')
		resposta = self.client.post(reverse('criar_usuario'), {
			'username': 'existente',
			'password': 'senha-segura-456',
			'data_nasc': '2005-06-15',
			'rg': '1234567',
			'cpf': '123.456.789-01',
			'escola': self.escola.pk,
		})
		self.assertEqual(resposta.status_code, 200)
		self.assertContains(resposta, 'Este nome de usuário já está em uso.')
		self.assertFalse(Usuario.objects.filter(user__username='existente').exists())


class CadastroPublicoTests(TestCase):
	def setUp(self):
		self.escola = Escola.objects.get(codigo_inep='29339227')

	def test_cadastro_publico_exibe_instrucoes_de_senha_em_portugues(self):
		resposta = self.client.get(reverse('cadastro'))
		self.assertEqual(resposta.status_code, 200)
		self.assertContains(resposta, 'Pelo menos 8 caracteres')
		self.assertContains(resposta, 'não pode ser tão comum')

	def test_cadastro_publico_cria_conta_e_perfil(self):
		url = reverse('cadastro')
		self.assertEqual(self.client.get(url).status_code, 200)
		resposta = self.client.post(url, {
			'username': 'nova_leitora',
			'password': 'senha-segura-456',
			'password_confirmation': 'senha-segura-456',
			'data_nasc': '2005-06-15',
			'rg': '1234567',
			'cpf': '123.456.789-01',
			'escola': self.escola.pk,
		})
		self.assertRedirects(resposta, reverse('minha_area'))
		self.assertTrue(Usuario.objects.filter(user__username='nova_leitora').exists())

	def test_cadastro_publico_rejeita_senhas_diferentes(self):
		resposta = self.client.post(reverse('cadastro'), {
			'username': 'nova_leitora',
			'password': 'senha-segura-456',
			'password_confirmation': 'outra-senha-789',
			'data_nasc': '2005-06-15',
			'rg': '1234567',
			'cpf': '123.456.789-01',
			'escola': self.escola.pk,
		})
		self.assertEqual(resposta.status_code, 200)
		self.assertContains(resposta, 'As senhas não coincidem.')
		self.assertFalse(get_user_model().objects.filter(username='nova_leitora').exists())

	def test_cadastro_publico_rejeita_escola_invalida_sem_erro_500(self):
		resposta = self.client.post(reverse('cadastro'), {
			'username': 'nova_leitora',
			'password': 'senha-segura-456',
			'password_confirmation': 'senha-segura-456',
			'data_nasc': '2005-06-15',
			'rg': '1234567',
			'cpf': '123.456.789-01',
			'escola': 'id-invalido',
		})

		self.assertEqual(resposta.status_code, 200)
		self.assertFalse(get_user_model().objects.filter(username='nova_leitora').exists())

	def test_busca_retorna_apenas_os_14_campi_do_if_baiano(self):
		Escola.objects.create(nome='IFBA - CAMPUS SALVADOR', cidade='Salvador', estado='BA')

		resposta = self.client.get(reverse('buscar_escolas'), {'q': 'BA'})
		resultados = resposta.json()['results']

		self.assertEqual(resposta.status_code, 200)
		self.assertEqual(len(resultados), 14)
		self.assertTrue(all(resultado['label'].startswith('IF BAIANO - CAMPUS ') for resultado in resultados))
