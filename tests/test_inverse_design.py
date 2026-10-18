import unittest

from model.inverse_design import dimensionar_configuracao


class TestInverseDesign(unittest.TestCase):
    def test_massa_atende_energia_e_potencia(self):
        r = dimensionar_configuracao(500, 100, 50, 10, .55, .02)
        self.assertGreaterEqual(r["massa_requerida_kg"], r["massa_por_energia_kg"])
        self.assertGreaterEqual(r["massa_requerida_kg"], r["massa_por_potencia_kg"])
        self.assertEqual(r["status"], "CALCULADO")

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError):
            dimensionar_configuracao(500, 100, 0, 10, .55)
        with self.assertRaises(ValueError):
            dimensionar_configuracao(500, 100, 50, 10, 1.2)
