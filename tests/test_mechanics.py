import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from model.geometry import geometria
from simulation.simulator import simular


def caso(**kw):
    p = dict(massa_kg=6, theta_graus=10, c_r=0.02, modo="laboratorio", L_m=1.2)
    p.update(kw)
    return simular(**p)


class TesteMecanico(unittest.TestCase):
    def proximo(self, a, b):
        self.assertTrue(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), (a, b))

    def test_A_geometria_laboratorio(self):
        self.proximo(geometria("laboratorio", 30, L_m=1.2).H_m, 0.6)

    def test_B_geometria_terreno(self):
        self.proximo(geometria("terreno", 30, H_m=1).L_m, 2)

    def test_C_forca_gravitacional(self):
        f = caso(theta_graus=30).forcas
        self.proximo(f.grav_paralela_N, 29.43)
        self.proximo(f.normal_N, 6 * 9.81 * math.sqrt(3) / 2)

    def test_D_ideal(self):
        r = caso(c_r=0)
        e = r.estado(r.tempo_final_s)
        self.assertEqual(e.energia.perda_rolamento_J, 0)
        self.proximo(e.velocidade_m_s, math.sqrt(2 * 9.81 * r.geometria.H_m))
        self.proximo(e.energia.cinetica_J, e.energia.inicial_J)

    def test_E_balanco_durante_descida(self):
        for modo, dimensao in [("laboratorio", {"L_m": 1.2}), ("terreno", {"H_m": 1})]:
            for angulo in (5, 10, 15, 20, 25, 30):
                r = simular(6, angulo, .02, modo, **dimensao)
                for e in r.amostras(1001):
                    with self.subTest(modo=modo, angulo=angulo, t=e.tempo_s):
                        self.proximo(e.energia.inicial_J, e.energia.restante_J + e.energia.cinetica_J + e.energia.perda_rolamento_J)
                        self.assertLessEqual(abs(e.energia.residuo_energia_J), 1e-12)
                        self.assertGreaterEqual(e.energia.restante_J, -1e-12)

    def test_F_balanco_final_antes_colisao(self):
        r = caso()
        e = r.estado(r.tempo_final_s)
        self.proximo(e.posicao_m, 1.2)
        self.proximo(e.energia.restante_J, 0)
        self.assertGreater(e.energia.cinetica_J, 0)
        self.proximo(e.energia.inicial_J, e.energia.cinetica_J + e.energia.perda_rolamento_J)

    def test_G_nao_desce(self):
        r = caso(c_r=1)
        self.assertEqual(r.forcas.status, "NAO_DESCE")
        self.assertLess(r.forcas.disponivel_N, 0)
        self.assertEqual(r.forcas.aceleracao_m_s2, 0)
        self.assertIsNone(r.tempo_final_s)
        for t in (0, 1, 100, 1e200):
            e = r.estado(t)
            self.assertEqual((e.posicao_m, e.velocidade_m_s, e.energia.cinetica_J, e.energia.perda_rolamento_J, e.energia.residuo_energia_J), (0, 0, 0, 0, 0))
            self.assertEqual(e.energia.inicial_J, e.energia.restante_J)

    def test_H_cr_negativo(self):
        with self.assertRaisesRegex(ValueError, "c_r"):
            caso(c_r=-.01)

    def test_I_massa_invalida(self):
        for x in (0, -1):
            with self.subTest(massa=x), self.assertRaisesRegex(ValueError, "massa"):
                caso(massa_kg=x)

    def test_J_theta_zero_terreno(self):
        with self.assertRaisesRegex(ValueError, "theta"):
            simular(6, 0, .02, "terreno", H_m=1)

    def test_K_nao_finitos(self):
        for nome in ("massa_kg", "theta_graus", "c_r", "g_m_s2", "L_m"):
            for x in (math.nan, math.inf, -math.inf):
                with self.subTest(nome=nome, valor=x), self.assertRaisesRegex(ValueError, "finito"):
                    caso(**{nome: x})
        for x in (math.nan, math.inf, -math.inf):
            with self.subTest(H=x), self.assertRaisesRegex(ValueError, "finito"):
                simular(6, 10, .02, "terreno", H_m=x)

    def test_L_dimensoes_invalidas(self):
        for x in (0, -1, None):
            for modo, chave in (("laboratorio", "L_m"), ("terreno", "H_m")):
                with self.subTest(modo=modo, valor=x), self.assertRaises(ValueError):
                    simular(6, 10, .02, modo, **{chave: x})

    def test_M_limites_angulares(self):
        for x in (-1, 0, 90, 91):
            with self.subTest(theta=x), self.assertRaises(ValueError):
                caso(theta_graus=x)
        for x in (1e-6, 89.999999):
            r = caso(theta_graus=x, c_r=0)
            self.proximo(r.estado(r.tempo_final_s).energia.residuo_energia_J, 0)

    def test_N_transicao_partida(self):
        base = caso(c_r=0)
        critico = base.forcas.grav_paralela_N / base.forcas.normal_N
        self.assertEqual(caso(c_r=critico * (1 - 1e-9)).forcas.status, "DESCE")
        self.assertEqual(caso(c_r=critico * (1 + 1e-9)).forcas.status, "NAO_DESCE")
        self.assertEqual(caso(c_r=critico).forcas.status, "NAO_DESCE")

    def test_O_tempo_e_amostragem(self):
        r = caso()
        for t in (-1, math.inf, math.nan, r.tempo_final_s + 1):
            with self.subTest(t=t), self.assertRaises(ValueError):
                r.estado(t)
        for n in (0, 1, 2.5, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                r.amostras(n)

    def test_P_escala_massa(self):
        a, b = caso(), caso(massa_kg=12)
        self.proximo(a.tempo_final_s, b.tempo_final_s)
        self.proximo(2 * a.estado(0).energia.inicial_J, b.estado(0).energia.inicial_J)

    def test_Q_importacao_sem_efeitos(self):
        env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1]), PYTHONDONTWRITEBYTECODE="1")
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.run([sys.executable, "-B", "-c", "import simulation.simulator; import sys; assert not any(x in sys.modules for x in ('matplotlib','numpy','pandas','plotly','streamlit'))"], cwd=tmp, env=env, capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_R_entradas_ambiguas_e_tipos(self):
        for kw in ({"modo": "outro"}, {"H_m": 1}, {"massa_kg": True}, {"c_r": ".02"}, {"g_m_s2": 0}, {"g_m_s2": -1}):
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                caso(**kw)


if __name__ == "__main__":
    unittest.main()
