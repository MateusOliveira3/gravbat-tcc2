import unittest
from model.electromechanics import ParametrosGerador
from model.electromechanical_coupling import acoplar_carga_resistiva
from simulation.cycle import ciclo_descida_subida
from simulation.simulator import simular


class TestCiclo(unittest.TestCase):
    def test_ciclo_completo_tem_saldo_e_tempos(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0, fases=2)
        ac, _, _ = acoplar_carga_resistiva(base, .05, 1.0, 1.0, p, 8.0)
        ciclo = ciclo_descida_subida(base, ac, 10.0)
        self.assertEqual(ciclo["status"], "COMPLETA")
        self.assertGreater(ciclo["tempo_subida_s"], 0.0)
        self.assertEqual(ciclo["saldo_liquido_J"], ciclo["energia_gerada_J"] - ciclo["energia_subida_J"])

    def test_subida_invalida(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0)
        ac, _, _ = acoplar_carga_resistiva(base, .05, 1.0, 1.0, p, 8.0)
        with self.assertRaises(ValueError): ciclo_descida_subida(base, ac, 0.0)

    def test_ciclo_aceita_energia_eletrica_integrada(self):
        base = simular(5.0, 10.0, .02, "laboratorio", L_m=1.2)
        p = ParametrosGerador(.1, 2.0)
        ac, _, _ = acoplar_carga_resistiva(base, .05, 1.0, 1.0, p, 8.0)
        ciclo = ciclo_descida_subida(base, ac, 10.0, energia_gerada_J=0.42,
                                     origem_energia="SIMULADO_DINAMICO_AC")
        self.assertAlmostEqual(ciclo["energia_gerada_J"], 0.42)
        self.assertEqual(ciclo["origem_energia"], "SIMULADO_DINAMICO_AC")
