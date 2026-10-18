"""Testes da adaptação não visual; sem servidor ou browser."""
import unittest
from unittest.mock import patch
from simulation.simulator import simular
from dashboard.scenarios import interpretar, perda_percentual, varrer_inclinacao


class TestDashboard(unittest.TestCase):
    def test_sweep_lab_usa_nucleo_em_45_pontos(self):
        r = simular(6, 10, .02, "laboratorio", L_m=1.2)
        with patch("dashboard.scenarios.simular", wraps=simular) as motor:
            linhas = varrer_inclinacao(r)
        self.assertEqual(motor.call_count, 45)
        self.assertEqual([p["theta_graus"] for p in linhas], list(range(1, 46)))
        self.assertTrue(all(p["L_m"] == 1.2 for p in linhas))
        self.assertLess(linhas[0]["H_m"], linhas[-1]["H_m"])
        self.assertEqual(linhas[0]["status"], "NAO_DESCE")
        self.assertIsNone(linhas[0]["tempo_descida_s"])
        self.assertEqual(linhas[0]["perda_percentual"], 0)

    def test_sweep_terreno_preserva_altura_e_parametros(self):
        r = simular(12, 10, .03, "terreno", H_m=2, g_m_s2=9.8)
        linhas = varrer_inclinacao(r)
        self.assertTrue(all(p["H_m"] == 2 for p in linhas))
        self.assertGreater(linhas[0]["L_m"], linhas[-1]["L_m"])
        esperado = simular(12, 30, .03, "terreno", H_m=2, g_m_s2=9.8)
        self.assertEqual(linhas[29]["tempo_descida_s"], esperado.tempo_final_s)
        self.assertEqual(linhas[29]["perda_percentual"], perda_percentual(esperado))

    def test_perda_bloqueado_e_ideal(self):
        for cr in (0, 1):
            self.assertEqual(perda_percentual(simular(6, 10, cr, "laboratorio", L_m=1.2)), 0)

    def test_interpretacao_deterministica_descida(self):
        r = simular(6, 10, .02, "terreno", H_m=1)
        texto = interpretar(r)
        self.assertEqual(texto, interpretar(r))
        for trecho in ("6 kg", "10°", "58,86 J", "maior comprimento", "energia cinética final"):
            self.assertIn(trecho, texto)
        self.assertNotIn("elétrica", texto)
        self.assertNotIn("útil", texto)

    def test_interpretacao_bloqueio(self):
        texto = interpretar(simular(6, 10, 1, "laboratorio", L_m=1.2))
        for trecho in ("NAO_DESCE", "0 J (0%)", "permanece armazenada", "velocidade é zero"):
            self.assertIn(trecho, texto)

    def test_sweep_todos_bloqueados(self):
        linhas = varrer_inclinacao(simular(6, 10, 2, "terreno", H_m=1))
        self.assertTrue(all(p["status"] == "NAO_DESCE" and p["tempo_descida_s"] is None and p["perda_percentual"] == 0 for p in linhas))
