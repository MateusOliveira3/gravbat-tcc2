import math
import unittest
from model.inverse_design import dimensionar_configuracao
from model.electromechanics import ParametrosGerador, previa_carga_resistiva
from model.dimensioning import dimensionar_demanda
from simulation.simulator import simular
from simulation.electromechanical_dynamic import simular_descida_eletromecanica


class TestCorrecoesP0(unittest.TestCase):
    def test_pico_sem_duracao_nao_declara_atendimento(self):
        r = dimensionar_configuracao(1, 1000, 3600, 10, .5, .02)
        self.assertEqual(r["status"], "DADOS_INSUFICIENTES")
        self.assertAlmostEqual(r["massa_por_potencia_pico_kg"], 1000/(.5*9.81*.02), places=6)
        self.assertAlmostEqual(r["massa_por_energia_kg"], 3600/(.5*9.81*10), places=6)

    def test_velocidade_trilho_tem_componente_vertical(self):
        r = dimensionar_configuracao(1, 10, 3600, 10, .5, .02, theta_graus=30)
        self.assertAlmostEqual(r["velocidade_vertical_m_s"], .01)

    def test_balanco_eletromagnetico(self):
        p = ParametrosGerador(.1, 2.0, fases=2, eficiencia_retificador=.9)
        r = previa_carga_resistiva(20, 8.0, p)
        self.assertAlmostEqual(r["potencia_em_W"], r["potencia_cobre_W"] + r["potencia_carga_W"])
        self.assertGreaterEqual(r["potencia_cobre_W"], 0.0)
        self.assertAlmostEqual(r["torque_resistente_Nm"], r["potencia_em_W"] / 20)

    def test_dimensionadores_tem_mesma_massa_de_energia(self):
        a = dimensionar_configuracao(10, 10, 3600, 5, .8, .02)
        b = dimensionar_demanda(0.01, 0.01, 5, .8, 1, velocidade_vertical_m_s=.02)
        self.assertAlmostEqual(a["massa_por_energia_kg"], b["massa_por_energia_kg"], places=9)
        self.assertAlmostEqual(a["massa_por_potencia_media_kg"], b["massa_por_potencia_media_kg"], places=9)

    def test_desaceleracao_para_antes_do_final(self):
        base = simular(1.0, 10.0, .02, "laboratorio", L_m=10.0)
        p = ParametrosGerador(10.0, .01)
        r = simular_descida_eletromecanica(base, .05, 1.0, 1.0, p, 1e-6, passo_s=.001, velocidade_inicial_m_s=.1)
        self.assertEqual(r["status"], "PARA")
        velocidades = [e["velocidade_m_s"] for e in r["estados"]]
        self.assertGreater(velocidades[0], 0.0)
        self.assertLess(velocidades[-1], velocidades[0])
        self.assertEqual(velocidades[-1], 0.0)
        self.assertLess(r["estados"][-1]["posicao_m"], 10.0)
        self.assertGreaterEqual(r["estados"][-1]["energia_acumulada_J"], 0.0)

    def test_convergencia_temporal_reproduzivel(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0)
        resultados = [simular_descida_eletromecanica(base, .05, 1.0, 1.0, p, 8.0, passo_s=dt)
                      for dt in (.004, .002, .001)]
        for r in resultados:
            self.assertEqual(r["status"], "DESCE")
            self.assertAlmostEqual(r["estados"][-1]["posicao_m"], 1.2, places=12)
        self.assertLess(abs(resultados[1]["estados"][-1]["velocidade_m_s"] - resultados[2]["estados"][-1]["velocidade_m_s"]), .005)
        self.assertLess(abs(resultados[1]["estados"][-1]["energia_acumulada_J"] - resultados[2]["estados"][-1]["energia_acumulada_J"]), .005)


if __name__ == "__main__":
    unittest.main()
