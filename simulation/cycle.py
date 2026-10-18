"""Balanço energético simplificado de um ciclo descida-subida V0.6."""
from model.geometry import finito, positivo


def ciclo_descida_subida(base, acoplamento_descida, potencia_subida_W,
                         eficiencia_subida=1.0, energia_gerada_J=None,
                         origem_energia="CALCULADO"):
    """Calcula o ciclo usando energia da descida e recarga prescrita.

    ``energia_gerada_J`` permite informar a energia elétrica integrada de uma
    trajetória dinâmica. Quando omitido, preserva a referência mecânica V0.4.
    """
    finito("potencia_subida_W", potencia_subida_W)
    positivo("potencia_subida_W", potencia_subida_W)
    finito("eficiencia_subida", eficiencia_subida)
    if not 0 < eficiencia_subida <= 1:
        raise ValueError("eficiencia_subida deve satisfazer 0 < eta <= 1")
    if acoplamento_descida.tempo_final_s is None:
        return {"status": "NAO_COMPLETA", "energia_gerada_J": 0.0,
                "energia_subida_J": 0.0, "saldo_liquido_J": 0.0}
    final = acoplamento_descida.estado(acoplamento_descida.tempo_final_s)
    if energia_gerada_J is None:
        energia_gerada = final["carga_J"]
        origem_energia = "CALCULADO_V04_MECANICO"
    else:
        finito("energia_gerada_J", energia_gerada_J)
        if energia_gerada_J < 0:
            raise ValueError("energia_gerada_J deve ser >= 0")
        energia_gerada = energia_gerada_J
    energia_potencial = base.massa_kg * base.g_m_s2 * base.geometria.H_m
    energia_subida = energia_potencial / eficiencia_subida
    tempo_subida = energia_subida / potencia_subida_W
    return {"status": "COMPLETA", "tempo_descida_s": acoplamento_descida.tempo_final_s,
            "tempo_subida_s": tempo_subida, "tempo_ciclo_s": acoplamento_descida.tempo_final_s + tempo_subida,
            "energia_gerada_J": energia_gerada, "energia_subida_J": energia_subida,
            "saldo_liquido_J": energia_gerada - energia_subida,
            "eficiencia_ciclo": energia_gerada / energia_subida if energia_subida else 0.0,
            "origem_energia": origem_energia}
