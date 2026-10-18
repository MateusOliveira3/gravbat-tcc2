import math
import unittest
from model.cable import GeometriaCabo


class TestCabo(unittest.TestCase):
    def test_voltas_da_primeira_camada(self):
        c = GeometriaCabo("aço", .01, .10, 10.0)
        self.assertAlmostEqual(c.raio_nucleo_m, .05)
        self.assertAlmostEqual(c.voltas_estimadas_primeira_camada, 10/(math.pi*.1))

    def test_parametros_invalidos(self):
        with self.assertRaises(ValueError): GeometriaCabo("", .01, .1, 10)
        with self.assertRaises(ValueError): GeometriaCabo("aço", 0, .1, 10)
