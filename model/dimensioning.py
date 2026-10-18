"""Dimensionamento energético preliminar V0.7."""
from model.geometry import finito, positivo


def dimensionar_demanda(energia_util_kWh, potencia_max_kW, altura_m,
                        eficiencia_global, tempo_descarga_h,
                        massa_por_modulo_kg=None, velocidade_vertical_m_s=0.02,
                        duracao_pico_h=None):
    """Estima massa pela energia e módulos pela potência/energia.

    O resultado é uma ordem de grandeza calculada, não projeto executivo.
    """
    for nome, valor in (("energia_util_kWh", energia_util_kWh),
                        ("potencia_max_kW", potencia_max_kW),
                        ("altura_m", altura_m),
                        ("eficiencia_global", eficiencia_global),
                        ("tempo_descarga_h", tempo_descarga_h)):
        finito(nome, valor)
    positivo("energia_util_kWh", energia_util_kWh)
    positivo("potencia_max_kW", potencia_max_kW)
    positivo("altura_m", altura_m)
    positivo("tempo_descarga_h", tempo_descarga_h)
    positivo("velocidade_vertical_m_s", velocidade_vertical_m_s)
    if not 0 < eficiencia_global <= 1:
        raise ValueError("eficiencia_global deve satisfazer 0 < eta <= 1")
    if massa_por_modulo_kg is not None:
        positivo("massa_por_modulo_kg", massa_por_modulo_kg)
    energia_J = energia_util_kWh * 3_600_000
    massa_energia = energia_J / (eficiencia_global * 9.81 * altura_m)
    potencia_media_kW = energia_util_kWh / tempo_descarga_h
    massa_potencia_media = potencia_media_kW * 1000 / (eficiencia_global * 9.81 * velocidade_vertical_m_s)
    pico_sem_duracao = potencia_max_kW > potencia_media_kW and duracao_pico_h is None
    massa_pico = (potencia_max_kW * 1000 / (eficiencia_global * 9.81 * velocidade_vertical_m_s))
    massa_total = max(massa_energia, massa_potencia_media)
    modulos_energia = None if massa_por_modulo_kg is None else massa_total / massa_por_modulo_kg
    return {"massa_total_kg": massa_total, "massa_por_energia_kg": massa_energia,
            "massa_por_potencia_media_kg": massa_potencia_media,
            "massa_por_potencia_pico_kg": massa_pico,
            "potencia_media_kW": potencia_media_kW,
            "modulos_por_energia": modulos_energia,
            "potencia_max_kW": potencia_max_kW,
            "energia_util_kWh": energia_util_kWh,
            "velocidade_vertical_m_s": velocidade_vertical_m_s,
            "duracao_pico_h": duracao_pico_h,
            "status": "DADOS_INSUFICIENTES" if pico_sem_duracao else "CALCULADO"}
