"""Solução analítica a partir do repouso, até antes de colisão/frenagem."""
import math
from dataclasses import dataclass
from model.geometry import geometria, finito, positivo
from model.mechanics import forcas, Forcas
from model.energy import energia, Energia
from config import G_M_S2


@dataclass(frozen=True)
class Estado:
    tempo_s: float
    posicao_m: float
    velocidade_m_s: float
    energia: Energia


@dataclass(frozen=True)
class Simulacao:
    massa_kg: float
    g_m_s2: float
    c_r: float
    geometria: object
    forcas: Forcas
    tempo_final_s: float | None

    def estado(self, tempo_s):
        finito("tempo_s", tempo_s)
        if tempo_s < 0 or (self.tempo_final_s is not None and tempo_s > self.tempo_final_s):
            raise ValueError("tempo_s deve estar entre zero e o fim da rampa")
        a = self.forcas.aceleracao_m_s2
        s = 0.5 * a * tempo_s ** 2 if a else 0.0
        v = a * tempo_s
        # Condição de contorno exata, evita extrapolação por arredondamento.
        if self.tempo_final_s is not None and tempo_s == self.tempo_final_s:
            s = self.geometria.L_m
        return Estado(tempo_s, s, v, energia(self.massa_kg, self.g_m_s2, self.geometria, self.forcas, s, v))

    def amostras(self, n=301):
        if isinstance(n, bool) or not isinstance(n, int) or n < 2:
            raise ValueError("n deve ser inteiro >= 2")
        if self.tempo_final_s is None:
            return (self.estado(0.0),)
        return tuple(self.estado(self.tempo_final_s * (i / (n - 1))) for i in range(n))


def simular(massa_kg, theta_graus, c_r, modo, *, L_m=None, H_m=None, g_m_s2=G_M_S2):
    geo = geometria(modo, theta_graus, L_m=L_m, H_m=H_m)
    f = forcas(massa_kg, g_m_s2, c_r, geo)
    tf = math.sqrt(2 * geo.L_m / f.aceleracao_m_s2) if f.status == "DESCE" else None
    if tf is not None:
        positivo("tempo_final_s calculado (limite numérico)", tf)
    resultado = Simulacao(massa_kg, g_m_s2, c_r, geo, f, tf)
    resultado.estado(tf if tf is not None else 0.0)
    return resultado
