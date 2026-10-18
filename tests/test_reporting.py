import json
import unittest

from model.reporting import relatorio_cenario, serializar_relatorio, serializar_tabela_relatorio, serializar_trajetoria, serializar_transformacoes


class TestReporting(unittest.TestCase):
    def test_relatorio_e_serializavel_e_classificado(self):
        r = relatorio_cenario({"x": 1}, {"y": 2}, ["h"], ["l"])
        self.assertEqual(r["classificacao"]["validacao"], "NÃO EXPERIMENTAL")
        self.assertEqual(json.loads(serializar_relatorio(r))["entradas"]["x"], 1)
        csv_texto = serializar_tabela_relatorio(r)
        self.assertIn("grupo,parametro,valor,classificacao", csv_texto)
        self.assertIn("entradas,x,1", csv_texto)

    def test_trajetoria_tem_unidades_e_linhas(self):
        csv_texto = serializar_trajetoria([{"tempo_s": 0.0, "posicao_m": 0.0, "velocidade_m_s": 1.0}])
        self.assertIn("tempo (s)", csv_texto)
        self.assertIn("0.0", csv_texto)

    def test_transformacoes_tem_perdas_e_status(self):
        class E:
            nome = "gerador"; entrada_J = 10; saida_J = 8; perda_J = 2; eficiencia = .8; status = "HIPÓTESE"
        csv_texto = serializar_transformacoes([E()])
        self.assertIn("perda (J)", csv_texto)
        self.assertIn("HIPÓTESE", csv_texto)
