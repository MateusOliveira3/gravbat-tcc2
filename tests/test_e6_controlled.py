import unittest
from model.e6_controlled import controlado_torque, passivo_e4
class TestE6(unittest.TestCase):
 def test_meta_60_chegada_e_balanco(self):
  r=controlado_torque(6,1,10,.02,60)
  self.assertEqual(r.status,'CHEGADA'); self.assertAlmostEqual(r.residuo_J,0); self.assertAlmostEqual(r.v_media_m_s, r.L_m/60)
 def test_saturacao_bloqueia(self):
  r=controlado_torque(6,1,10,.02,60,tau_max_Nm=.01)
  self.assertEqual(r.status,'BLOQUEADO'); self.assertEqual(r.energia_carga_J,0)
 def test_passivo_referencia(self):
  r=passivo_e4(6,1,10,.02)
  self.assertEqual(r.status,'DESCE'); self.assertGreater(r.energia_carga_J,0); self.assertGreater(r.velocidade_final_m_s,0)
if __name__=='__main__': unittest.main()
