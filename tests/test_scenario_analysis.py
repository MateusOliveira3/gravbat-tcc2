import unittest
from model.scenario_analysis import comparar_cenarios


class TestCenarios(unittest.TestCase):
    def test_comparacao_preserva_identificacao(self):
        r = comparar_cenarios([
            {"nome": "baixo", "energia_util_kWh": 1, "potencia_max_kW": .2,
             "altura_m": 10, "eficiencia_global": .5, "tempo_descarga_h": 2},
            {"nome": "alto", "energia_util_kWh": 1, "potencia_max_kW": .2,
             "altura_m": 20, "eficiencia_global": .5, "tempo_descarga_h": 2},
        ])
        self.assertEqual([x["nome"] for x in r], ["baixo", "alto"])
        self.assertLess(r[1]["massa_total_kg"], r[0]["massa_total_kg"])
