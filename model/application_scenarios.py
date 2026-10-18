"""Cenários de aplicação para exploração preliminar do GravBat.

Os valores são referências de entrada marcadas como HIPÓTESE; não representam
medições de consumo nem projetos de instalações reais.
"""

SCENARIOS = {
    "Casa de baixa demanda": {
        "energia_util_kWh": 8.0,
        "potencia_max_kW": 2.0,
        "altura_m": 100.0,
        "tempo_descarga_h": 4.0,
        "eficiencia_global": 0.55,
        "status": "HIPÓTESE",
        "observacao": "Demanda diária simplificada para exploração acadêmica.",
    },
    "Instalação comunitária": {
        "energia_util_kWh": 500.0,
        "potencia_max_kW": 100.0,
        "altura_m": 200.0,
        "tempo_descarga_h": 5.0,
        "eficiencia_global": 0.55,
        "status": "HIPÓTESE",
        "observacao": "Cenário paramétrico; deve ser substituído por curva de carga.",
    },
    "Cenário urbano exploratório": {
        "energia_util_kWh": 10000.0,
        "potencia_max_kW": 2000.0,
        "altura_m": 800.0,
        "tempo_descarga_h": 8.0,
        "eficiencia_global": 0.55,
        "status": "HIPÓTESE",
        "observacao": "Escala exploratória inspirada em desnível; não é demanda de uma cidade medida.",
    },
}


def obter_cenario(nome):
    """Retorna uma cópia do cenário para evitar alterações globais."""
    if nome not in SCENARIOS:
        raise ValueError("cenário de aplicação desconhecido")
    return dict(SCENARIOS[nome])
