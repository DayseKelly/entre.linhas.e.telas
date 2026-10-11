from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from obras.models import Obra
from .models import UsuarioObra

class FavoritosTests(TestCase):
	def setUp(self):
		self.usuario = get_user_model().objects.create_user(username='leitora', password='senha-segura-123')
		self.obra = Obra.objects.create(titulo='Livro favorito', autor='Autora', resumo='')
		self.client.force_login(self.usuario)

	def test_favorito_pode_ser_adicionado_e_removido(self):
		url = reverse('alternar_favorito', args=[self.obra.pk])

		resposta = self.client.post(url)
		self.assertRedirects(resposta, reverse('detalhe_obra', args=[self.obra.pk]))
		self.assertTrue(UsuarioObra.objects.get(usuario=self.usuario, obra=self.obra).favorito)
		self.assertContains(self.client.get(reverse('meus_favoritos')), 'Livro favorito')

		self.client.post(url)
		self.assertFalse(UsuarioObra.objects.get(usuario=self.usuario, obra=self.obra).favorito)
