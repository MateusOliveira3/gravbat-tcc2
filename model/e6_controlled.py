"""E6 independente: diagn?stico de descarga regulada.
N?o altera os modelos E1--E5; o torque prescrito ? explicitamente uma carga mec?nica.
"""
from dataclasses import dataclass
import math
from model.geometry import geometria
from model.mechanics import forcas
from model.electromechanics import ParametrosGerador
from simulation.electromechanical_dynamic import simular_descida_eletromecanica
from simulation.simulator import simular

@dataclass(frozen=True)
class E6Resultado:
    regime: str; theta_graus: float; duracao_s: float; L_m: float
    v_media_m_s: float; torque_Nm: float; potencia_carga_media_W: float
    energia_carga_J: float; energia_dissipada_J: float; energia_rolamento_J: float
    energia_cinetica_final_J: float; velocidade_final_m_s: float; status: str
    residuo_J: float

def controlado_torque(massa_kg, altura_m, theta_graus, cr, duracao_s, raio_d_m=.05, relacao_G=1., eta_transmissao=.9, tau_max_Nm=None):
    """Regime B: velocidade m?dia uniforme e torque resistente prescrito.
    O torque ? tratado como freio mec?nico; energia el?trica ? zero neste regime.
    """
    if duracao_s <= 0: raise ValueError("duracao_s deve ser > 0")
    geo=geometria('terreno',theta_graus,H_m=altura_m); f=forcas(massa_kg,9.81,cr,geo)
    v=geo.L_m/duracao_s
    tau=eta_transmissao*raio_d_m*f.disponivel_N/relacao_G
    if tau_max_Nm is not None and tau_max_Nm < tau:
        return E6Resultado('B_torque_prescrito',theta_graus,duracao_s,geo.L_m,v,tau_max_Nm,0.,0.,0.,f.rol_movimento_N*geo.L_m,0.,0.,'BLOQUEADO',massa_kg*9.81*altura_m-f.rol_movimento_N*geo.L_m)
    e_g=massa_kg*9.81*altura_m; e_rol=f.rol_movimento_N*geo.L_m
    # velocidade constante: energia dispon?vel ap?s rolamento ? absorvida pelo freio
    e_freio=max(0.,e_g-e_rol); resid=e_g-e_rol-e_freio
    return E6Resultado('B_torque_prescrito',theta_graus,duracao_s,geo.L_m,v,tau,0.,0.,e_freio,e_rol,0.,v,'CHEGADA',resid)

def passivo_e4(massa_kg, altura_m, theta_graus, cr, resistencia_carga_ohm=8., passo_s=.001, raio_d_m=.05, relacao_G=1., ke_Vs_rad=.1, resistencia_fase_ohm=2., eta_transmissao=.9):
    geo=geometria('terreno',theta_graus,H_m=altura_m); base=simular(massa_kg,theta_graus,cr,'terreno',H_m=altura_m)
    p=ParametrosGerador(ke_Vs_rad,resistencia_fase_ohm,2,.9)
    r=simular_descida_eletromecanica(base,raio_d_m,relacao_G,eta_transmissao,p,resistencia_carga_ohm,passo_s)
    last=r['estados'][-1]; e_em=last.get('energia_acumulada_J',0.); e_cu=last.get('perda_cobre_acumulada_J',0.)
    e_carga=max(0.,e_em-e_cu)
    e_rol=base.forcas.rol_movimento_N*geo.L_m; eg=massa_kg*9.81*altura_m; ek=.5*massa_kg*last['velocidade_m_s']**2
    return E6Resultado('A_passivo_E4',theta_graus,last['tempo_s'],geo.L_m,geo.L_m/last['tempo_s'],last.get('torque_eletromagnetico_Nm',0.),e_carga/last['tempo_s'],e_carga, e_cu,e_rol,ek,last['velocidade_m_s'],r['status'],eg-e_rol-e_carga-e_cu-ek)



def simular_torque_prescrito(massa_kg, altura_m, theta_graus, cr, duracao_s, raio_d_m=.05, relacao_G=1., eta_transmissao=.9, passo_s=.001, tau_max_Nm=None):
    """Regime B din?mico: torque constante escolhido para dura??o-alvo.
    Parte do repouso; n?o injeta energia. Dura??o-alvo s? ? v?lida se a acelera??o
    resultante for positiva e o torque requerido estiver dentro da satura??o.
    """
    if duracao_s <= 0 or passo_s <= 0: raise ValueError("duracao_s e passo_s devem ser > 0")
    geo=geometria('terreno',theta_graus,H_m=altura_m); f=forcas(massa_kg,9.81,cr,geo)
    a_req=2*geo.L_m/duracao_s**2
    fc=f.disponivel_N-massa_kg*a_req
    tau=eta_transmissao*raio_d_m*fc/relacao_G
    if fc <= 0: return {"status":"ALVO_INVIAVEL_RAPIDO","torque_Nm":tau,"amostras":(),"residuo_J":None}
    if tau_max_Nm is not None and tau > tau_max_Nm: return {"status":"BLOQUEIO_SATURACAO","torque_Nm":tau,"amostras":(),"residuo_J":None}
    t=0.; s=0.; v=0.; estados=[]; eg=massa_kg*9.81*altura_m; er=0.; et=0.; eb=0.; ek=0.
    while t < duracao_s-1e-12:
        dt=min(passo_s,duracao_s-t); estados.append({"tempo_s":t,"posicao_m":s,"velocidade_m_s":v,"torque_Nm":tau})
        s=min(geo.L_m,s+v*dt+.5*a_req*dt*dt); v=v+a_req*dt; t+=dt
    er=f.rol_movimento_N*geo.L_m; entrada=fc*geo.L_m; et=(1-eta_transmissao)*entrada; eb=eta_transmissao*entrada; ek=.5*massa_kg*v*v
    resid=eg-er-et-eb-ek
    estados.append({"tempo_s":t,"posicao_m":s,"velocidade_m_s":v,"torque_Nm":tau})
    return {"status":"CHEGADA","torque_Nm":tau,"amostras":tuple(estados),"tempo_s":t,"velocidade_final_m_s":v,"energia_rolamento_J":er,"energia_transmissao_J":et,"energia_freio_eixo_J":eb,"energia_cinetica_final_J":ek,"residuo_J":resid,"energia_carga_J":0.0}
