"""Balanço energético explícito por transformação."""
from dataclasses import dataclass
from model.geometry import finito


@dataclass(frozen=True)
class EtapaEnergia:
    nome: str
    entrada_J: float
    saida_J: float
    perda_J: float
    eficiencia: float
    status: str


def balanço_transformacoes(energia_inicial_J, eficiencias):
    finito("energia_inicial_J", energia_inicial_J)
    if energia_inicial_J < 0:
        raise ValueError("energia_inicial_J deve ser >= 0")
    nomes = ("mecânica", "transmissão", "gerador", "retificador", "conversor", "carga")
    if len(eficiencias) != len(nomes):
        raise ValueError("são necessárias seis eficiências")
    energia = energia_inicial_J
    etapas = []
    for nome, eta in zip(nomes, eficiencias):
        finito(f"eficiencia_{nome}", eta)
        if not 0 < eta <= 1:
            raise ValueError(f"eficiência inválida na etapa {nome}")
        saida = energia * eta
        etapas.append(EtapaEnergia(nome, energia, saida, energia - saida, eta, "HIPÓTESE"))
        energia = saida
    return tuple(etapas)
