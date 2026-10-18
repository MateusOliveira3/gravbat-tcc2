import unittest

from model.application_scenarios import SCENARIOS, obter_cenario


class TestApplicationScenarios(unittest.TestCase):
    def test_catalogo_tem_status_e_parametros_positivos(self):
        self.assertGreaterEqual(len(SCENARIOS), 3)
        for c in SCENARIOS.values():
            self.assertEqual(c["status"], "HIPÓTESE")
            for k in ("energia_util_kWh", "potencia_max_kW", "altura_m", "tempo_descarga_h", "eficiencia_global"):
                self.assertGreater(c[k], 0)

    def test_obter_copia_nao_altera_catalogo(self):
        c = obter_cenario("Casa de baixa demanda")
        c["altura_m"] = 999
        self.assertNotEqual(SCENARIOS["Casa de baixa demanda"]["altura_m"], 999)

    def test_nome_invalido(self):
        with self.assertRaises(ValueError):
            obter_cenario("cidade inventada")
