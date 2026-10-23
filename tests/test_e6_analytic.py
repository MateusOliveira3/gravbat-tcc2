import unittest
from model.e6_analytic import referencia
class TestE6Analitico(unittest.TestCase):
 def test_banco_10_g1(self):
  o,e=referencia(6,1,10,.02)
  self.assertAlmostEqual(o.b_Ns_m,.4444444444,8); self.assertAlmostEqual(o.tempo_s,2.858997,4); self.assertAlmostEqual(e['residuo'],0,10)
 def test_banco_g1457(self):
  o,e=referencia(6,1,10,.02,G=14.5671456214)
  self.assertAlmostEqual(o.tempo_s,60,3); self.assertAlmostEqual(e['Eac'],37.55237,3)
if __name__=='__main__':unittest.main()
