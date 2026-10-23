# E6.2 — Modelo de descarga regulada e limites físicos

**Data:** 23/10/2026  
**Branch:** `fix/coerencia-fisica-dashboard`  
**Escopo:** implementação inicial independente; E1–E5 preservados.

## Modelo implementado

Foi criado `model/e6_controlled.py`, sem alterar os módulos anteriores.

- **Regime A — passivo:** chama `simulation.electromechanical_dynamic.simular_descida_eletromecanica` com os parâmetros do E4 e calcula separadamente energia AC aproximada (`E_em - E_cobre`), cobre, rolamento, energia cinética e resíduo.
- **Regime B — torque prescrito:** usa velocidade média `L/T` e torque limite analítico `tau = eta_t r_d F_0/G` para manter movimento uniforme. O torque é tratado como freio mecânico; portanto, energia elétrica recuperada é zero e a energia disponível após rolamento é explicitamente dissipada. Se `tau_max_Nm` for inferior ao necessário, o estado é `BLOQUEADO`.
- **Regime C:** permanece representado pelo próprio E4 passivo; a relação entre FEM, resistências, corrente e torque não foi desacoplada nem substituída por torque arbitrário. A conclusão desta rodada é que os parâmetros atuais não sustentam a descarga longa.

A hipótese de inércia rotacional desprezível permanece explícita.

## Resultados do cenário-base

`m=6 kg`, `H=1 m`, `g=9,81 m/s²`, `c_r=0,02`, `r_d=0,05 m`, `G=1`, `eta_t=0,90`, `K_e=0,1`, `R_fase=2 ohm`, duas fases, carga de 8 ohm.

| Ângulo | Regime | duração (s) | velocidade final (m/s) | torque (N m) | energia AC (J) | energia dissipada/cobre (J) | energia cinética final (J) | resíduo (J) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 10° | A passivo | 2,859 | 3,891 | 0,0778 | 4,866 | 1,216 | 45,429 | 0,672 |
| 20° | A passivo | 1,381 | 4,163 | 0,0833 | 2,618 | 0,655 | 51,981 | 0,372 |
| 30° | A passivo | 0,930 | 4,256 | 0,0851 | 1,828 | 0,457 | 54,328 | 0,208 |
| 40° | A passivo | 0,717 | 4,298 | 0,0860 | 1,432 | 0,358 | 55,430 | 0,237 |

Para o regime B, as metas de 30 s e 60 s são cinematicamente representáveis, com `v=L/T`, mas a energia elétrica é zero por definição do freio prescrito. Para 10°: `v=0,1920 m/s` em 30 s e `0,0960 m/s` em 60 s; torque requerido `0,4078 N m`. A energia potencial é `58,86 J`, rolamento `6,676 J` e energia absorvida pelo freio `52,184 J`.

Isso demonstra a diferença entre prolongar uma descida com dissipação e gerar energia elétrica útil.

## Meta de 0,5 W AC durante 60 s

A meta requer `30 J`. O limite ideal é `E_g=58,86 J`, mas o regime A fornece apenas aproximadamente `4,866 J` na carga AC para 10°. Portanto, a meta **não é atendida** pelo E4 passivo atual. O regime B mostra que uma duração de 60 s exige apenas velocidade média menor, mas não fornece energia elétrica. Um regime C controlado precisará simultaneamente de torque eletromagnético suficiente, tensão/FEM adequada em baixa velocidade, limites de corrente, perdas e balanço energético; esses elementos ainda não foram implementados.

## Arquivos e dados

- `model/e6_controlled.py`: modelo independente A/B e diagnóstico C.
- `tests/test_e6_controlled.py`: testes de chegada, saturação/bloqueio e referência passiva.
- `outputs/e6/e6_resultados.csv`: resultados reproduzíveis.
- `outputs/e6/e6_inclinacao_tempo_energia.svg`
- `outputs/e6/e6_inclinacao_velocidade.svg`
- `outputs/e6/e6_regimes_energia.svg`

Os gráficos desta rodada são diagnósticos iniciais; mapas de calor, Pareto e controle temporal completo permanecem fora do escopo autorizado desta primeira implementação.

## Verificação

- Testes específicos E6: 3 aprovados.
- Compilação dos módulos: executar `python -m py_compile` conforme o guia.
- Suíte completa: manter o registro de 88 testes, 87 aprovados e um erro ambiental Windows (`PermissionError` na limpeza de `TemporaryDirectory`).
- `git diff --check`: sem erro de whitespace.

## Limitações e próximos passos condicionados à revisão

1. O torque prescrito ainda é um balanço idealizado de freio, não um controlador implementado.
2. O regime C não possui saturação eletromagnética independente nem controle de velocidade.
3. A energia AC foi obtida pela diferença entre energia eletromagnética e cobre no integrador atual; energia CC após retificação deve continuar separada.
4. O resíduo do regime A decorre da discretização e do avanço explícito de posição/velocidade.
5. Não há validação experimental, caracterização de gerador, inércia rotacional detalhada ou frenagem terminal modelada.

Não foram alterados E1–E5, dashboard, catálogo, parâmetros históricos ou resultados consolidados. Nenhum commit, merge ou push foi executado.

