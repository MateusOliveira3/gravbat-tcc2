import unittest
from model.dimensioning import dimensionar_demanda


class TestDimensionamento(unittest.TestCase):
    def test_massa_energia_e_potencia_media(self):
        r = dimensionar_demanda(1.0, .2, 10.0, .8, 2.0, 100.0)
        self.assertGreater(r["massa_total_kg"], 0)
        self.assertAlmostEqual(r["potencia_media_kW"], .5)
        self.assertAlmostEqual(r["modulos_por_energia"], r["massa_total_kg"] / 100)

    def test_entradas_invalidas(self):
        with self.assertRaises(ValueError): dimensionar_demanda(1, .2, 10, 0, 2)
        with self.assertRaises(ValueError): dimensionar_demanda(1, .2, 10, .8, 0)
