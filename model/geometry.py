"""Geometria retilínea; unidades SI, ângulo de entrada em graus."""
import math
from dataclasses import dataclass


def finito(nome, valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(valor):
        raise ValueError(f"{nome} deve ser um número real finito")
    return valor


def positivo(nome, valor):
    finito(nome, valor)
    if valor <= 0:
        raise ValueError(f"{nome} deve ser > 0")
    return valor


@dataclass(frozen=True)
class Geometria:
    modo: str
    theta_graus: float
    L_m: float
    H_m: float

    @property
    def theta_rad(self):
        return math.radians(self.theta_graus)


def geometria(modo, theta_graus, *, L_m=None, H_m=None):
    finito("theta_graus", theta_graus)
    if not 0 < theta_graus < 90:
        raise ValueError("theta_graus deve satisfazer 0 < theta < 90 graus")
    seno = math.sin(math.radians(theta_graus))
    if modo == "laboratorio":
        positivo("L_m", L_m)
        if H_m is not None:
            raise ValueError("laboratorio aceita somente L_m; H_m é calculado")
        H_m = L_m * seno
    elif modo == "terreno":
        positivo("H_m", H_m)
        if L_m is not None:
            raise ValueError("terreno aceita somente H_m; L_m é calculado")
        L_m = H_m / seno
    else:
        raise ValueError("modo deve ser 'laboratorio' ou 'terreno'")
    positivo("L_m calculado", L_m)
    positivo("H_m calculado", H_m)
    return Geometria(modo, theta_graus, L_m, H_m)
