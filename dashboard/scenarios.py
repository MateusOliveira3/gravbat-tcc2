"""Adaptação não visual: todas as trajetórias/forças vêm do núcleo V0.1."""
from simulation.simulator import simular


def perda_percentual(resultado):
    e = resultado.estado(resultado.tempo_final_s or 0.0).energia
    return 100 * e.perda_rolamento_J / e.inicial_J


def varrer_inclinacao(resultado):
    geo = resultado.geometria
    dimensao = {"L_m": geo.L_m} if geo.modo == "laboratorio" else {"H_m": geo.H_m}
    linhas = []
    for theta in range(1, 46):
        r = simular(resultado.massa_kg, theta, resultado.c_r, geo.modo,
                    g_m_s2=resultado.g_m_s2, **dimensao)
        linhas.append({"theta_graus": theta, "L_m": r.geometria.L_m,
                       "H_m": r.geometria.H_m, "status": r.forcas.status,
                       "perda_percentual": perda_percentual(r),
                       "tempo_descida_s": r.tempo_final_s})
    return linhas


def numero(valor):
    """Formato compacto para a interface; tabelas técnicas preservam detalhes."""
    valor = float(valor)
    if abs(valor) >= 1000:
        return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if abs(valor) >= 100:
        return f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{valor:.4g}".replace(".", ",")


def interpretar(r):
    e = r.estado(r.tempo_final_s or 0.0).energia
    texto = (f"Com massa de {numero(r.massa_kg)} kg e inclinação de "
             f"{numero(r.geometria.theta_graus)}°, o desnível é "
             f"{numero(r.geometria.H_m)} m e a energia potencial inicial é "
             f"{numero(e.inicial_J)} J. ")
    if r.tempo_final_s is None:
        texto += ("NAO_DESCE sob a aproximação de partida V0.1. Não há percurso: "
                  "a perda real por rolamento é 0 J (0%); toda a energia potencial "
                  "permanece armazenada. A velocidade é zero e o fim da rampa não é alcançado. ")
    else:
        texto += (f"Até o fim da rampa, o rolamento dissipa {numero(e.perda_rolamento_J)} J "
                  f"({numero(perda_percentual(r))}% da energia inicial). "
                  f"A descida dura {numero(r.tempo_final_s)} s. "
                  "A energia cinética final permanece no corpo antes de qualquer frenagem. ")
    if r.geometria.modo == "terreno":
        texto += ("Neste modo, o desnível permanece fixo: uma inclinação menor exige "
                  "maior comprimento de rampa para vencer o mesmo desnível.")
    else:
        texto += "Neste modo, o comprimento permanece fixo: mudar a inclinação muda o desnível e a energia inicial."
    return texto
