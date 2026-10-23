"""Referência analítica independente para a dinâmica linear amortecida do E6."""
from dataclasses import dataclass
import math
from model.geometry import geometria
from model.mechanics import forcas
@dataclass(frozen=True)
class AnaliticoE6:
    theta_graus: float; G: float; b_Ns_m: float; L_m: float; F0_N: float; tempo_s: float; velocidade_final_m_s: float
    def estado(self,t):
        tau=6.0/self.b_Ns_m; vinf=self.F0_N/self.b_Ns_m
        v=vinf*(1-math.exp(-t/tau)); x=vinf*(t-tau*(1-math.exp(-t/tau)))
        return x,v

def resolver_tempo(F0,L,m,b):
    if F0<=0:return None
    if b<=0:return math.sqrt(2*m*L/F0)
    def x(t):
        tau=m/b; return F0/b*(t-tau*(1-math.exp(-t/tau)))
    lo=0.; hi=max(1.,2*L/(F0/m))
    while x(hi)<L and hi<1e9: hi*=2
    if x(hi)<L:return None
    for _ in range(100):
        mid=(lo+hi)/2
        if x(mid)<L:lo=mid
        else:hi=mid
    return (lo+hi)/2

def referencia(massa_kg,altura_m,theta_graus,cr,G=1.,ke=.1,rd=.05,eta=.9,Rfase=2.,Rcarga=8.):
    geo=geometria('terreno',theta_graus,H_m=altura_m); f=forcas(massa_kg,9.81,cr,geo)
    b=2*.5*ke**2*G**2/(eta*rd**2*(Rfase+Rcarga))
    T=resolver_tempo(f.disponivel_N,geo.L_m,massa_kg,b)
    if T is None:return None
    obj=AnaliticoE6(theta_graus,G,b,geo.L_m,f.disponivel_N,T,0.)
    x,v=obj.estado(T); object.__setattr__(obj,'velocidade_final_m_s',v)
    Eg=massa_kg*9.81*altura_m; Erol=f.rol_movimento_N*geo.L_m; Ek=.5*massa_kg*v*v; Eres=f.disponivel_N*geo.L_m-Ek
    Etrans=(1-eta)*Eres; Eem=eta*Eres; Eac=Eem*Rcarga/(Rfase+Rcarga); Ecu=Eem*Rfase/(Rfase+Rcarga)
    return obj,dict(Eg=Eg,Erol=Erol,Ek=Ek,Eres=Eres,Etrans=Etrans,Eem=Eem,Eac=Eac,Ecu=Ecu,Pac=Eac/T,residuo=Eg-Erol-Etrans-Eac-Ecu-Ek)
