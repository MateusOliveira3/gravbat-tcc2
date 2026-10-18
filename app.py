"""Dashboard científico do GravBat: núcleo mecânico V0.4 e preparação da V0.5."""
import math
import time
import streamlit as st
import config
from simulation.simulator import simular
from dashboard.scenarios import interpretar, numero, perda_percentual, varrer_inclinacao
from dashboard import charts
from model.transmission import cinematica
from model.coupling import acoplar
from model.motor_catalog import listar_motores, obter_motor
from model.electromechanics import ParametrosGerador, fem_fase, previa_carga_resistiva
from model.electromechanical_coupling import acoplar_carga_resistiva
from simulation.cycle import ciclo_descida_subida
from model.cable import GeometriaCabo
from model.dimensioning import dimensionar_demanda
from model.application_scenarios import SCENARIOS, obter_cenario
from model.reporting import relatorio_cenario, serializar_relatorio, serializar_tabela_relatorio, serializar_trajetoria, serializar_transformacoes
from model.inverse_design import dimensionar_configuracao
from model.scenario_analysis import comparar_cenarios
from model.energy_chain import balanço_transformacoes
from simulation.electromechanical_dynamic import simular_descida_eletromecanica

st.set_page_config(page_title="GravBat · Modelo científico", page_icon="↘", layout="wide")
st.html("""<style>
[data-testid="stMetricLabel"] p {white-space: normal;}
[data-testid="stMetricValue"] {font-size: 1.15rem; white-space: normal; overflow-wrap: anywhere;}
[data-testid="stVerticalBlockBorderWrapper"] {padding-top: .45rem; padding-bottom: .45rem;}
[data-testid="stExpander"] {margin-top: .25rem; margin-bottom: .25rem;}
</style>""")
st.title("GravBat")
st.caption("TCC-2 · Engenharia de Energia / UFSC · núcleo científico do modelo")
st.info("Fluxo da análise: cenário → modelo mecânico → transmissão → conversão eletromecânica → ciclo → dimensionamento → verificação. Resultados calculados/simulados não constituem validação experimental.")
modo_interface = st.radio("Visualização", ["Dashboard compacto", "Auditoria técnica"], horizontal=True, key="modo_interface")

with st.expander("Como ler esta versão", expanded=False):
    st.markdown("""
    **Objetivo desta versão:** verificar o comportamento mecânico e o acoplamento de uma carga genérica.

    **Entradas:** parâmetros do cenário e hipóteses configuráveis na barra lateral.

    **Resultados:** grandezas calculadas pelo modelo e trajetórias simuladas.

    **Ainda não implementado:** gerador, retificador, eletrônica, controle e ciclo de subida.

    **Classificação:** os resultados são identificados como calculados ou simulados; parâmetros sem medição são hipóteses.
    """)

painel_cenario = st.container(border=True)
with painel_cenario:
    st.subheader("Cenário")
    if modo_interface == "Dashboard compacto":
        st.subheader("Pergunta de aplicação")
        pergunta = st.text_input("Descreva o que você quer estimar", value="Qual massa pode alimentar iluminação e Wi‑Fi por 4 horas?", key="pergunta_compacta_v2")
        st.caption("A pergunta orienta os valores iniciais de dimensionamento. Depois, você pode editar qualquer variável para comparar cenários.")
    modo_label = st.radio("Geometria", ["Laboratório · L fixo", "Aplicação · H fixo"], index=0 if modo_interface == "Auditoria técnica" else 1, key=f"modo_{modo_interface}")
    modo = "laboratorio" if modo_label.startswith("Laboratório") else "terreno"
    st.caption("HIPÓTESES / ENTRADAS · valores iniciais assumidos, não aferidos experimentalmente.")
    config_cols = st.columns(4)
    massa = config_cols[0].number_input("Massa (kg)", value=config.MASSA_KG, step=1.0, key="massa")
    theta = config_cols[1].number_input("Inclinação (graus)", value=10.0, step=1.0, key="theta")
    cr = config_cols[2].number_input("c_r · resistência equivalente", value=config.C_R, step=.01, format="%.4f", key="cr")
    if modo == "laboratorio":
        dimensao = {"L_m": config_cols[3].number_input("Comprimento L (m)", value=config.L_LAB_M, step=.1, key=f"L_{modo_interface}")}
    else:
        dimensao = {"H_m": config_cols[3].number_input("Desnível H (m)", value=config.H_TERRENO_M, step=.1, key=f"H_{modo_interface}")}
    st.caption(f"g = {config.G_M_S2} m/s² · valor adotado. c_r é resistência em movimento, não atrito estático.")
    st.caption("Domínio: massa e dimensão > 0; c_r ≥ 0; 0 < inclinação < 90°. Alterações recalculam o cenário e a varredura.")
    altura_configurada = dimensao.get("H_m", dimensao.get("L_m", 0.0) * math.sin(math.radians(theta)))
    comprimento_configurado = dimensao.get("L_m", dimensao.get("H_m", 0.0) / math.sin(math.radians(theta)))
    geometria_info = st.columns(3)
    geometria_info[0].metric("Comprimento da rampa", numero(comprimento_configurado) + " m")
    geometria_info[1].metric("Desnível vertical", numero(altura_configurada) + " m")
    geometria_info[2].metric("Inclinação", numero(theta) + "°")

with st.sidebar:
    st.header("Catálogo eletromecânico")
    motores = [m for m in listar_motores() if m.ke_Vs_rad is not None and m.resistencia_fase_ohm is not None and m.fases is not None]
    motores.sort(key=lambda m: (0 if "DATASHEET" in m.status else 1, m.nome))
    motor_id = st.selectbox("Modelo do motor", [m.id for m in motores],
                            format_func=lambda value: obter_motor(value).nome)
    motor_selecionado = obter_motor(motor_id)
    st.caption(f"Status: {motor_selecionado.status}")
    if "DATASHEET" in motor_selecionado.status:
        st.success("Referência principal: parâmetros derivados de datasheet de fabricante. Confirmar convenções e compatibilidade com o componente físico.")
    st.caption("O seletor mostra modelos com parâmetros mínimos para simulação. Outros candidatos podem permanecer no catálogo enquanto K_e não estiver convertido ou medido.")

with st.sidebar:
    st.header("Cabo e tambor · geometria preliminar")
    tipo_cabo = st.text_input("Tipo de cabo", value="A definir", key="tipo_cabo")
    diametro_cabo = st.number_input("Diâmetro do cabo (m)", value=.01, min_value=.000001, step=.001, format="%.4f", key="diametro_cabo")
    diametro_nucleo = st.number_input("Diâmetro do núcleo do tambor (m)", value=.10, min_value=.000001, step=.01, format="%.4f", key="diametro_nucleo")
    comprimento_cabo = st.number_input("Comprimento disponível de cabo (m)", value=10.0, min_value=.000001, step=1.0, key="comprimento_cabo")
try:
    cabo = GeometriaCabo(tipo_cabo, diametro_cabo, diametro_nucleo, comprimento_cabo)
    r = simular(massa, theta, cr, modo, **dimensao)
    estados = r.amostras(config.N_AMOSTRAS)
    sweep = varrer_inclinacao(r)
except (ValueError, OverflowError, ZeroDivisionError) as erro:
    st.error(f"Configuração inválida ou fora do domínio numérico: {erro}. Revise as entradas; nenhum valor foi corrigido automaticamente.")
    st.stop()

final = estados[-1]
if r.tempo_final_s is None:
    st.warning("NAO_DESCE · Sob a aproximação de partida, o corpo permanece em repouso. Não há percurso nem perda por rolamento.")
else:
    st.success("DESCE · Movimento a partir do repouso, calculado até o fim da rampa, antes de colisão ou frenagem.")

if modo_interface == "Auditoria técnica":
    metricas = [
    ("Desnível H", numero(r.geometria.H_m) + " m"),
    ("Comprimento L", numero(r.geometria.L_m) + " m"),
    ("Energia potencial inicial", numero(final.energia.inicial_J) + " J"),
    ("Perda por rolamento", numero(final.energia.perda_rolamento_J) + " J"),
    ("Força gravitacional paralela", numero(r.forcas.grav_paralela_N) + " N"),
    ("Resistência ao rolamento", numero(r.forcas.rol_movimento_N) + " N"),
    ("Força líquida no movimento", numero(r.forcas.disponivel_N) + " N"),
    ("Aceleração efetiva", numero(r.forcas.aceleracao_m_s2) + " m/s²"),
    ("Tempo de descida", numero(r.tempo_final_s) + " s" if r.tempo_final_s is not None else "Não aplicável"),
    ("Velocidade final" if r.tempo_final_s is not None else "Velocidade · repouso", numero(final.velocidade_m_s) + " m/s"),
    ("Energia dissipada por rolamento", numero(perda_percentual(r)) + " %"),
    ]
    for i in range(0, len(metricas), 3):
        for col, (rotulo, valor) in zip(st.columns(3), metricas[i:i+3]):
            col.metric(rotulo, valor)
    st.caption("Resistência ao rolamento: valor equivalente previsto durante movimento, não força estática identificada. No bloqueio, a força líquida no movimento é um diagnóstico da aproximação de partida; a aceleração efetiva é zero.")
    st.subheader("Resposta principal do cenário")
    st.caption("Resumo preliminar calculado a partir das entradas atuais. Detalhes e verificações ficam nas seções abaixo.")
    resumo = st.columns(4)
    resumo[0].metric("Energia potencial", numero(final.energia.inicial_J) + " J")
    resumo[1].metric("Tempo de descida", numero(r.tempo_final_s) + " s" if r.tempo_final_s is not None else "Não aplicável")
    resumo[2].metric("Velocidade final", numero(final.velocidade_m_s) + " m/s")
    resumo[3].metric("Estado", "DESCE" if r.tempo_final_s is not None else "BLOQUEADO")

if modo_interface == "Dashboard compacto":
  with painel_cenario:
    st.caption("A pergunta fica no topo do cenário; os parâmetros abaixo podem ser ajustados para testar alternativas.")
    with st.expander("Demanda e condição de operação", expanded=True):
        dc = st.columns(5)
        energia_pergunta = dc[0].number_input("Energia útil por evento (Wh)", value=400.0, min_value=0.001, step=10.0, key="energia_pergunta_v6")
        potencia_pergunta = dc[1].number_input("Potência de projeto (W)", value=200.0, min_value=0.001, step=10.0, key="potencia_pergunta_v4")
        duracao_pergunta = dc[2].number_input("Duração (s)", value=14400.0, min_value=0.001, step=60.0, key="duracao_pergunta_v3")
        velocidade_pergunta = dc[3].number_input("Velocidade (m/s)", value=0.02, min_value=0.000001, step=0.01, format="%.4f", key="velocidade_pergunta")
        eficiencia_global = dc[4].number_input("Eficiência global", value=0.55, min_value=0.01, max_value=1.0, step=0.01, format="%.2f", key="eficiencia_global_v1")
        mc = st.columns(3)
        modulos = mc[0].number_input("Módulos em paralelo", value=10, min_value=1, step=1, key="modulos_paralelo_v1")
        perfil_operacao = mc[1].selectbox("Perfil de operação", ["Iluminação e Wi‑Fi", "Controle solar/eólico", "Reserva de potência"], key="perfil_operacao_v1")
        excedente_W = mc[2].number_input("Excedente renovável (W)", value=1000.0, min_value=0.0, step=100.0, key="excedente_renovavel_v1")
        duracao_excedente_h = st.number_input("Duração do excedente (h)", value=1.0, min_value=0.001, step=0.5, key="duracao_excedente_v1")
        st.caption("O módulo individual pode ser repetido em paralelo. O banco total soma massa, energia e potência dos módulos disponíveis.")
        altura_pergunta = r.geometria.H_m
        resultado_inverso = dimensionar_configuracao(energia_pergunta, potencia_pergunta, duracao_pergunta, altura_pergunta, eficiencia_global, velocidade_pergunta, theta_graus=theta)
        massa_modulo = massa
        massa_banco = massa_modulo * modulos
        energia_banco_Wh = massa_banco * config.G_M_S2 * altura_pergunta * eficiencia_global / 3600.0
        potencia_banco_W = massa_banco * config.G_M_S2 * velocidade_pergunta * eficiencia_global
        modulos_requeridos = math.ceil(resultado_inverso["massa_requerida_kg"] / massa_modulo)
        energia_excedente_Wh = excedente_W * duracao_excedente_h
        modulos_curtailment = math.ceil(energia_excedente_Wh / max(energia_banco_Wh / modulos, 1e-12)) if excedente_W > 0 else 0
        ri = st.columns(4)
        ri[0].metric("Massa requerida · aplicação", numero(resultado_inverso["massa_requerida_kg"]) + " kg")
        ri[1].metric("Massa limitada pela energia", numero(resultado_inverso["massa_por_energia_kg"]) + " kg")
        massa_potencia_media_ui = resultado_inverso.get("massa_por_potencia_media_kg", resultado_inverso["massa_por_potencia_kg"])
        ri[2].metric("Massa pela potência média", numero(massa_potencia_media_ui) + " kg")
        ri[3].metric("Potência média", numero(resultado_inverso["potencia_media_W"]) + " W")
        rb = st.columns(4)
        rb[0].metric("Massa do banco", numero(massa_banco) + " kg")
        rb[1].metric("Energia do banco", numero(energia_banco_Wh) + " Wh")
        rb[2].metric("Potência do banco", numero(potencia_banco_W) + " W")
        rb[3].metric("Módulos para atender demanda", numero(modulos_requeridos))
        if resultado_inverso.get("status") == "DADOS_INSUFICIENTES":
            st.warning("DADOS_INSUFICIENTES: a potência de projeto excede a potência média, mas não foi informada a duração do pico. O número de módulos abaixo é apenas referência de energia/potência média; o atendimento do pico não está declarado.")
        rc = st.columns(3)
        rc[0].metric("Excedente a absorver", numero(energia_excedente_Wh) + " Wh")
        rc[1].metric("Módulos para absorver excedente", numero(modulos_curtailment))
        rc[2].metric("Potência de carga do evento", numero(excedente_W) + " W")
        if perfil_operacao == "Controle solar/eólico":
            st.success("Leitura do serviço: o banco é avaliado como absorvedor de excedente renovável. O resultado indica quantos módulos seriam necessários para deslocar esse evento sem tratá-lo como alimentação contínua de uma residência.")
        if resultado_inverso["potencia_media_W"] > potencia_pergunta:
            st.warning(f"A energia e a duração informadas implicam potência média de {numero(resultado_inverso['potencia_media_W'])} W, acima da potência máxima informada de {numero(potencia_pergunta)} W. Aumente a duração ou revise a energia do evento.")
        st.info(f"Perfil **{perfil_operacao}**: o banco configurado com {numero(modulos)} módulos de {numero(massa_modulo)} kg entrega aproximadamente {numero(energia_banco_Wh)} Wh e {numero(potencia_banco_W)} W. Para a demanda parametrizada, o modelo estima {numero(modulos_requeridos)} módulos equivalentes.")
        if "resid" in pergunta.lower() and energia_pergunta <= 100.0:
            st.warning("A pergunta menciona uma residência, mas a energia útil ainda está no valor genérico de 100 Wh. Edite esse campo para o consumo que deseja representar; o modelo não inventa o consumo residencial a partir do texto.")
        massa_pico_ui = resultado_inverso.get("massa_por_potencia_pico_kg", resultado_inverso["massa_por_potencia_kg"])
        st.caption(f"Origem dos valores: a massa requerida usa energia e potência média. A potência de projeto de {numero(potencia_pergunta)} W é tratada como requisito de pico para inversor/barramento; se precisar ser sustentada continuamente pela massa, a massa correspondente seria {numero(massa_pico_ui)} kg. A eficiência global de {numero(eficiencia_global * 100)}% é uma hipótese configurável e deve ser substituída pelo produto das eficiências parciais documentadas.")
        st.caption("Configuração calculada pela maior restrição entre energia e potência. A velocidade-alvo exige freio eletromagnético/controle; não é garantida pela ponte de diodos isoladamente.")
    cp = st.columns(4)
    cp[0].metric("Energia útil solicitada", numero(energia_pergunta) + " Wh")
    cp[1].metric("Duração solicitada", numero(duracao_pergunta / 3600.0) + " h")
    cp[2].metric("Massa dimensionada", numero(resultado_inverso["massa_requerida_kg"]) + " kg")
    cp[3].metric("Estado", "DIMENSIONAMENTO")
    st.caption("A duração acima pertence à aplicação perguntada. A rampa animada abaixo é a referência mecânica do cenário e tem tempo próprio; ela não substitui a duração de atendimento da aplicação.")
    passo_posicao = r.geometria.L_m / max(len(estados) - 1, 1)
    posicao_escolhida = st.slider("Posição da massa na rampa (m)", 0.0, float(r.geometria.L_m), float(r.geometria.L_m), step=max(passo_posicao, 0.000001), key="posicao_compacta")
    indice = min(range(len(estados)), key=lambda i: abs(estados[i].posicao_m - posicao_escolhida))
    executar = st.button("▶ Executar descida", type="primary", key="executar_descida")
    if executar and r.tempo_final_s is not None:
        painel_animacao = st.empty()
        painel_metricas = st.empty()
        for indice_animacao in range(0, len(estados), max(1, len(estados) // 80)):
            estado_animacao = estados[indice_animacao]
            progresso_animacao = 1.0 - (estado_animacao.posicao_m / r.geometria.L_m if r.geometria.L_m else 0.0)
            massa_aplicacao = resultado_inverso["massa_requerida_kg"]
            potencia_animacao = massa_aplicacao * config.G_M_S2 * velocidade_pergunta * eficiencia_global
            tempo_controlado = estado_animacao.posicao_m / velocidade_pergunta if velocidade_pergunta > 0 else estado_animacao.tempo_s
            energia_restante_aplicacao = massa_aplicacao * config.G_M_S2 * max(r.geometria.L_m - estado_animacao.posicao_m, 0.0) * math.sin(math.radians(theta)) * eficiencia_global
            with painel_animacao.container():
                st.plotly_chart(charts.esquema_rampa(progresso_animacao, potencia_animacao), width="stretch", key=f"animacao_rampa_{indice_animacao}", config={"displaylogo": False})
            with painel_metricas.container():
                am = st.columns(4)
                am[0].metric("Posição", numero(estado_animacao.posicao_m) + " m")
                am[1].metric("Energia útil restante", numero(energia_restante_aplicacao / 3600.0) + " Wh")
                am[2].metric("Velocidade controlada", numero(velocidade_pergunta) + " m/s")
                am[3].metric("Tempo da descida", numero(tempo_controlado) + " s")
            time.sleep(0.035)
        indice = len(estados) - 1
    estado_visual = estados[indice]
    progresso_visual = 1.0 - (estado_visual.posicao_m / r.geometria.L_m if r.geometria.L_m else 0.0)
    massa_aplicacao = resultado_inverso["massa_requerida_kg"]
    potencia_visual = massa_aplicacao * config.G_M_S2 * velocidade_pergunta * eficiencia_global
    energia_restante_visual = massa_aplicacao * config.G_M_S2 * max(r.geometria.L_m - estado_visual.posicao_m, 0.0) * math.sin(math.radians(theta)) * eficiencia_global
    if not executar:
        st.plotly_chart(charts.esquema_rampa(progresso_visual, potencia_visual), width="stretch", key="esquema_rampa_compacto", config={"displaylogo": False})
        cv = st.columns(5)
        cv[0].metric("Posição", numero(estado_visual.posicao_m) + " m")
        cv[1].metric("Energia útil restante", numero(energia_restante_visual / 3600.0) + " Wh")
        cv[2].metric("Velocidade controlada", numero(velocidade_pergunta) + " m/s")
        cv[3].metric("Tempo da descida", numero(estado_visual.posicao_m / velocidade_pergunta) + " s")
        cv[4].metric("Potência instantânea", numero(potencia_visual) + " W")
    if r.tempo_final_s is not None:
        st.caption(f"Referência mecânica da rampa: {numero(r.tempo_final_s)} s. A referência histórica de 50 s do TCC-1 é um benchmark didático, não um requisito imposto ao modelo.")
    curva = st.selectbox("Curva principal", ["Energia ao longo da rampa", "Velocidade ao longo do tempo"], key="curva_compacta")
    if curva == "Energia ao longo da rampa":
        st.plotly_chart(charts.energia_posicao(estados), width="stretch", key="curva_compacta_energia", config={"displaylogo": False, "scrollZoom": False})
    else:
        st.plotly_chart(charts.velocidade_tempo(estados), width="stretch", key="curva_compacta_velocidade", config={"displaylogo": False, "scrollZoom": False})
    st.success("Dashboard compacto: altere as entradas acima e observe a resposta principal. Para equações, perdas, testes e exportações, selecione Auditoria técnica.")
    st.caption("Ciclo energético: descida = descarga/geração; subida = recarga da massa. O esquema visual atual representa a descida.")
    st.stop()
with st.expander("Verificação numérica"):
    st.write("O resíduo energético mede o erro numérico do balanço de energia. Não representa uma perda física do sistema.")
    st.metric("Máx. resíduo energético", numero(max(abs(e.energia.residuo_energia_J) for e in estados)) + " J")

def grafico(fig, chave):
    st.plotly_chart(fig, width="stretch", key=chave, config={"displaylogo": False, "scrollZoom": False})

st.subheader("Transmissão cinemática")
st.caption(f"Cabo: {cabo.tipo}; diâmetro {numero(cabo.diametro_cabo_m)} m; núcleo {numero(cabo.diametro_nucleo_m)} m; {numero(cabo.voltas_estimadas_primeira_camada)} voltas equivalentes na primeira camada. O raio efetivo ainda é uma entrada separada.")
st.warning("Esta seção mostra a referência cinemática sem carga. As RPM não incluem o torque eletromecânico.")
with st.sidebar:
    st.header("Transmissão cinemática")
    raio_d = st.number_input("Raio efetivo do tambor r_d (m)", value=0.05, min_value=0.000001, step=0.01, format="%.4f", key="raio_d")
    relacao_G = st.number_input("Relação G = ω_saida / ω_tambor", value=1.0, min_value=0.000001, step=0.5, format="%.4f", key="G")
    eta_t = st.number_input("η da transmissão", value=1.0, min_value=.000001, max_value=1.0, step=.05, format="%.4f", key="eta_t")
    st.caption("r_d e G são hipóteses configuráveis. Sem carga ou inércia, alteram apenas as rotações.")
try:
    transm = [cinematica(e.velocidade_m_s, raio_d, relacao_G) for e in estados]
except ValueError as erro:
    st.error(f"Parâmetro de transmissão inválido: {erro}")
    st.stop()
st.caption("A transmissão fornece a referência sem carga. Torque, potência elétrica e eficiência aparecem nas verificações específicas.")
tc = st.columns(4)
tc[0].metric("Velocidade linear final", numero(final.velocidade_m_s) + " m/s")
tc[1].metric("RPM final do tambor", numero(transm[-1].rpm_tambor) + " RPM")
tc[2].metric("ω final de saída", numero(transm[-1].omega_saida_rad_s) + " rad/s")
tc[3].metric("RPM final de saída", numero(transm[-1].rpm_saida) + " RPM")
with st.expander("Diagnóstico da transmissão: RPM", expanded=False):
    st.markdown("**RPM versus tempo**")
    grafico(charts.rpm_tempo([{"tempo_s": e.tempo_s, "rpm_tambor": t.rpm_tambor, "rpm_saida": t.rpm_saida} for e, t in zip(estados, transm)]), "rpm_tempo")
g_sweep = []
for g in (0.25, 0.5, 1.0, 2.0, 4.0):
    g_sweep.append({"G": g, "rpm_saida": cinematica(final.velocidade_m_s, raio_d, g).rpm_saida})
with st.expander("Diagnóstico da transmissão: relação G", expanded=False):
    st.markdown("**Relação G versus RPM final de saída**")
    grafico(charts.varredura_G(g_sweep), "sweep_G")

st.subheader("Motor e conversão eletromecânica")
st.info("Selecione um perfil de motor para estimar FEM, potência, torque resistente e resposta dinâmica. A origem de cada perfil aparece junto aos parâmetros.")
with st.expander("Parâmetros do modelo selecionado"):
    st.dataframe([
        {"Parâmetro": "Identificador", "Valor": motor_selecionado.id, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Nome", "Valor": motor_selecionado.nome, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Tipo", "Valor": motor_selecionado.tipo, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "K_e (V·s/rad)", "Valor": motor_selecionado.ke_Vs_rad, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Resistência de fase (Ω)", "Valor": motor_selecionado.resistencia_fase_ohm, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Número de fases", "Valor": motor_selecionado.fases, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Origem", "Valor": motor_selecionado.origem, "Origem/status": motor_selecionado.status},
        {"Parâmetro": "Observação", "Valor": motor_selecionado.observacao, "Origem/status": motor_selecionado.status},
    ], hide_index=True, width="stretch")
energia_eletrica_dinamica_J = None
ciclo = None
if motor_selecionado.ke_Vs_rad is not None and motor_selecionado.resistencia_fase_ohm is not None and motor_selecionado.fases is not None:
    parametros_motor = ParametrosGerador(
        motor_selecionado.ke_Vs_rad,
        motor_selecionado.resistencia_fase_ohm,
        motor_selecionado.fases,
    )
    omega_preview = transm[-1].omega_saida_rad_s
    fem_preview = parametros_motor.ke_Vs_rad * abs(omega_preview)
    st.caption("FEM de circuito aberto estimada no pico da fase. Esta grandeza é calculada e ainda não representa tensão sob carga.")
    ecatalogo = st.columns(3)
    ecatalogo[0].metric("ω de saída", numero(omega_preview) + " rad/s")
    ecatalogo[1].metric("FEM de pico · circuito aberto", numero(fem_preview) + " V")
    ecatalogo[2].metric("Fases cadastradas", str(parametros_motor.fases))
    resistencia_carga = st.number_input("Carga resistiva equivalente (Ω)", value=8.0, min_value=0.000001, step=1.0, key="resistencia_carga")
    previa = previa_carga_resistiva(omega_preview, resistencia_carga, parametros_motor)
    st.caption("Prévia de carga: aproximação por fase equivalente, com potência senoidal média multiplicada pelo número de fases. Não altera a trajetória mecânica.")
    pc = st.columns(4)
    pc[0].metric("Corrente de pico", numero(previa["corrente_pico_A"]) + " A")
    pc[1].metric("Potência AC estimada", numero(previa["potencia_ac_W"]) + " W")
    pc[2].metric("Potência CC estimada", numero(previa["potencia_cc_W"]) + " W")
    pc[3].metric("Torque resistente estimado", numero(previa["torque_resistente_Nm"]) + " N·m")
    st.markdown("**Comparação dos perfis eletromecânicos cadastrados**")
    comparacao_motores = []
    for candidato in motores:
        p_candidato = ParametrosGerador(candidato.ke_Vs_rad, candidato.resistencia_fase_ohm, candidato.fases)
        prev_candidato = previa_carga_resistiva(omega_preview, resistencia_carga, p_candidato)
        comparacao_motores.append({
            "Modelo": candidato.nome,
            "Status": candidato.status,
            "FEM pico (V)": prev_candidato["fem_pico_V"],
            "Potência AC (W)": prev_candidato["potencia_ac_W"],
            "Torque resistente (N·m)": prev_candidato["torque_resistente_Nm"],
        })
    st.dataframe(comparacao_motores, hide_index=True, width="stretch")
    st.caption("Comparação CALCULADA no mesmo ponto de rotação e carga resistiva. Não é ensaio comparativo nem curva completa de desempenho.")
    st.caption("Acoplamento quase estacionário: o torque equivalente no ponto de referência é aplicado à dinâmica para comparação.")
    ac_em, _, _ = acoplar_carga_resistiva(r, raio_d, relacao_G, eta_t, parametros_motor, resistencia_carga)
    if ac_em.status == "DESCE_COM_CARGA":
        st.metric("Tempo com torque eletromecânico", numero(ac_em.tempo_final_s) + " s")
        st.metric("Aceleração com torque eletromecânico", numero(ac_em.aceleracao_m_s2) + " m/s²")
    else:
        st.warning("A carga elétrica equivalente bloqueia a descida no modelo quase estacionário.")
    with st.expander("Verificação do modelo: integração dinâmica", expanded=False):
        dinamica_em = simular_descida_eletromecanica(
            r, raio_d, relacao_G, eta_t, parametros_motor, resistencia_carga,
            passo_s=0.002)
        estados_dinamicos = dinamica_em["estados"]
        st.caption("A integração numérica atualiza o torque conforme a velocidade. Esta curva é diagnóstico científico e usa a hipótese de carga resistiva equivalente.")
        st.metric("Passos numéricos", str(len(estados_dinamicos)))
        if dinamica_em["status"] == "DESCE":
            energia_eletrica_dinamica_J = estados_dinamicos[-1]["energia_acumulada_J"]
            st.metric("Tempo dinâmico", numero(estados_dinamicos[-1]["tempo_s"]) + " s")
            st.metric("Velocidade final dinâmica", numero(estados_dinamicos[-1]["velocidade_m_s"]) + " m/s")
            st.markdown("**Grandezas dinâmicas da verificação**")
            grafico(charts.serie_dinamica(estados_dinamicos, "velocidade_m_s", "Velocidade", "Velocidade (m/s)"), "dinamica_velocidade")
            grafico(charts.serie_dinamica(estados_dinamicos, "torque_eletromagnetico_Nm", "Torque eletromagnético", "Torque (N·m)"), "dinamica_torque")
            grafico(charts.serie_dinamica(estados_dinamicos, "potencia_ac_W", "Potência AC", "Potência (W)"), "dinamica_potencia")
            grafico(charts.serie_dinamica(estados_dinamicos, "energia_acumulada_J", "Energia AC acumulada", "Energia (J)"), "dinamica_energia")
            ed = estados_dinamicos[-1]
            st.metric("Energia AC acumulada", numero(ed["energia_acumulada_J"]) + " J")
            st.metric("Perda de cobre acumulada", numero(ed["perda_cobre_acumulada_J"]) + " J")
            st.download_button("Baixar trajetória dinâmica CSV", serializar_trajetoria(estados_dinamicos), "gravbat_trajetoria_dinamica.csv", "text/csv")
st.subheader("Verificação da carga mecânica")
st.warning("Carga mecânica genérica de torque constante. Não representa torque de gerador. A energia entregue é mecânica e a eficiência é somente da transmissão.")
with st.sidebar:
    carga_ativa=st.checkbox("Ativar carga acoplada", value=False, key="carga_ativa")
    tau_carga=st.number_input("Torque da carga τ (N·m)", value=0.0, min_value=0.0, step=.01, format="%.4f", key="tau_carga")
ac=acoplar(r, tau_carga if carga_ativa else 0.0, raio_d, relacao_G, eta_t)
ae=ac.estados(config.N_AMOSTRAS); af=ae[-1]
if ac_em.status == "DESCE_COM_CARGA":
    with st.expander("Verificação do modelo: comparação entre cargas", expanded=False):
        st.caption("Diagnóstico de desenvolvimento; não é o resultado principal do cenário.")
        st.markdown("**Velocidade: sem carga, carga mecânica e carga eletromecânica**")
        estados_em = ac_em.estados(config.N_AMOSTRAS)
        comparacao_em = []
        for e_sem, e_mec, e_em in zip(estados, ae, estados_em):
            comparacao_em.append({"tempo_s": e_em["tempo_s"], "sem": e_sem.velocidade_m_s,
                                  "mecanica": e_mec["velocidade_m_s"],
                                  "eletromecanica": e_em["velocidade_m_s"]})
        fig_em = charts.comparacao_linhas(comparacao_em, "Velocidade (m/s)", "velocidade")
        grafico(fig_em, "cmp_eletromecanica_vel")
    st.subheader("Ciclo de armazenamento")
    potencia_subida = st.number_input("Potência externa para subida (W)", value=10.0, min_value=0.000001, step=1.0, key="potencia_subida")
    eta_subida = st.number_input("Eficiência da subida", value=0.8, min_value=0.000001, max_value=1.0, step=.05, key="eta_subida")
    ciclo = ciclo_descida_subida(
        r, ac_em, potencia_subida, eta_subida,
        energia_gerada_J=energia_eletrica_dinamica_J,
        origem_energia="SIMULADO_DINAMICO_AC" if energia_eletrica_dinamica_J is not None else "CALCULADO_V04_MECANICO",
    )
    if ciclo["status"] == "COMPLETA":
        cv = st.columns(4)
        cv[0].metric("Energia elétrica na descida", numero(ciclo["energia_gerada_J"]) + " J")
        cv[1].metric("Energia consumida na subida", numero(ciclo["energia_subida_J"]) + " J")
        cv[2].metric("Saldo líquido do ciclo", numero(ciclo["saldo_liquido_J"]) + " J")
        cv[3].metric("Tempo do ciclo", numero(ciclo["tempo_ciclo_s"]) + " s")
        potencia_media_descida = ciclo["energia_gerada_J"] / ciclo["tempo_descida_s"] if ciclo["tempo_descida_s"] else 0.0
        potencia_pico_descida = max((e["potencia_ac_W"] for e in estados_dinamicos), default=0.0) if estados_dinamicos else 0.0
        cp = st.columns(3)
        cp[0].metric("Potência elétrica média", numero(potencia_media_descida) + " W")
        cp[1].metric("Potência elétrica de pico", numero(potencia_pico_descida) + " W")
        cp[2].metric("Eficiência do ciclo", numero(ciclo["eficiencia_ciclo"] * 100) + " %")
        st.info("Resposta operacional do cenário: valores simulados/calculados para este conjunto de hipóteses; não representam dimensionamento executivo nem validação experimental.")
        st.caption(f"Energia de descida: {ciclo['origem_energia']}. A subida usa potência prescrita; o saldo é uma estimativa do modelo e não valida uma instalação real.")
if ac.status == "NAO_DESCE_COM_CARGA": st.error("NAO_DESCE_COM_CARGA · A força resistente da carga elimina a aceleração líquida. Não há percurso, tempo ou energia entregue.")
else: st.success("DESCE_COM_CARGA · A carga altera a aceleração e a rotação no modelo analítico.")
st.caption("A carga mecânica altera a trajetória: torque refletido → tensão no cabo → força resistente → aceleração. Ela permanece separada da conversão eletromecânica dinâmica.")
cc=st.columns(4)
cc[0].metric("Torque da carga", numero(ac.tau_carga_Nm)+" N·m")
cc[1].metric("Torque refletido no tambor", numero(ac.torque_tambor_resistente_Nm)+" N·m")
cc[2].metric("Força no cabo", numero(ac.forca_carga_N)+" N")
cc[3].metric("Torque limite de partida", numero(ac.torque_limite_v04_Nm)+" N·m")
ec=st.columns(4)
ec[0].metric("Energia entregue à carga", numero(af['carga_J'])+" J")
ec[1].metric("Perda da transmissão", numero(af['perda_transmissao_J'])+" J")
ec[2].metric("Potência mecânica média", numero(af['carga_J']/ac.tempo_final_s if ac.tempo_final_s else 0)+" W")
ec[3].metric("Potência mecânica final", numero(af['potencia_carga_W'])+" W")
with st.expander("Limite de torque e balanço mecânico"):
    st.write("Torque limite de partida — modelo V0.4: valor teórico que leva a aceleração líquida a zero. Não representa limite experimental ou do futuro gerador.")
    st.write("O balanço inclui energia cinética, rolamento, energia entregue à carga e perda da transmissão. A carga é mecânica, nunca elétrica.")
if carga_ativa and ac.status == "DESCE_COM_CARGA":
    with st.expander("Verificação V0.4: carga mecânica", expanded=False):
        st.markdown("**Velocidade sem carga versus com carga**")
        cmp=[]
        for e, x in zip(estados, ae): cmp.append({"tempo_s":x['tempo_s'],"sem":e.velocidade_m_s,"com":x['velocidade_m_s']})
        grafico(charts.comparacao_linhas(cmp,"Velocidade (m/s)","velocidade"),"cmp_vel")
        st.markdown("**RPM de saída sem carga versus com carga**")
        cmp_r=[]
        for e, x in zip(estados, ae): cmp_r.append({"tempo_s":x['tempo_s'],"sem":cinematica(e.velocidade_m_s,raio_d,relacao_G).rpm_saida,"com":x['rpm_saida']})
        grafico(charts.comparacao_linhas(cmp_r,"RPM de saída","rpm"),"cmp_rpm")
        st.markdown("**Potência mecânica na carga versus tempo**")
        grafico(charts.velocidade_tempo([type('E',(),{'tempo_s':x['tempo_s'],'velocidade_m_s':x['potencia_carga_W']}) for x in ae]),"pot_carga")
        st.markdown("**Balanço energético final da carga mecânica**")
        grafico(charts.barras_energia({'Cinética':af['cinetica_J'],'Rolamento':af['rolamento_J'],'Carga mecânica':af['carga_J'],'Perda transmissão':af['perda_transmissao_J']}),"balanco_v04")
else:
    st.caption("A carga mecânica V0.4 está desligada; os gráficos de diagnóstico dessa carga ficam ocultos.")

st.subheader("Interpretação do cenário")
st.write(interpretar(r))
st.subheader("Relatório reproduzível do cenário")
with st.expander("Gerar registro para o TCC", expanded=False):
    resultado_relatorio = {
        "energia_potencial_J": final.energia.inicial_J,
        "tempo_descida_s": r.tempo_final_s,
        "velocidade_final_m_s": final.velocidade_m_s,
        "ciclo": ciclo if ciclo is not None else {"status": "NÃO DISPONÍVEL"},
    }
    entradas_relatorio = {
        "massa_kg": r.massa_kg,
        "inclinacao_graus": r.geometria.theta_graus,
        "comprimento_m": r.geometria.L_m,
        "resistencia_equivalente": r.c_r,
        "motor_id": motor_selecionado.id,
        "motor_nome": motor_selecionado.nome,
        "motor_status": motor_selecionado.status,
        "motor_origem": motor_selecionado.origem,
        "motor_observacao": motor_selecionado.observacao,
    }
    relatorio = relatorio_cenario(
        entradas_relatorio,
        resultado_relatorio,
        ["massa pontual", "c_r constante", "partida a partir do repouso", "eficiências configuráveis"],
        ["sem validação experimental", "sem projeto civil", "sem curva de carga real", "sem disponibilidade ou despacho"],
    )
    st.json(relatorio)
    st.download_button("Baixar relatório JSON", serializar_relatorio(relatorio), "gravbat_cenario.json", "application/json")
    st.download_button("Baixar tabela CSV", serializar_tabela_relatorio(relatorio), "gravbat_cenario.csv", "text/csv")
st.subheader("Dimensionamento por demanda")
with st.expander("Testar uma demanda de energia e potência", expanded=False):
    dc = st.columns(5)
    demanda_kwh = dc[0].number_input("Energia útil (kWh)", value=1.0, min_value=.000001, step=.5, key="demanda_kwh")
    demanda_kw = dc[1].number_input("Potência máxima (kW)", value=.2, min_value=.000001, step=.1, key="demanda_kw")
    altura_dim = dc[2].number_input("Altura útil (m)", value=10.0, min_value=.000001, step=1.0, key="altura_dim")
    eta_dim = dc[3].number_input("Eficiência global", value=.5, min_value=.000001, max_value=1.0, step=.05, key="eta_dim")
    tempo_dim = dc[4].number_input("Duração (h)", value=2.0, min_value=.000001, step=.5, key="tempo_dim")
    dim = dimensionar_demanda(demanda_kwh, demanda_kw, altura_dim, eta_dim, tempo_dim)
    dm = st.columns(3)
    dm[0].metric("Massa estimada", numero(dim["massa_total_kg"]) + " kg")
    dm[1].metric("Potência média", numero(dim["potencia_media_kW"]) + " kW")
    dm[2].metric("Potência máxima informada", numero(dim["potencia_max_kW"]) + " kW")
    if ciclo is not None and ciclo.get("status") == "COMPLETA" and ciclo.get("energia_gerada_J", 0.0) > 0:
        energia_modulo_kWh = ciclo["energia_gerada_J"] / 3_600_000
        modulos_energia = demanda_kwh / energia_modulo_kWh
        modulos_potencia = (demanda_kw * 1000) / max(ciclo["energia_gerada_J"] / ciclo["tempo_descida_s"], 1e-12)
        modulos_requeridos = max(1, math.ceil(max(modulos_energia, modulos_potencia)))
        st.markdown("**Estimativa baseada no ciclo simulado atual**")
        md = st.columns(4)
        md[0].metric("Energia por módulo/ciclo", numero(energia_modulo_kWh) + " kWh")
        md[1].metric("Módulos por energia", numero(modulos_energia))
        md[2].metric("Módulos por potência", numero(modulos_potencia))
        md[3].metric("Módulos estimados", str(modulos_requeridos))
        st.caption("Estimativa calculada usando a energia e a potência da descida simulada. Não inclui disponibilidade, armazenamento intermediário, despacho, redundância, limites térmicos ou projeto civil.")
    st.caption("Estimativa energética de ordem de grandeza. Não é projeto executivo nem comprovação de atendimento da potência máxima.")
st.subheader("Pergunta de aplicação")
with st.expander("Fazer uma pergunta de escala", expanded=False):
    st.caption("Os cenários abaixo são hipóteses de entrada para explorar ordens de grandeza. Substitua-os por dados de consumo, terreno e operação quando disponíveis.")
    nome_aplicacao = st.selectbox("Aplicação de referência", list(SCENARIOS), key="aplicacao_referencia")
    aplicacao = obter_cenario(nome_aplicacao)
    st.write(aplicacao["observacao"])
    acols = st.columns(5)
    e_app = acols[0].number_input("Energia útil (kWh)", value=float(aplicacao["energia_util_kWh"]), min_value=.000001, key="app_energia")
    p_app = acols[1].number_input("Potência máxima (kW)", value=float(aplicacao["potencia_max_kW"]), min_value=.000001, key="app_potencia")
    h_app = acols[2].number_input("Desnível útil (m)", value=float(aplicacao["altura_m"]), min_value=.000001, key="app_altura")
    t_app = acols[3].number_input("Duração de descarga (h)", value=float(aplicacao["tempo_descarga_h"]), min_value=.000001, key="app_tempo")
    eta_app = acols[4].number_input("Eficiência global", value=float(aplicacao["eficiencia_global"]), min_value=.000001, max_value=1.0, key="app_eta")
    comprimento_app = st.number_input("Comprimento do percurso (m)", value=max(h_app * 8.0, 1.0), min_value=.000001, key="app_comprimento")
    inclinacao_app = math.degrees(math.asin(min(h_app / comprimento_app, 1.0)))
    st.caption(f"Geometria derivada: inclinação equivalente de {numero(inclinacao_app)}°. O cálculo usa o desnível vertical; o comprimento é uma verificação geométrica.")
    if h_app > comprimento_app:
        st.error("O desnível não pode ser maior que o comprimento do percurso.")
    resultado_app = dimensionar_demanda(e_app, p_app, h_app, eta_app, t_app)
    appm = st.columns(4)
    appm[0].metric("Massa gravitacional", numero(resultado_app["massa_total_kg"]) + " kg")
    appm[1].metric("Potência média", numero(resultado_app["potencia_media_kW"]) + " kW")
    appm[2].metric("Energia armazenada requerida", numero(e_app / eta_app) + " kWh")
    appm[3].metric("Razão potência/média", numero(p_app / resultado_app["potencia_media_kW"]) + " vezes")
    st.dataframe([
        {"Parâmetro": "Energia útil", "Valor": f"{numero(e_app)} kWh", "Classificação": "HIPÓTESE / ENTRADA"},
        {"Parâmetro": "Potência máxima", "Valor": f"{numero(p_app)} kW", "Classificação": "HIPÓTESE / ENTRADA"},
        {"Parâmetro": "Desnível", "Valor": f"{numero(h_app)} m", "Classificação": "HIPÓTESE / ENTRADA"},
        {"Parâmetro": "Comprimento", "Valor": f"{numero(comprimento_app)} m", "Classificação": "HIPÓTESE / GEOMETRIA"},
        {"Parâmetro": "Eficiência global", "Valor": f"{numero(eta_app * 100)} %", "Classificação": "HIPÓTESE / CONFIGURÁVEL"},
    ], hide_index=True, width="stretch")
    st.caption(f"Classificação: {aplicacao['status']}. Resultado CALCULADO pelo modelo energético; não é projeto executivo, estudo de rede ou validação de curtailment.")
st.subheader("Sensibilidade do cenário")
with st.expander("Comparar alturas e eficiências", expanded=False):
    cenarios = [
        {"nome": "Altura baixa", "energia_util_kWh": demanda_kwh, "potencia_max_kW": demanda_kw, "altura_m": max(altura_dim / 2, .000001), "eficiencia_global": eta_dim, "tempo_descarga_h": tempo_dim},
        {"nome": "Cenário atual", "energia_util_kWh": demanda_kwh, "potencia_max_kW": demanda_kw, "altura_m": altura_dim, "eficiencia_global": eta_dim, "tempo_descarga_h": tempo_dim},
        {"nome": "Altura alta", "energia_util_kWh": demanda_kwh, "potencia_max_kW": demanda_kw, "altura_m": altura_dim * 2, "eficiencia_global": eta_dim, "tempo_descarga_h": tempo_dim},
        {"nome": "Eficiência baixa", "energia_util_kWh": demanda_kwh, "potencia_max_kW": demanda_kw, "altura_m": altura_dim, "eficiencia_global": max(eta_dim * .7, .000001), "tempo_descarga_h": tempo_dim},
        {"nome": "Eficiência alta", "energia_util_kWh": demanda_kwh, "potencia_max_kW": demanda_kw, "altura_m": altura_dim, "eficiencia_global": min(eta_dim * 1.2, 1.0), "tempo_descarga_h": tempo_dim},
    ]
    tabela_cenarios = comparar_cenarios(cenarios)
    st.dataframe(tabela_cenarios, hide_index=True, width="stretch")
    st.caption("Comparação calculada para explorar sensibilidade à altura e à eficiência. Os cenários baixo/alto são perturbações paramétricas, não previsões de terreno nem valores medidos.")
st.subheader("Balanço energético por transformação")
with st.expander("Definir eficiências parciais", expanded=False):
    st.caption("Os valores abaixo são entradas de cenário. Nenhum deles é tratado como medição do GravBat.")
    ef = st.columns(6)
    eta_mec = ef[0].number_input("Mecânica", value=1.0, min_value=.000001, max_value=1.0, step=.05, key="eta_mec")
    eta_trans = ef[1].number_input("Transmissão", value=eta_t, min_value=.000001, max_value=1.0, step=.05, key="eta_trans_chain")
    eta_ger = ef[2].number_input("Gerador", value=1.0, min_value=.000001, max_value=1.0, step=.05, key="eta_ger")
    eta_ret = ef[3].number_input("Retificador", value=1.0, min_value=.000001, max_value=1.0, step=.05, key="eta_ret")
    eta_conv = ef[4].number_input("Conversor", value=1.0, min_value=.000001, max_value=1.0, step=.05, key="eta_conv")
    eta_carga = ef[5].number_input("Carga", value=1.0, min_value=.000001, max_value=1.0, step=.05, key="eta_carga")
    etapas = balanço_transformacoes(final.energia.inicial_J, (eta_mec, eta_trans, eta_ger, eta_ret, eta_conv, eta_carga))
    st.dataframe([{"Etapa": e.nome, "Entrada (J)": e.entrada_J, "Saída (J)": e.saida_J, "Perda (J)": e.perda_J, "Eficiência": e.eficiencia, "Status": e.status} for e in etapas], hide_index=True, width="stretch")
    st.metric("Eficiência global do cenário", numero(etapas[-1].saida_J / final.energia.inicial_J if final.energia.inicial_J else 0))
    st.download_button("Baixar balanço de transformações CSV", serializar_transformacoes(etapas), "gravbat_balanco_transformacoes.csv", "text/csv")
with st.expander("Hipóteses do modelo"):
    st.markdown("""- Massa pontual, rampa retilínea e rígida, repouso inicial.
- Gravidade adotada g = 9,81 m/s² e c_r constante.
- c_r representa resistência equivalente ao rolamento em movimento; não atrito estático.
- **APROXIMAÇÃO DO MODELO V0.1:** partida quando a força gravitacional paralela supera c_r N. Caso contrário, aceleração efetiva zero.
- Ausência de inércia rotacional, arrasto, cabo, tambor, transmissão, gerador, eletrônica, controle e frenagem.
- Simulação encerrada antes de colisão/frenagem; energia cinética final permanece no corpo.
- Interface V0.2 usa modelo físico V0.1. Geometrias e parâmetros padrão são assumidos; validação experimental pendente.""")

st.subheader("Evolução mecânica")
if r.tempo_final_s is None:
    st.caption("Sem trajetória de descida: os gráficos mostram somente o estado em repouso, em t=0 e s=0.")
st.markdown("**Energia versus posição**")
grafico(charts.energia_posicao(estados), "energia")
st.markdown("**Velocidade versus tempo**")
grafico(charts.velocidade_tempo(estados), "velocidade")
st.markdown("**Forças no plano inclinado**")
grafico(charts.forcas(r), "forcas")

st.subheader("Efeito da inclinação · 1° a 45°")
st.caption("Varredura com massa e c_r atuais. " + ("Comprimento L fixo; desnível H varia." if modo == "laboratorio" else "Desnível H fixo; comprimento L varia."))
bloqueados = [p["theta_graus"] for p in sweep if p["status"] == "NAO_DESCE"]
if bloqueados:
    st.warning("NAO_DESCE nos ângulos: " + ", ".join(map(str, bloqueados)) + "°. Nesses pontos, perda real = 0% por ausência de percurso; tempo de descida ausente. Isso não representa uma descida sem perdas.")
st.markdown("**Perda por rolamento versus inclinação**")
grafico(charts.varredura(sweep, "perda_percentual", "Energia inicial dissipada (%)"), "sweep_perda")
st.markdown("**Tempo de descida versus inclinação**")
grafico(charts.varredura(sweep, "tempo_descida_s", "Tempo de descida (s)"), "sweep_tempo")
with st.expander("Dados da varredura"):
    st.dataframe(sweep, hide_index=True, width="stretch")
