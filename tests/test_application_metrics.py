import math
import unittest

from dashboard.application_metrics import (
    compatibilidade_autonomia,
    duracao_controlada_s,
    potencia_util_estimada,
    velocidade_vertical,
)


class TestMetricasAplicacao(unittest.TestCase):
    def test_projecao_vertical_do_trilho(self):
        self.assertAlmostEqual(velocidade_vertical(0.02, 10), 0.003473, places=6)

    def test_potencia_e_energia_por_duracao_coerentes(self):
        massa_banco = 60.0
        g = 9.81
        theta = 10.0
        v = 0.02
        eta = 0.55
        altura = 2.0
        comprimento = altura / math.sin(math.radians(theta))
        energia_Wh = massa_banco * g * altura * eta / 3600.0
        potencia = potencia_util_estimada(massa_banco, g, v, theta, eta)
        duracao = duracao_controlada_s(comprimento, v)
        self.assertAlmostEqual(potencia, 1.1243024911, places=9)
        self.assertAlmostEqual(energia_Wh * 3600.0 / duracao, potencia, places=9)

    def test_potencia_muda_com_inclinacao(self):
        p10 = potencia_util_estimada(60, 9.81, .02, 10, .55)
        p30 = potencia_util_estimada(60, 9.81, .02, 30, .55)
        self.assertAlmostEqual(p30 / p10, math.sin(math.radians(30)) / math.sin(math.radians(10)))

    def test_autonomia_incompatível_com_descida_curta(self):
        resultado = compatibilidade_autonomia(400, 14400, 575.9)
        self.assertFalse(resultado["atende_duracao"])
        self.assertAlmostEqual(resultado["razao_duracao"], 575.9 / 14400)

    def test_autonomia_compativel_quando_duracao_cobre_demanda(self):
        resultado = compatibilidade_autonomia(400, 14400, 14400)
        self.assertTrue(resultado["atende_duracao"])


if __name__ == "__main__":
    unittest.main()

