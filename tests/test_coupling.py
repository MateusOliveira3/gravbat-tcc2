import math, unittest
from simulation.simulator import simular
from model.coupling import acoplar, varrer_torque

class TestAcoplamento(unittest.TestCase):
    def setUp(self): self.base=simular(6,10,.02,'laboratorio',L_m=1.2)
    def test_A_N_zero_reproduz(self):
        c=acoplar(self.base,0,.05,1,1); self.assertAlmostEqual(c.tempo_final_s,self.base.tempo_final_s); self.assertEqual(c.estado(c.tempo_final_s)['carga_J'],0)
    def test_B_C_forcas(self):
        c=acoplar(self.base,.1,.05,2,.8); self.assertAlmostEqual(c.forca_carga_N,5); self.assertAlmostEqual(c.torque_tambor_resistente_Nm,.25)
    def test_D_E_limite(self):
        c=acoplar(self.base,.01,.05,1,1); self.assertLess(c.aceleracao_m_s2,self.base.forcas.aceleracao_m_s2)
        l=acoplar(self.base,c.torque_limite_v04_Nm,.05,1,1); self.assertEqual(l.status,'NAO_DESCE_COM_CARGA')
        self.assertEqual(acoplar(self.base,c.torque_limite_v04_Nm*1.01,.05,1,1).status,'NAO_DESCE_COM_CARGA')
    def test_F_G_P(self):
        for tau in (-1,math.nan,math.inf):
            with self.assertRaises(ValueError): acoplar(self.base,tau,.05,1,1)
        for eta in (0,1.1,math.nan,math.inf):
            with self.assertRaises(ValueError): acoplar(self.base,.1,.05,1,eta)
    def test_H_I_J_K_L_M_N_O(self):
        c=acoplar(self.base,.1,.05,2,.8); e=c.estado(c.tempo_final_s)
        self.assertAlmostEqual(e['carga_J'],.1*2*c.base.geometria.L_m/.05)
        self.assertAlmostEqual(e['entrada_transmissao_J'],c.forca_carga_N*c.base.geometria.L_m)
        self.assertGreaterEqual(e['perda_transmissao_J'],0)
        self.assertAlmostEqual(e['residuo_J'],0,delta=1e-12)
        self.assertAlmostEqual(e['potencia_carga_W']*c.tempo_final_s/2,e['carga_J'],delta=1e-10)
        z=acoplar(self.base,0,.05,2,.8).estado(acoplar(self.base,0,.05,2,.8).tempo_final_s); self.assertEqual(z['carga_J'],0); self.assertEqual(z['perda_transmissao_J'],0)

    def test_maximo_analitico_independente(self):
        eta=.9; var=varrer_torque(self.base,.05,1,eta,2001)
        melhor=max((p for p in var if p['status']=='DESCE_COM_CARGA'),key=lambda p:p['potencia_media_W'])
        limite=var[0]['limite_Nm']; esperado=2*limite/3
        self.assertLess(abs(melhor['tau_carga_Nm']/esperado-1), .002)
        self.assertAlmostEqual(var[0]['potencia_media_W'],0)
        self.assertEqual(var[-1]['status'],'NAO_DESCE_COM_CARGA')
