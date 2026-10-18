import math
import unittest
from model.electromechanics import (ParametrosGerador, fem_fase,
    fase_carregada, torque_eletromagnetico, potencia_cc,
    previa_carga_resistiva)


class TestEletromecanicaMinima(unittest.TestCase):
    def setUp(self):
        self.p = ParametrosGerador(0.1, 2.0, fases=2, eficiencia_retificador=0.9)

    def test_fem_e_proporcional_a_velocidade(self):
        self.assertAlmostEqual(fem_fase(20, self.p, theta_eletrico_rad=math.pi/2), 2.0)
        self.assertAlmostEqual(fem_fase(40, self.p, theta_eletrico_rad=math.pi/2), 4.0)

    def test_fases_tem_deslocamento(self):
        self.assertAlmostEqual(fem_fase(10, self.p, 0, math.pi/2), 1.0)
        self.assertAlmostEqual(fem_fase(10, self.p, 1, math.pi/2), -1.0)

    def test_resistencia_reduz_tensao_terminal(self):
        self.assertAlmostEqual(fase_carregada(20, .25, self.p, theta_eletrico_rad=math.pi/2), 1.5)

    def test_torque_por_potencia_eletromagnetica(self):
        self.assertAlmostEqual(torque_eletromagnetico(20, 2.0, .5), .05)
        self.assertEqual(torque_eletromagnetico(0, 2.0, .5), 0.0)

    def test_retificador_separado(self):
        self.assertAlmostEqual(potencia_cc(10, self.p), 9.0)

    def test_parametros_invalidos(self):
        with self.assertRaises(ValueError): ParametrosGerador(0, 2)
        with self.assertRaises(ValueError): ParametrosGerador(0.1, 2, fases=0)
        with self.assertRaises(ValueError): ParametrosGerador(0.1, 2, eficiencia_retificador=1.1)

    def test_previa_carga_resistiva(self):
        r = previa_carga_resistiva(20, 8.0, self.p)
        self.assertAlmostEqual(r["fem_pico_V"], 2.0)
        self.assertGreater(r["corrente_pico_A"], 0.0)
        self.assertAlmostEqual(r["potencia_cc_W"], .9 * r["potencia_ac_W"])
        self.assertGreater(r["torque_resistente_Nm"], 0.0)

