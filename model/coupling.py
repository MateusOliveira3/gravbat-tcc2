"""Acoplamento dinâmico V0.4 com torque mecânico constante no eixo de saída."""
import math
from dataclasses import dataclass
from model.geometry import finito, positivo
from model.transmission import cinematica


@dataclass(frozen=True)
class Acoplamento:
    base: object
    tau_carga_Nm: float
    eta_transmissao: float
    raio_d_m: float
    relacao_G: float
    forca_carga_N: float
    torque_tambor_resistente_Nm: float
    aceleracao_m_s2: float
    status: str
    tempo_final_s: float | None

    @property
    def torque_limite_v04_Nm(self):
        disponivel = self.base.forcas.disponivel_N
        return max(0.0, self.eta_transmissao * self.raio_d_m * disponivel / self.relacao_G)

    def estados(self, n=301):
        if self.tempo_final_s is None:
            return (self.estado(0.0),)
        return tuple(self.estado(self.tempo_final_s * i/(n-1)) for i in range(n))

    def estado(self, tempo_s):
        finito("tempo_s", tempo_s)
        if tempo_s < 0 or (self.tempo_final_s is not None and tempo_s > self.tempo_final_s):
            raise ValueError("tempo_s fora da trajetória V0.4")
        s = .5*self.aceleracao_m_s2*tempo_s**2
        v = self.aceleracao_m_s2*tempo_s
        if self.tempo_final_s is not None and tempo_s == self.tempo_final_s:
            s = self.base.geometria.L_m
        ep = self.base.massa_kg*self.base.g_m_s2*(self.base.geometria.H_m-s*math.sin(self.base.geometria.theta_rad))
        k = .5*self.base.massa_kg*v*v
        rol = self.base.forcas.rol_movimento_N*s
        e_carga = self.tau_carga_Nm*self.relacao_G*s/self.raio_d_m
        e_entrada = e_carga/self.eta_transmissao
        perda_t = e_entrada-e_carga
        inicial=self.base.massa_kg*self.base.g_m_s2*self.base.geometria.H_m
        p_carga=self.tau_carga_Nm*self.relacao_G*v/self.raio_d_m
        p_in=p_carga/self.eta_transmissao
        return {"tempo_s":tempo_s,"posicao_m":s,"velocidade_m_s":v,"ep_restante_J":ep,"cinetica_J":k,"rolamento_J":rol,"carga_J":e_carga,"entrada_transmissao_J":e_entrada,"perda_transmissao_J":perda_t,"residuo_J":inicial-(ep+k+rol+e_entrada),"potencia_carga_W":p_carga,"potencia_entrada_W":p_in,"rpm_saida":cinematica(v,self.raio_d_m,self.relacao_G).rpm_saida}


def acoplar(base, tau_carga_Nm, raio_d_m, relacao_G, eta_transmissao=1.0):
    finito("tau_carga_Nm", tau_carga_Nm)
    if tau_carga_Nm < 0: raise ValueError("tau_carga_Nm deve ser >= 0")
    finito("eta_transmissao", eta_transmissao)
    if not 0 < eta_transmissao <= 1: raise ValueError("eta_transmissao deve satisfazer 0 < eta <= 1")
    positivo("raio_d_m", raio_d_m); positivo("relacao_G", relacao_G)
    fc=relacao_G*tau_carga_Nm/(eta_transmissao*raio_d_m)
    liquida=base.forcas.disponivel_N-fc
    a=liquida/base.massa_kg if liquida>0 else 0.0
    tf=math.sqrt(2*base.geometria.L_m/a) if a>0 else None
    return Acoplamento(base,tau_carga_Nm,eta_transmissao,raio_d_m,relacao_G,fc,relacao_G*tau_carga_Nm/eta_transmissao,a,"DESCE_COM_CARGA" if a>0 else "NAO_DESCE_COM_CARGA",tf)


def varrer_torque(base, raio_d_m, relacao_G, eta_transmissao=1.0, pontos=1001):
    """Varredura uniforme até 1,01 do limite efetivo; não impõe o ponto ótimo."""
    if isinstance(pontos, bool) or not isinstance(pontos, int) or pontos < 3:
        raise ValueError("pontos deve ser inteiro >= 3")
    limite=acoplar(base,0,raio_d_m,relacao_G,eta_transmissao).torque_limite_v04_Nm
    saida=[]
    for i in range(pontos):
        c=acoplar(base,1.01*limite*i/(pontos-1),raio_d_m,relacao_G,eta_transmissao)
        e=c.estado(c.tempo_final_s or 0.0)
        saida.append({"tau_carga_Nm":c.tau_carga_Nm,"limite_Nm":limite,"status":c.status,"aceleracao_m_s2":c.aceleracao_m_s2,"tempo_s":c.tempo_final_s,"potencia_media_W":e["carga_J"]/c.tempo_final_s if c.tempo_final_s else 0.0,"energia_carga_J":e["carga_J"]})
    return saida
