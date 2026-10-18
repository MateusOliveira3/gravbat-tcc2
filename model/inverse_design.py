"""Dimensionamento inverso com semântica explícita de potência e velocidade."""
import math
from model.geometry import finito, positivo


def dimensionar_configuracao(energia_Wh, potencia_W, duracao_s, altura_m,
                             eficiencia_global, velocidade_descida_m_s=0.02,
                             g_m_s2=9.81, theta_graus=None,
                             potencia_continua_W=None, duracao_pico_s=None):
    """Dimensiona energia e potência média; diagnostica pico sem duração.

    Sem theta_graus, a velocidade histórica é interpretada como vertical.
    Com ângulo, ela é velocidade ao longo do trilho.
    """
    valores = (("energia_Wh", energia_Wh), ("potencia_W", potencia_W),
               ("duracao_s", duracao_s), ("altura_m", altura_m),
               ("eficiencia_global", eficiencia_global),
               ("velocidade_descida_m_s", velocidade_descida_m_s))
    for nome, valor in valores:
        finito(nome, valor)
        positivo(nome, valor)
    if not 0 < eficiencia_global <= 1:
        raise ValueError("eficiencia_global deve satisfazer 0 < eta <= 1")
    velocidade_trilho_m_s = velocidade_descida_m_s
    velocidade_vertical_m_s = velocidade_trilho_m_s
    if theta_graus is not None:
        finito("theta_graus", theta_graus)
        if not 0 < theta_graus < 90:
            raise ValueError("theta_graus deve estar entre 0 e 90")
        velocidade_vertical_m_s *= math.sin(math.radians(theta_graus))
    energia_J = energia_Wh * 3600.0
    massa_energia = energia_J / (eficiencia_global * g_m_s2 * altura_m)
    potencia_media_W = energia_J / duracao_s
    massa_potencia_pico = potencia_W / (eficiencia_global * g_m_s2 * velocidade_vertical_m_s)
    massa_potencia_media = potencia_media_W / (eficiencia_global * g_m_s2 * velocidade_vertical_m_s)
    massa_requerida = max(massa_energia, massa_potencia_media)
    pico_sem_duracao = potencia_W > potencia_media_W and duracao_pico_s is None
    return {
        "massa_requerida_kg": massa_requerida,
        "massa_por_energia_kg": massa_energia,
        "massa_por_potencia_kg": massa_potencia_pico,
        "massa_por_potencia_pico_kg": massa_potencia_pico,
        "massa_por_potencia_media_kg": massa_potencia_media,
        "energia_armazenada_J": energia_J / eficiencia_global,
        "potencia_media_W": potencia_media_W,
        "potencia_continua_W": potencia_continua_W if potencia_continua_W is not None else potencia_media_W,
        "potencia_mecanica_estimada_W": massa_requerida * g_m_s2 * velocidade_vertical_m_s,
        "velocidade_descida_m_s": velocidade_trilho_m_s,
        "velocidade_trilho_m_s": velocidade_trilho_m_s,
        "velocidade_vertical_m_s": velocidade_vertical_m_s,
        "duracao_pico_s": duracao_pico_s,
        "altura_m": altura_m,
        "status": "DADOS_INSUFICIENTES" if pico_sem_duracao else "CALCULADO",
        "diagnostico": ("Potência de pico sem duração definida; atendimento do pico não pode ser declarado."
                        if pico_sem_duracao else "Requisitos energéticos e de potência compatíveis com as entradas."),
    }
