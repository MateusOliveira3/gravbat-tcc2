"""Integração numérica V0.5 com torque elétrico dependente da velocidade."""
from model.electromechanics import previa_carga_resistiva


def simular_descida_eletromecanica(base, raio_d_m, relacao_G,
                                   eta_transmissao, parametros,
                                   resistencia_carga_ohm, passo_s=0.002,
                                   max_passos=200000, velocidade_inicial_m_s=0.0):
    if passo_s <= 0:
        raise ValueError("passo_s deve ser > 0")
    if base.tempo_final_s is None:
        return {"status": "NAO_DESCE", "estados": ({"tempo_s": 0.0, "posicao_m": 0.0, "velocidade_m_s": 0.0},)}
    dt = passo_s
    t = 0.0
    s = 0.0
    if velocidade_inicial_m_s < 0:
        raise ValueError("velocidade_inicial_m_s deve ser >= 0")
    v = velocidade_inicial_m_s
    estados = []
    energia_acumulada = 0.0
    energia_resistiva = 0.0
    potencia_anterior = 0.0
    perda_anterior = 0.0
    for _ in range(max_passos):
        omega = relacao_G * v / raio_d_m
        previa = previa_carga_resistiva(omega, resistencia_carga_ohm, parametros)
        forca_carga = relacao_G * previa["torque_resistente_Nm"] / (eta_transmissao * raio_d_m)
        a = (base.forcas.disponivel_N - forca_carga) / base.massa_kg
        energia_acumulada += 0.5 * (potencia_anterior + previa["potencia_em_W"]) * dt
        perda_cobre = parametros.resistencia_fase_ohm * previa["corrente_pico_A"]**2 * parametros.fases * .5
        energia_resistiva += 0.5 * (perda_anterior + perda_cobre) * dt
        estados.append({"tempo_s": t, "posicao_m": s, "velocidade_m_s": v,
                        "aceleracao_m_s2": a, "omega_saida_rad_s": omega,
                        "torque_eletromagnetico_Nm": previa["torque_resistente_Nm"],
                        "potencia_ac_W": previa["potencia_carga_W"],
                        "potencia_em_W": previa["potencia_em_W"],
                        "energia_acumulada_J": energia_acumulada,
                        "perda_cobre_acumulada_J": energia_resistiva})
        if s >= base.geometria.L_m:
            estados[-1]["posicao_m"] = base.geometria.L_m
            return {"status": "DESCE", "estados": tuple(estados)}
        v_novo = v + a * dt
        if v_novo < 0.0:
            estados.append({"tempo_s": t + dt, "posicao_m": s,
                            "velocidade_m_s": 0.0, "aceleracao_m_s2": 0.0,
                            "omega_saida_rad_s": 0.0,
                            "torque_eletromagnetico_Nm": 0.0,
                            "potencia_ac_W": 0.0, "potencia_em_W": 0.0,
                            "energia_acumulada_J": energia_acumulada,
                            "perda_cobre_acumulada_J": energia_resistiva})
            return {"status": "PARA", "estados": tuple(estados)}
        v = v_novo
        s += v * dt
        t += dt
        potencia_anterior = previa["potencia_em_W"]
        perda_anterior = perda_cobre
    raise RuntimeError("integração excedeu max_passos")
