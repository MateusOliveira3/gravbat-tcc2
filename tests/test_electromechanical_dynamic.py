import unittest
from model.electromechanics import ParametrosGerador
from simulation.electromechanical_dynamic import simular_descida_eletromecanica
from simulation.simulator import simular


class TestDinamicaEletromecanica(unittest.TestCase):
    def test_sem_carga_eletrica_reproduz_descida(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0)
        r = simular_descida_eletromecanica(base, .05, 1.0, 1.0, p, 1e12, passo_s=.001)
        self.assertEqual(r["status"], "DESCE")
        self.assertAlmostEqual(r["estados"][-1]["posicao_m"], 1.2)
        self.assertAlmostEqual(r["estados"][-1]["velocidade_m_s"], base.estado(base.tempo_final_s).velocidade_m_s, delta=.01)

    def test_torque_e_corrente_aparecem(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0)
        r = simular_descida_eletromecanica(base, .05, 1.0, 1.0, p, 8.0, passo_s=.002)
        self.assertEqual(r["status"], "DESCE")
        self.assertGreater(r["estados"][-1]["torque_eletromagnetico_Nm"], 0.0)
        self.assertGreater(r["estados"][-1]["energia_acumulada_J"], 0.0)
        self.assertGreaterEqual(r["estados"][-1]["perda_cobre_acumulada_J"], 0.0)
