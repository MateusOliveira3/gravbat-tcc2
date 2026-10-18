import unittest
from model.electromechanics import ParametrosGerador
from model.electromechanical_coupling import acoplar_carga_resistiva
from simulation.simulator import simular


class TestAcoplamentoEletromecanico(unittest.TestCase):
    def test_carga_eletrica_reduz_aceleracao(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0, fases=2, eficiencia_retificador=.9)
        carga, previa, _ = acoplar_carga_resistiva(base, .05, 1.0, 1.0, p, 8.0)
        self.assertGreater(previa["torque_resistente_Nm"], 0.0)
        self.assertLess(carga.aceleracao_m_s2, base.forcas.aceleracao_m_s2)

    def test_carga_muito_resistiva_tende_a_zero(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0, fases=2)
        carga, _, _ = acoplar_carga_resistiva(base, .05, 1.0, 1.0, p, 1e9)
        self.assertGreaterEqual(carga.tau_carga_Nm, 0.0)
