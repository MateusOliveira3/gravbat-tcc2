"""Geometria preliminar do cabo e do tambor."""
import math
from dataclasses import dataclass
from model.geometry import positivo


@dataclass(frozen=True)
class GeometriaCabo:
    tipo: str
    diametro_cabo_m: float
    diametro_nucleo_m: float
    comprimento_disponivel_m: float

    def __post_init__(self):
        if not self.tipo.strip():
            raise ValueError("tipo deve ser informado")
        positivo("diametro_cabo_m", self.diametro_cabo_m)
        positivo("diametro_nucleo_m", self.diametro_nucleo_m)
        positivo("comprimento_disponivel_m", self.comprimento_disponivel_m)

    @property
    def raio_nucleo_m(self):
        return self.diametro_nucleo_m / 2

    @property
    def voltas_estimadas_primeira_camada(self):
        return self.comprimento_disponivel_m / (math.pi * self.diametro_nucleo_m)
