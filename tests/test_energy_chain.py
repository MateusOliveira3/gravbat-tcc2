import unittest
from model.energy_chain import balanço_transformacoes


class TestBalançoTransformacoes(unittest.TestCase):
    def test_perdas_por_etapa_e_produto_global(self):
        etapas = balanço_transformacoes(1000.0, (.9, .8, .7, .9, .95, .98))
        self.assertEqual(len(etapas), 6)
        self.assertAlmostEqual(etapas[0].saida_J, 900.0)
        self.assertGreaterEqual(sum(e.perda_J for e in etapas), 0.0)
        self.assertAlmostEqual(etapas[-1].saida_J, 1000*.9*.8*.7*.9*.95*.98)

    def test_eficiencia_unitaria_conserva_energia(self):
        etapas = balanço_transformacoes(100.0, (1, 1, 1, 1, 1, 1))
        self.assertTrue(all(e.perda_J == 0 for e in etapas))
        self.assertEqual(etapas[-1].saida_J, 100.0)

    def test_quantidade_e_valores_invalidos(self):
        with self.assertRaises(ValueError): balanço_transformacoes(1, (.9,))
        with self.assertRaises(ValueError): balanço_transformacoes(1, (.9, .8, 0, .9, .9, .9))
