"""Balanço mecânico; resíduo numérico não é dissipação física."""
import math
from dataclasses import dataclass
from model.geometry import finito


@dataclass(frozen=True)
class Energia:
    inicial_J: float
    restante_J: float
    cinetica_J: float
    perda_rolamento_J: float
    residuo_energia_J: float


def energia(massa_kg, g_m_s2, geometria, forcas, s_m, v_m_s):
    inicial = massa_kg * g_m_s2 * geometria.H_m
    restante = massa_kg * g_m_s2 * (geometria.H_m - s_m * math.sin(geometria.theta_rad))
    cinetica = 0.5 * massa_kg * v_m_s ** 2
    perda = forcas.rol_movimento_N * s_m
    residuo = inicial - (restante + cinetica + perda)
    for x in (inicial, restante, cinetica, perda, residuo):
        finito("energia calculada (limite numérico)", x)
    return Energia(inicial, restante, cinetica, perda, residuo)
