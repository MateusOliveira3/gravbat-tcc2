"""Métricas de aplicação com convenções cinemáticas explícitas."""
import math


def velocidade_vertical(velocidade_trilho_m_s, theta_graus):
    """Projeta velocidade ao longo do trilho no eixo vertical."""
    return velocidade_trilho_m_s * math.sin(math.radians(theta_graus))


def potencia_util_estimada(massa_kg, g_m_s2, velocidade_trilho_m_s,
                                theta_graus, eficiencia_global):
    """Potência útil estimada com eficiência global hipotética; não é potência elétrica medida."""
    return (massa_kg * g_m_s2 * velocidade_vertical(velocidade_trilho_m_s, theta_graus)
            * eficiencia_global)


def duracao_controlada_s(comprimento_rampa_m, velocidade_trilho_m_s):
    """Duração de uma descida a velocidade constante no trilho."""
    return comprimento_rampa_m / velocidade_trilho_m_s


def compatibilidade_autonomia(energia_util_Wh, duracao_s, duracao_descida_s):
    """Compara duração solicitada e duração mecânica de uma descarga."""
    return {
        "atende_duracao": duracao_descida_s >= duracao_s,
        "duracao_s": duracao_s,
        "duracao_descida_s": duracao_descida_s,
        "razao_duracao": duracao_descida_s / duracao_s,
        "energia_util_Wh": energia_util_Wh,
    }


