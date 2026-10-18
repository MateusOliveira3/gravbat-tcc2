"""Comparação reproduzível de cenários de armazenamento."""
from model.dimensioning import dimensionar_demanda


def comparar_cenarios(cenarios):
    resultados = []
    for c in cenarios:
        r = dimensionar_demanda(c["energia_util_kWh"], c["potencia_max_kW"],
                                c["altura_m"], c["eficiencia_global"],
                                c["tempo_descarga_h"])
        resultados.append({**c, **r})
    return resultados
