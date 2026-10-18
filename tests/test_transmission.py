import math
import unittest
from model.transmission import cinematica, potencia_prescrita, rpm
from simulation.simulator import simular


class TestTransmissao(unittest.TestCase):
    def test_A_v_r_omega(self):
        c = cinematica(2, .5, 1)
        self.assertAlmostEqual(c.velocidade_linear_m_s, c.raio_d_m * c.omega_tambor_rad_s)

    def test_B_rpm(self):
        self.assertAlmostEqual(rpm(2 * math.pi), 60)

    def test_C_D_relacao(self):
        c = cinematica(1, .1, 3)
        self.assertAlmostEqual(c.omega_saida_rad_s, 3 * c.omega_tambor_rad_s)
        self.assertAlmostEqual(c.rpm_saida, c.rpm_tambor * 3)
        self.assertAlmostEqual(cinematica(1, .1, 1).rpm_saida, cinematica(1, .1, 1).rpm_tambor)

    def test_E_F_nao_altera_trajetoria(self):
        base = simular(6, 10, .02, "laboratorio", L_m=1.2)
        for raio in (.01, .05, .2):
            for g in (.25, 1, 4):
                # Cinemática só lê velocidade; a simulação segue igual.
                self.assertEqual(base.tempo_final_s, simular(6, 10, .02, "laboratorio", L_m=1.2).tempo_final_s)
                cinematica(base.estado(base.tempo_final_s).velocidade_m_s, raio, g)

    def test_G_H_I_J_K_L_M_validacao_e_potencia(self):
        for kwargs in ({"relacao_G": 0}, {"relacao_G": -1}, {"relacao_G": math.nan}, {"relacao_G": math.inf},
                       {"raio_d_m": 0}, {"raio_d_m": -1}, {"raio_d_m": math.nan}, {"raio_d_m": math.inf}):
            with self.assertRaises(ValueError):
                cinematica(1, kwargs.get("raio_d_m", .1), kwargs.get("relacao_G", 1))
        p = potencia_prescrita(2, 5, 2, 1)
        self.assertAlmostEqual(p.potencia_entrada_W, 10)
        self.assertAlmostEqual(p.potencia_saida_W, 10)
        self.assertAlmostEqual(p.torque_saida_Nm, 1)
        p = potencia_prescrita(2, 5, 2, .8)
        self.assertAlmostEqual(p.potencia_saida_W, 8)
        self.assertAlmostEqual(p.torque_saida_Nm, .8)
        for eta in (0, -1, 1.1, math.nan, math.inf):
            with self.assertRaises(ValueError):
                potencia_prescrita(1, 1, 1, eta)

