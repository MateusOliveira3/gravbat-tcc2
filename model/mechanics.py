"""Forças constantes. Critério de partida é aproximação da V0.1."""
import math
from dataclasses import dataclass
from model.geometry import positivo, finito


@dataclass(frozen=True)
class Forcas:
    normal_N: float
    grav_paralela_N: float
    rol_movimento_N: float
    disponivel_N: float
    aceleracao_m_s2: float
    status: str


def forcas(massa_kg, g_m_s2, c_r, geometria):
    positivo("massa_kg", massa_kg)
    positivo("g_m_s2", g_m_s2)
    finito("c_r", c_r)
    if c_r < 0:
        raise ValueError("c_r deve ser >= 0")
    peso = massa_kg * g_m_s2
    normal = peso * math.cos(geometria.theta_rad)
    grav = peso * math.sin(geometria.theta_rad)
    rol = c_r * normal
    disponivel = grav - rol
    a = disponivel / massa_kg if disponivel > 0 else 0.0
    for nome, valor in [("peso", peso), ("normal", normal), ("grav", grav), ("rol", rol), ("disponivel", disponivel), ("aceleracao", a)]:
        finito(f"resultado {nome} (limite numérico)", valor)
    if disponivel > 0:
        positivo("aceleracao calculada", a)
    return Forcas(normal, grav, rol, disponivel, a, "DESCE" if disponivel > 0 else "NAO_DESCE")
