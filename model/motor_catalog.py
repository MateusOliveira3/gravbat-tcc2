"""Catálogo rastreável de motores para a V0.5.

Os registros são dados de entrada; nenhum modelo é tratado como componente físico
do GravBat sem fabricante, código e fonte verificáveis.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class MotorCatalogo:
    id: str
    nome: str
    tipo: str
    origem: str
    status: str
    ke_Vs_rad: float | None
    resistencia_fase_ohm: float | None
    fases: int | None
    observacao: str


CATALOGO = (
    MotorCatalogo(
        id="hipotetico_v05",
        nome="Modelo hipotético V0.5",
        tipo="Motor de passo multifásico equivalente",
        origem="Hipótese de software; sem componente físico associado",
        status="HIPÓTESE",
        ke_Vs_rad=0.1,
        resistencia_fase_ohm=2.0,
        fases=2,
        observacao="Usado somente para testar o pipeline e a interface. Não é um motor comercial.",
    ),
    MotorCatalogo(
        id="faulhaber_dm52100s_datasheet",
        nome="FAULHABER DM52100S — candidato de datasheet",
        tipo="Motor de passo bipolar, 2 fases",
        origem="Datasheet FAULHABER, https://cdn.faulhaber.com/media/DAM/Documents/Datasheets%20Portfolio%20Collection/standard-datasheets-portfolio-en.pdf",
        status="DATASHEET-DERIVADO",
        ke_Vs_rad=2.2 / (1000 * 2 * 3.141592653589793 / 100),
        resistencia_fase_ohm=0.7,
        fases=2,
        observacao="K_e derivado do datasheet: 2,2 V/(1000 passos/s), 100 passos/rev; K_e = 2,2/(20π) = 0,0350 V·s/rad. Confirmar convenção por medição.",
    ),
    MotorCatalogo(
        id="perfil_estudo_12v",
        nome="Perfil de estudo 12 V — motor de passo bipolar",
        tipo="Motor de passo bipolar, 2 fases",
        origem="Hipótese paramétrica inspirada em faixas de motores de passo de baixa tensão",
        status="HIPÓTESE-PARAMÉTRICA",
        ke_Vs_rad=0.05,
        resistencia_fase_ohm=10.0,
        fases=2,
        observacao="Perfil para análise de sensibilidade; 12 V é tensão de referência, não tensão FEM garantida. K_e e resistência precisam de datasheet ou medição.",
    ),
    MotorCatalogo(
        id="perfil_estudo_30v",
        nome="Perfil de estudo 30 V — motor de passo bipolar",
        tipo="Motor de passo bipolar, 2 fases",
        origem="Hipótese paramétrica para análise de tensão intermediária",
        status="HIPÓTESE-PARAMÉTRICA",
        ke_Vs_rad=0.10,
        resistencia_fase_ohm=30.0,
        fases=2,
        observacao="Perfil exploratório; 30 V é tensão de referência, não especificação de um motor identificado. K_e e resistência precisam de datasheet ou medição.",
    ),
)


def listar_motores():
    return CATALOGO


def obter_motor(motor_id):
    for motor in CATALOGO:
        if motor.id == motor_id:
            return motor
    raise ValueError(f"motor não cadastrado: {motor_id}")
