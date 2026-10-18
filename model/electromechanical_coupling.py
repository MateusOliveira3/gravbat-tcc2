"""Acoplamento V0.5 quase estacionário entre carga elétrica e mecânica."""
from model.coupling import acoplar
from model.electromechanics import previa_carga_resistiva


def acoplar_carga_resistiva(base, raio_d_m, relacao_G, eta_transmissao,
                            parametros, resistencia_carga_ohm):
    """Aplica torque equivalente calculado na velocidade final sem carga."""
    referencia = base.tempo_final_s or 0.0
    velocidade = base.estado(referencia).velocidade_m_s
    omega_saida = relacao_G * velocidade / raio_d_m
    previa = previa_carga_resistiva(omega_saida, resistencia_carga_ohm, parametros)
    resultado = acoplar(base, previa["torque_resistente_Nm"], raio_d_m,
                        relacao_G, eta_transmissao)
    return resultado, previa, omega_saida
