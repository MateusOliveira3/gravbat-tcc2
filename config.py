"""Valores adotados para reprodução dos cenários do script original."""
G_M_S2 = 9.81
MASSA_KG = 6.0
C_R = 0.02
ANGULOS_GRAUS = (5, 10, 15, 20, 25, 30)
L_LAB_M = 1.20
H_TERRENO_M = 2.00
N_AMOSTRAS = 301

CLASSIFICACOES = (
    "DADO MEDIDO", "DADO DE LITERATURA", "HIPÓTESE",
    "RESULTADO CALCULADO", "RESULTADO SIMULADO", "RESULTADO EXPERIMENTAL",
)
ORIGENS = {
    "g_m_s2": ("HIPÓTESE", "Valor adotado 9.81 m/s²; não medido localmente"),
    "massa_kg": ("HIPÓTESE", "Entrada configurável; 6 kg do script original, sem medição comprovada"),
    "theta_graus": ("HIPÓTESE", "Entradas da varredura original; não medidas"),
    "c_r": ("HIPÓTESE", "Resistência equivalente em movimento, configurável, não medida"),
    "L_lab_m": ("HIPÓTESE", "1.20 m assumido no script original; geometria não aferida"),
    "H_terreno_m": ("HIPÓTESE", "2.00 m como referência mínima de aplicação; geometria editável e não aferida"),
    "geometria_forcas": ("RESULTADO CALCULADO", "Equações analíticas V0.1"),
    "trajetoria_energias": ("RESULTADO SIMULADO", "Amostragem da solução analítica, sem validação experimental"),
}
