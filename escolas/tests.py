from django.test import TestCase

from .constants import CAMPI_IF_BAIANO
from .models import Escola


class CampiIfBaianoTests(TestCase):
    def test_migracao_cadastra_exatamente_os_14_campi(self):
        campi = Escola.objects.filter(nome__in=CAMPI_IF_BAIANO)

        self.assertEqual(campi.count(), 14)
        self.assertSetEqual(set(campi.values_list('nome', flat=True)), set(CAMPI_IF_BAIANO))
        self.assertEqual(set(campi.values_list('estado', flat=True)), {'BA'})
        self.assertEqual(
            Escola.objects.get(codigo_inep='29339227').nome,
            'IF BAIANO - CAMPUS GUANAMBI',
        )
