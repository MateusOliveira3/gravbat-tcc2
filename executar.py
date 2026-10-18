"""Reproduz testes, cenários e relatório V0.1 usando biblioteca padrão."""
import csv
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import unittest

import config
from simulation.simulator import simular

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
FONTES = (
    ROOT / "work" / "tcc2_modelo_mecanico_v01.py",
    ROOT / "work" / "TCC 3.0.1.docx.pdf",
    ROOT / "work" / "Texto colado.txt",
)


def csv_gravar(nome, linhas):
    with (OUT / nome).open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)


def resumo(nome, r):
    amostras = r.amostras(config.N_AMOSTRAS)
    final = amostras[-1]
    return dict(caso=nome, modo=r.geometria.modo, massa_kg=r.massa_kg,
                g_m_s2=r.g_m_s2, theta_graus=r.geometria.theta_graus, c_r=r.c_r,
                L_m=r.geometria.L_m, H_m=r.geometria.H_m,
                **asdict(r.forcas), tempo_final_s=r.tempo_final_s,
                posicao_final_m=final.posicao_m, velocidade_final_m_s=final.velocidade_m_s,
                **asdict(final.energia),
                residuo_max_durante_J=max(abs(e.energia.residuo_energia_J) for e in amostras),
                classificacao="RESULTADO SIMULADO")


def tabela(linhas):
    chaves = ("caso", "theta_graus", "L_m", "H_m", "tempo_final_s", "velocidade_final_m_s", "inicial_J", "restante_J", "cinetica_J", "perda_rolamento_J", "residuo_max_durante_J", "residuo_energia_J")
    nomes = ("Caso", "θ (°)", "L (m)", "H (m)", "t (s)", "v (m/s)", "Ei (J)", "Ep final (J)", "K final (J)", "Erol (J)", "máx abs(r) (J)", "r final (J)")
    texto = "| " + " | ".join(nomes) + " |\n|" + "---|" * len(nomes) + "\n"
    for linha in linhas:
        valores = []
        for chave in chaves:
            v = linha[chave]
            valores.append("não alcança" if v is None else f"{v:.6g}" if isinstance(v, float) else str(v))
        texto += "| " + " | ".join(valores) + " |\n"
    return texto


def main():
    OUT.mkdir(exist_ok=True)
    log = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    testes = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    (OUT / "testes.log").write_text(log.getvalue(), encoding="utf-8")
    if not testes.wasSuccessful():
        print(log.getvalue())
        return 1
    linhas, trajetorias = [], []
    for modo, dimensao in (("laboratorio", {"L_m": config.L_LAB_M}), ("terreno", {"H_m": config.H_TERRENO_M})):
        for theta in config.ANGULOS_GRAUS:
            r = simular(config.MASSA_KG, theta, config.C_R, modo, g_m_s2=config.G_M_S2, **dimensao)
            nome = f"{modo}_{theta}"
            linhas.append(resumo(nome, r))
            for e in r.amostras(config.N_AMOSTRAS):
                trajetorias.append(dict(caso=nome, tempo_s=e.tempo_s, posicao_m=e.posicao_m,
                                        velocidade_m_s=e.velocidade_m_s, **asdict(e.energia)))
    csv_gravar("cenarios_12.csv", linhas)
    csv_gravar("trajetorias.csv", trajetorias)
    base = simular(6, 10, 0, "laboratorio", L_m=1.2)
    critico = base.forcas.grav_paralela_N / base.forcas.normal_N
    limites = [resumo(nome, simular(6, ang, cr, "laboratorio", L_m=1.2)) for nome, ang, cr in (
        ("ideal", 10, 0), ("bloqueado", 10, 1), ("limiar", 10, critico),
        ("abaixo_limiar", 10, critico * (1 - 1e-9)),
        ("acima_limiar", 10, critico * (1 + 1e-9)),
        ("quase_horizontal_ideal", 1e-6, 0), ("quase_vertical", 89.999999, .02))]
    csv_gravar("casos_limite.csv", limites)
    csv_gravar("origem_parametros.csv", [dict(parametro=k, classificacao=v[0], origem_status=v[1]) for k, v in config.ORIGENS.items()])
    fontes = [dict(caminho=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "indisponível nesta reprodução") for p in FONTES]
    (OUT / "fontes_sha256.json").write_text(json.dumps(fontes, ensure_ascii=False, indent=2), encoding="utf-8")
    max_d = max(r["residuo_max_durante_J"] for r in linhas)
    max_f = max(abs(r["residuo_energia_J"]) for r in linhas)
    exec_log = f"Python {platform.python_version()}\nExecutável: {sys.executable}\nComando: python -B executar.py\nTestes: {testes.testsRun}, falhas: {len(testes.failures)}, erros: {len(testes.errors)}\n12 cenários, {config.N_AMOSTRAS} amostras/cenário, {len(trajetorias)} estados exportados\n7 casos limite\nMáximo |resíduo| durante: {max_d:.17g} J\nMáximo |resíduo| final: {max_f:.17g} J\n"
    (OUT / "execucao.log").write_text(exec_log, encoding="utf-8")
    (OUT / "tabela_12_casos.md").write_text(tabela(linhas), encoding="utf-8")
    # Cria nomes finais antes de obter a árvore real.
    for nome in ("relatorio_v01.md", "arvore.txt"):
        (OUT / nome).touch(exist_ok=True)
    arquivos = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    arvore = str(ROOT) + "\n" + "\n".join("  " + p for p in arquivos) + "\n"
    (OUT / "arvore.txt").write_text(arvore, encoding="utf-8")
    rel = f"""# GravBat TCC 2 - entrega da Fase 1 / V0.1

Núcleo mecânico consolidado em `{ROOT}`. Encerrado para revisão. O modelo computacional é o produto principal; o protótipo é opcional para validação. Sem UI nesta entrega. V0.2 será dashboard mecânico, conforme decisão mais recente, substituindo o roadmap antigo do script.

## 1. Árvore real e arquivos criados

```text
{arvore}```

Todos os arquivos da árvore foram criados nesta pasta exclusiva. `work/tcc1_extraido.txt` é extração auxiliar; código em model/, simulation/, config.py, executar.py e tests/; documentação em README.md e outputs/. Nenhuma fonte original foi modificada. A única cópia externa autorizada é a promoção dos entregáveis para a pasta indicada da conversa de origem; o código permanece aqui. Hashes das três fontes estão em fontes_sha256.json.

## 2. Alterações em relação ao script original

Preservadas as equações analíticas de descida. Separadas geometria, forças, energia e simulação. Removidas dependências de matplotlib, numpy e pandas; nenhuma dependência de Plotly/Streamlit. Importação não cria resultados. Adicionadas validações, configuração central, origem/status, trajetória energética e testes. Corrigido bloqueio: não contabiliza percurso ou perda inexistente. Força disponível e aceleração efetiva são distintas. Não há estimativa elétrica nem benchmark no núcleo.

## 3. Equações e unidades implementadas

- Laboratório: H = L sen θ; terreno: L = H/sen θ. L e H em m.
- N = mg cos θ; Fg = mg sen θ; Fr = c_r N; Fdisp = Fg - Fr (N).
- Se Fdisp > 0: a = Fdisp/m (m/s²); tf = √(2L/a) (s); s(t) = at²/2 (m); v(t) = at (m/s).
- Ei = mgH; Ep(t) = mg[H - s(t) sen θ]; K(t) = mv(t)²/2; Erol(t) = Fr s(t), todas em J.
- residuo_energia_J = Ei - [Ep + K + Erol]. Resíduo numérico NÃO é perda física.
- Para Fdisp <= 0, a efetiva = s = v = K = Erol = 0, Ep = Ei e tf = None (fim não alcançado).

Substituindo a na soma K + Erol obtém-se (Fdisp + Fr)s = mg sen θ s. Somando Ep recupera-se Ei em qualquer instante do domínio analítico. A avaliação discreta verifica a implementação em ponto flutuante; não substitui essa identidade. No instante final s=L é condição de contorno exata; não há colisão/frenagem e K permanece positiva.

## 4. Hipóteses e rastreabilidade

Repouso inicial, massa pontual, rampa retilínea, gravidade e resistência equivalentes constantes. Não inclui rotação, arrasto, transmissão, cabo/tambor, gerador, eletrônica ou controle. APROXIMAÇÃO DO MODELO V0.1: reutilizar Fg - c_r N > 0 para decidir partida. c_r é resistência ao rolamento EM MOVIMENTO; não é atrito estático. O valor rol_movimento_N no bloqueio é referência do modelo de movimento, não força estática medida ou perda dissipada.

g = {config.G_M_S2} m/s² é valor adotado. Massa = {config.MASSA_KG} kg e θ = {config.ANGULOS_GRAUS} graus são entradas do estudo. c_r = {config.C_R} é hipótese configurável. L_lab = {config.L_LAB_M} m e H_terreno = {config.H_TERRENO_M} m são geometrias ASSUMIDAS no script original, não medições demonstradas pelo PDF. A altura útil de 1–1,2 m discutida no TCC1 não comprova um comprimento de rampa laboratorial de 1,2 m.

`config.py` centraliza padrões e metadados. Vocabulário preparado: DADO MEDIDO, DADO DE LITERATURA, HIPÓTESE, RESULTADO CALCULADO, RESULTADO SIMULADO, RESULTADO EXPERIMENTAL. Não foram fabricados dados medidos/experimentais. Forças e geometria são calculadas; trajetórias são resultados simulados de solução analítica. Origem detalhada em origem_parametros.csv.

P_benchmark = 0,5 W é somente registro histórico do TCC1. Não se calcula potência elétrica produzida, não se impõe duração de 50/60 s, nem eficiência global de 45%. Tempo é resultado mecânico.

## 5. Testes completos e reprodução

Executar na pasta exclusiva: `python -B executar.py`. Python >= 3.10, biblioteca padrão. Alternativa com executável local: comando em README.md. Testes isolados: `python -B -m unittest discover -s tests -v`.

Tolerâncias dos testes: relativa 1e-12 e absoluta 1e-12 nas comparações gerais; resíduo absoluto <= 1e-12 J nos cenários padrão. Teste E avalia 1.001 instantes por cenário (12.012 estados). Exportação usa {config.N_AMOSTRAS} instantes por cenário. Testes A–L cobrem todos os requisitos mínimos. M–R acrescentam extremos angulares, transição, domínio temporal, escala de massa, importação e entradas ambíguas/tipos. Os subcasos são indicados individualmente se falharem.

```text
{log.getvalue()}```

Testes verificam consistência matemática e implementação; não são validação experimental.

## 6. Tabela completa dos 12 cenários

Todos com status DESCE. CSV contém precisão completa, forças, aceleração, parâmetros, energias e resíduos; tabela arredondada a seis algarismos significativos.

{tabela(linhas)}

## 7. Resíduos durante e ao final

Máximo absoluto durante as trajetórias exportadas: **{max_d:.17g} J**. Máximo absoluto final: **{max_f:.17g} J**. Cada linha da tabela/CSV traz seus resíduos. `trajetorias.csv` contém {len(trajetorias)} estados, inclusive início e fim, permitindo recalcular todos os balanços. Pequenos valores negativos de Ep final podem ocorrer por arredondamento e não são reinterpretados como perdas.

## 8. Bloqueio e casos limite

Exemplo bloqueado: massa 6 kg, θ=10°, c_r=1, L=1,2 m. Fdisp = {limites[1]['disponivel_N']:.12g} N, a efetiva = 0, deslocamento = 0, v = 0, K = 0, dissipação = 0; Ei = Ep = {limites[1]['inicial_J']:.12g} J. Tempo final não existe (None no Python; campo vazio no CSV). Não representa uma descida infinita com perdas acumuladas. `estado(t)` conserva esse estado para todo t finito não negativo.

{tabela(limites)}

No limiar numérico calculado por Fg/N, a comparação é Fdisp > 0, sem faixa de tolerância artificial. Pontos muito próximos do limiar são sensíveis a arredondamento e, principalmente, à incerteza física de c_r. A duração grande abaixo do limiar é consequência dessa aproximação, não previsão experimental comprovada. Entradas inválidas são rejeitadas com ValueError; escalas extremas que excedem representação numérica não são domínio validado.

## 9. Entregáveis e preservação

Relatório: relatorio_v01.md; tabela: tabela_12_casos.md e cenarios_12.csv; trajetórias: trajetorias.csv; limites: casos_limite.csv; evidências: testes.log, execucao.log, fontes_sha256.json; metadados: origem_parametros.csv; inventário: arvore.txt. Fontes preservadas em seus caminhos originais. O executor lê fontes somente para hash e não depende delas para calcular ou testar.

## 10. Decisões físicas e documentais pendentes

- Medir massa/geometria e caracterizar c_r e sua variação; hoje são hipóteses/entradas.
- Avaliar a aproximação de partida com evidência física; não foi criado modelo de atrito estático.
- Definir protocolo de validação experimental, se o protótipo ficar disponível, incluindo incertezas.
- Definir futuramente frenagem/colisão e destino da energia cinética após o fim; fora do domínio atual.
- Caracterizar transmissão e gerador antes de qualquer cálculo eletromecânico; não inventar constantes.
- Corrigir em revisão documental futura a referência [16]: seção de controle do TCC1 cita Åström e Murray, bibliografia lista Halliday/Resnick/Walker. PDF não alterado.

O TCC1 é fonte bibliográfica/conceitual, não comprovação experimental deste modelo. Entrega encerrada na V0.1, aguardando revisão.
"""
    (OUT / "relatorio_v01.md").write_text(rel, encoding="utf-8")
    print(exec_log)
    return 0


if __name__ == "__main__":
    sys.exit(main())

