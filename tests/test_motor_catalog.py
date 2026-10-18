import unittest
from model.motor_catalog import listar_motores, obter_motor


class TestCatalogoMotor(unittest.TestCase):
    def test_catalogo_inicial_e_explicitamente_hipotetico(self):
        motores = listar_motores()
        self.assertGreaterEqual(len(motores), 2)
        self.assertEqual(motores[0].status, "HIPÓTESE")
        self.assertIn("motor comercial", motores[0].observacao)
        self.assertEqual(motores[1].status, "DATASHEET-DERIVADO")
        self.assertAlmostEqual(motores[1].ke_Vs_rad, 2.2 / (20 * 3.141592653589793))

    def test_busca_por_id(self):
        motor = obter_motor("hipotetico_v05")
        self.assertEqual(motor.fases, 2)

    def test_id_inexistente(self):
        with self.assertRaises(ValueError):
            obter_motor("motor_real_inexistente")
