"""Apresentação Plotly; nenhuma equação de movimento nesta camada."""
import plotly.graph_objects as go

CORES = ("#16857b", "#365ec9", "#d07b20")


def estilo(fig, x, y):
    fig.update_layout(xaxis_title=x, yaxis_title=y, height=350,
                      margin=dict(l=20, r=20, t=20, b=20),
                      legend=dict(orientation="h", y=-.25), hovermode="x unified")
    return fig


def energia_posicao(estados):
    fig = go.Figure()
    for nome, campo, cor in zip(("Potencial restante", "Cinética", "Perda acumulada por rolamento"),
                                ("restante_J", "cinetica_J", "perda_rolamento_J"), CORES):
        fig.add_scatter(x=[e.posicao_m for e in estados],
                        y=[getattr(e.energia, campo) for e in estados], name=nome,
                        mode="lines" if len(estados) > 1 else "markers", line_color=cor)
    return estilo(fig, "Posição na rampa (m)", "Energia (J)")


def velocidade_tempo(estados):
    fig = go.Figure(go.Scatter(x=[e.tempo_s for e in estados], y=[e.velocidade_m_s for e in estados],
                              mode="lines" if len(estados) > 1 else "markers", name="Velocidade", line_color=CORES[1]))
    return estilo(fig, "Tempo (s)", "Velocidade (m/s)")


def velocidade_tempo_marcada(estados, tempo_atual, velocidade_alvo=None, duracao_alvo_s=None):
    """Curva pré-calculada com marcador do instante visual atual."""
    fig = velocidade_tempo(estados)
    if velocidade_alvo is not None:
        fim = max(estados[-1].tempo_s if estados else 1.0, duracao_alvo_s or 0.0)
        fig.add_scatter(x=[0, fim], y=[velocidade_alvo, velocidade_alvo],
                        mode="lines", name="Velocidade-alvo (hipótese)",
                        line=dict(color="#e2a84a", dash="dash"))
    if estados:
        atual = min(estados, key=lambda e: abs(e.tempo_s - tempo_atual))
        fig.add_vline(x=atual.tempo_s, line_color="#3ac2a2", line_width=2)
        fig.add_scatter(x=[atual.tempo_s], y=[atual.velocidade_m_s],
                        mode="markers", name="Instante atual",
                        marker=dict(size=10, color="#3ac2a2"))
    fig.update_layout(height=420, paper_bgcolor="#0d1118", plot_bgcolor="#0d1118",
                      font=dict(color="#dbe5f0"))
    return fig


def energia_posicao_marcada(estados, posicao_atual):
    fig = energia_posicao(estados)
    if estados:
        atual = min(estados, key=lambda e: abs(e.posicao_m - posicao_atual))
        fig.add_vline(x=atual.posicao_m, line_color="#3ac2a2", line_width=2)
    fig.update_layout(height=420, paper_bgcolor="#0d1118", plot_bgcolor="#0d1118",
                      font=dict(color="#dbe5f0"))
    return fig


def esquema_rampa(progresso, potencia_W=0.0):
    """Esquema didático compacto da rampa, massa e lâmpada."""
    p = max(0.0, min(1.0, progresso))
    x0, y0 = 1.0, 1.0
    x1, y1 = 9.0, 5.5
    xb = x0 + p * (x1 - x0)
    yb = y0 + p * (y1 - y0)
    brilho = max(0.15, min(1.0, abs(potencia_W) / 2.0))
    fig = go.Figure()
    fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1, line=dict(color="#365ec9", width=8))
    fig.add_shape(type="line", x0=1, y0=0.6, x1=1, y1=1.0, line=dict(color="#555", width=3))
    fig.add_shape(type="rect", x0=xb-.35, y0=yb-.25, x1=xb+.35, y1=yb+.25,
                 fillcolor="#d07b20", line=dict(color="#8a4f10", width=2))
    fig.add_shape(type="line", x0=9, y0=5.5, x1=10.2, y1=5.5, line=dict(color="#555", width=3))
    fig.add_shape(type="circle", x0=10.2, y0=5.15, x1=10.9, y1=5.85,
                 fillcolor=f"rgba(255, 215, 0, {brilho})", line=dict(color="#b8860b", width=2))
    fig.add_annotation(x=xb, y=yb+.55, text="massa", showarrow=False, font=dict(size=12))
    fig.add_annotation(x=10.55, y=4.8, text="carga", showarrow=False, font=dict(size=12))
    fig.update_xaxes(visible=False, range=[0, 11])
    fig.update_yaxes(visible=False, range=[0, 6.5], scaleanchor="x", scaleratio=1)
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                      title="Representação do ciclo mecânico → elétrico")
    return fig


def forcas(r):
    f = r.forcas
    fig = go.Figure(go.Bar(x=["Força gravitacional<br>paralela", "Resistência ao<br>rolamento", "Força líquida<br>no movimento"],
                          y=[f.grav_paralela_N, f.rol_movimento_N, f.disponivel_N],
                          marker_color=[CORES[0], CORES[2], CORES[1]]))
    return estilo(fig, "Componente", "Força (N)")


def varredura(linhas, campo, unidade):
    fig = go.Figure(go.Scatter(x=[p["theta_graus"] for p in linhas],
                              y=[p[campo] if p["status"] == "DESCE" else None for p in linhas],
                              mode="lines+markers", name="DESCE", connectgaps=False, line_color=CORES[0]))
    bloqueados = [p for p in linhas if p["status"] == "NAO_DESCE"]
    if bloqueados:
        if campo == "perda_percentual":
            fig.add_scatter(x=[p["theta_graus"] for p in bloqueados], y=[p[campo] for p in bloqueados],
                            mode="markers", marker=dict(symbol="x", size=9, color=CORES[2]),
                            name="NAO_DESCE: 0% sem percurso")
        else:
            # Faixa em coordenadas do painel, sem inventar um tempo para bloqueados.
            fig.add_vrect(x0=min(p["theta_graus"] for p in bloqueados)-.4,
                          x1=max(p["theta_graus"] for p in bloqueados)+.4,
                          fillcolor=CORES[2], opacity=.12, line_width=0,
                          annotation_text="NAO_DESCE · tempo não aplicável", annotation_position="top left")
    return estilo(fig, "Inclinação (°)", unidade)


def rpm_tempo(linhas):
    fig = go.Figure()
    fig.add_scatter(x=[p["tempo_s"] for p in linhas], y=[p["rpm_tambor"] for p in linhas], name="Tambor")
    fig.add_scatter(x=[p["tempo_s"] for p in linhas], y=[p["rpm_saida"] for p in linhas], name="Eixo de saída")
    return estilo(fig, "Tempo (s)", "Rotação (RPM)")


def varredura_G(linhas):
    fig = go.Figure(go.Scatter(x=[p["G"] for p in linhas], y=[p["rpm_saida"] for p in linhas], mode="lines+markers", name="RPM de saída"))
    return estilo(fig, "Relação G", "RPM final de saída")

def comparacao_linhas(linhas, nome_y, y):
    fig=go.Figure()
    series = (("Sem carga", "sem"), ("Com carga", "com"))
    if linhas and "mecanica" in linhas[0]:
        series = (("Sem carga", "sem"), ("Carga mecânica V0.4", "mecanica"),
                  ("Carga eletromecânica V0.5", "eletromecanica"))
    for nome, chave in series:
        fig.add_scatter(x=[p["tempo_s"] for p in linhas], y=[p[chave] for p in linhas], name=nome)
    return estilo(fig,"Tempo (s)",nome_y)

def barras_energia(d):
    fig=go.Figure(go.Bar(x=list(d),y=list(d.values()),marker_color=CORES))
    return estilo(fig,"Termo energético","Energia (J)")


def serie_dinamica(linhas, campo, nome, eixo_y):
    fig = go.Figure(go.Scatter(x=[p["tempo_s"] for p in linhas],
                               y=[p[campo] for p in linhas], mode="lines",
                               name=nome, line_color=CORES[1]))
    return estilo(fig, "Tempo (s)", eixo_y)
