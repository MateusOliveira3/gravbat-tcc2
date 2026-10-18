"""Modelo eletromecânico mínimo V0.5, parametrizado e sem dados de motor."""
import math
from dataclasses import dataclass
from model.geometry import finito, positivo


@dataclass(frozen=True)
class ParametrosGerador:
    """Parâmetros a obter por medição/datasheet ou declarar como hipótese."""
    ke_Vs_rad: float
    resistencia_fase_ohm: float
    fases: int = 2
    eficiencia_retificador: float = 1.0

    def __post_init__(self):
        positivo("ke_Vs_rad", self.ke_Vs_rad)
        positivo("resistencia_fase_ohm", self.resistencia_fase_ohm)
        if isinstance(self.fases, bool) or not isinstance(self.fases, int) or self.fases < 1:
            raise ValueError("fases deve ser inteiro >= 1")
        finito("eficiencia_retificador", self.eficiencia_retificador)
        if not 0 < self.eficiencia_retificador <= 1:
            raise ValueError("eficiencia_retificador deve satisfazer 0 < eta <= 1")


def fem_fase(omega_rad_s, parametros, fase=0, theta_eletrico_rad=0.0):
    """FEM senoidal de circuito aberto; forma de onda é hipótese V0.5."""
    finito("omega_rad_s", omega_rad_s)
    if isinstance(fase, bool) or not isinstance(fase, int) or not 0 <= fase < parametros.fases:
        raise ValueError("fase fora do intervalo")
    deslocamento = 2 * math.pi * fase / parametros.fases
    return parametros.ke_Vs_rad * omega_rad_s * math.sin(theta_eletrico_rad + deslocamento)


def fase_carregada(omega_rad_s, corrente_A, parametros, fase=0, theta_eletrico_rad=0.0):
    """Tensão terminal de fase em carga resistiva no modelo reduzido."""
    finito("corrente_A", corrente_A)
    e = fem_fase(omega_rad_s, parametros, fase, theta_eletrico_rad)
    return e - parametros.resistencia_fase_ohm * corrente_A


def torque_eletromagnetico(omega_rad_s, fem_V, corrente_A):
    """Torque resistente obtido por potência FEM/velocidade."""
    finito("omega_rad_s", omega_rad_s)
    finito("fem_V", fem_V)
    finito("corrente_A", corrente_A)
    if omega_rad_s == 0:
        return 0.0
    return fem_V * corrente_A / omega_rad_s


def potencia_cc(potencia_ac_W, parametros):
    finito("potencia_ac_W", potencia_ac_W)
    if potencia_ac_W < 0:
        raise ValueError("potencia_ac_W deve ser >= 0")
    return parametros.eficiencia_retificador * potencia_ac_W


def previa_carga_resistiva(omega_rad_s, resistencia_carga_ohm, parametros):
    """Estimativa de bancada com FEM de pico e carga resistiva equivalente.

    A aproximação usa uma fase equivalente e multiplica a potência média
    senoidal por ``fases``. Não representa ainda a ponte retificadora real.
    """
    finito("omega_rad_s", omega_rad_s)
    positivo("resistencia_carga_ohm", resistencia_carga_ohm)
    e_pico = abs(parametros.ke_Vs_rad * omega_rad_s)
    corrente_pico = e_pico / (parametros.resistencia_fase_ohm + resistencia_carga_ohm)
    potencia_carga_W = parametros.fases * .5 * corrente_pico**2 * resistencia_carga_ohm
    potencia_cobre_W = parametros.fases * .5 * corrente_pico**2 * parametros.resistencia_fase_ohm
    potencia_em_W = potencia_carga_W + potencia_cobre_W
    potencia_cc_W = potencia_cc(potencia_carga_W, parametros)
    torque_Nm = 0.0 if omega_rad_s == 0 else potencia_em_W / abs(omega_rad_s)
    return {"fem_pico_V": e_pico, "corrente_pico_A": corrente_pico,
            "potencia_ac_W": potencia_carga_W, "potencia_carga_W": potencia_carga_W,
            "potencia_cobre_W": potencia_cobre_W, "potencia_em_W": potencia_em_W,
            "potencia_cc_W": potencia_cc_W, "torque_resistente_Nm": torque_Nm}
