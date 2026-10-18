"""Transmissão cinemática sem carga e balanço isolado de potência prescrita."""
import math
from dataclasses import dataclass
from model.geometry import finito, positivo

RPM_POR_RAD_S = 60.0 / (2.0 * math.pi)


def _positivo(nome, valor):
    positivo(nome, valor)
    return float(valor)


def rpm(rad_s):
    finito("rad_s", rad_s)
    return rad_s * RPM_POR_RAD_S


@dataclass(frozen=True)
class Cinematica:
    velocidade_linear_m_s: float
    raio_d_m: float
    omega_tambor_rad_s: float
    rpm_tambor: float
    relacao_G: float
    omega_saida_rad_s: float
    rpm_saida: float


def cinematica(velocidade_linear_m_s, raio_d_m, relacao_G):
    finito("velocidade_linear_m_s", velocidade_linear_m_s)
    raio_d_m = _positivo("raio_d_m", raio_d_m)
    relacao_G = _positivo("relacao_G", relacao_G)
    omega = velocidade_linear_m_s / raio_d_m
    return Cinematica(velocidade_linear_m_s, raio_d_m, omega, rpm(omega),
                      relacao_G, relacao_G * omega, relacao_G * rpm(omega))


@dataclass(frozen=True)
class PotenciaPrescrita:
    torque_entrada_Nm: float
    omega_entrada_rad_s: float
    relacao_G: float
    eta_transmissao: float
    potencia_entrada_W: float
    potencia_saida_W: float
    torque_saida_Nm: float
    perda_transmissao_W: float


def potencia_prescrita(torque_entrada_Nm, omega_entrada_rad_s, relacao_G, eta_transmissao):
    finito("torque_entrada_Nm", torque_entrada_Nm)
    finito("omega_entrada_rad_s", omega_entrada_rad_s)
    relacao_G = _positivo("relacao_G", relacao_G)
    finito("eta_transmissao", eta_transmissao)
    if not 0 < eta_transmissao <= 1:
        raise ValueError("eta_transmissao deve satisfazer 0 < eta <= 1")
    p_in = torque_entrada_Nm * omega_entrada_rad_s
    p_out = eta_transmissao * p_in
    omega_out = relacao_G * omega_entrada_rad_s
    torque_out = 0.0 if omega_out == 0 else p_out / omega_out
    return PotenciaPrescrita(torque_entrada_Nm, omega_entrada_rad_s, relacao_G,
                             eta_transmissao, p_in, p_out, torque_out,
                             p_in - p_out)
