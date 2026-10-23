import unittest
import re

from dashboard.layout import animacao_interativa_html, svg_rampa_compacta, preparar_contrato_trajetoria
from dashboard import charts
from simulation.simulator import simular


class TestLayoutDashboard(unittest.TestCase):
    def test_chamada_do_dashboard_com_cinco_argumentos(self):
        # Reproduz a chamada da tela principal e garante compatibilidade da integração.
        svg = svg_rampa_compacta(11.52, 2.0, 0.52, 10.0, 5.99)
        self.assertIn("<svg", svg)
        self.assertIn("L = 11.52 m", svg)
        self.assertIn("H = 2.00 m", svg)

    def test_posicoes_inicial_intermediaria_final(self):
        for posicao in (0.0, 5.0, 10.0):
            svg = svg_rampa_compacta(10.0, 5.0, 0.5, 30.0, posicao)
            self.assertIn("<rect", svg)
            self.assertIn("<line", svg)

    def test_graficos_marcados_usam_a_mesma_trajetoria(self):
        estados = simular(6, 30, 0.02, "terreno", H_m=2).amostras(20)
        velocidade = charts.velocidade_tempo_marcada(estados, estados[5].tempo_s, 0.02, 100.0)
        energia = charts.energia_posicao_marcada(estados, estados[5].posicao_m)
        self.assertTrue(velocidade.data)
        self.assertTrue(energia.data)

    def test_componente_interativo_tem_relogio_e_controles(self):
        estados = simular(6, 30, 0.02, "terreno", H_m=2).amostras(8)
        html = animacao_interativa_html(4.0, 2.0, 30.0, estados)
        for trecho in ("requestAnimationFrame", "gb-play", "gb-pause", "gb-reset", "gb-seek", "gb-cabo", "gb-carro", "gb-massa", "gb-gear-big", "gb-gear-small", "gb-chart", "gb-marker", "chartSelect"):
            self.assertIn(trecho, html)
        self.assertEqual(html.count('<circle cx="-20"'), 1)
        self.assertEqual(html.count('<circle cx="20"'), 1)
        self.assertIn("rotate('+(-theta*180/Math.PI)+')", html)

    def test_cota_e_angulo_usam_geometria_do_cenario(self):
        svg = svg_rampa_compacta(10.0, 10.0 * 0.173648, 0.5, theta_graus=10.0)
        self.assertIn("H = 1.74 m", svg)
        self.assertIn("θ = 10.0°", svg)

    def test_posicao_permanece_no_trilho(self):
        svg = svg_rampa_compacta(10.0, 2.0, 0.5, theta_graus=30.0, posicao_m=5.0)
        self.assertIn("aria-label='Representação esquemática", svg)
        self.assertIn("L = 10.00 m", svg)

    def test_animacao_usa_interpolacao_unica_e_rodas_nos_dois_trilhos(self):
        estados = simular(6, 10, 0.02, "terreno", H_m=2).amostras(8)
        html = animacao_interativa_html(11.52, 2.0, 10.0, estados)
        self.assertIn("u=Math.max(0,Math.min(1,z.s/L))", html)
        self.assertIn("x=x1+u*(x0-x1),y=y1+u*(y0-y1)", html)
        self.assertIn("nx=-Math.sin(theta),ny=Math.cos(theta)", html)
        self.assertIn('cy="0"', html)
        self.assertIn('cy="22"', html)
        self.assertIn("ax=x+11*nx,ay=y+11*ny", html)

    def test_contrato_explicitamente_separa_geometria_mecanica_trajetoria(self):
        estados = simular(6, 30, 0.02, "terreno", H_m=2).amostras(8)
        contrato = preparar_contrato_trajetoria(4.0, 2.0, 30.0, estados, massa_kg=6, cr=0.02)
        self.assertEqual(set(contrato), {"geometry", "mechanical", "trajectory", "metadata"})
        self.assertEqual(contrato["trajectory"]["mode"], "free")
        self.assertEqual(contrato["trajectory"]["samples"][0]["s_m"], 0.0)
        self.assertLessEqual(contrato["trajectory"]["samples"][-1]["s_m"], 4.0)

    def test_componente_tem_um_unico_elemento_linear_de_cabo_e_rotulos_dinamicos(self):
        estados = simular(6, 10, 0.02, "terreno", H_m=2).amostras(8)
        html = animacao_interativa_html(11.52, 2.0, 10.0, estados)
        cabos = re.findall(r'<line[^>]*id="gb-cabo"[^>]*>', html)
        self.assertEqual(len(cabos), 1)
        self.assertIn('id="gb-chart-x"', html)
        self.assertIn('id="gb-chart-y"', html)
        self.assertIn("chartX.textContent=energy?", html)


if __name__ == "__main__":
    unittest.main()
