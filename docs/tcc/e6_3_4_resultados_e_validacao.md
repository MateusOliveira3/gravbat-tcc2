# E6.3/E6.4 — Resultados e validação

**Data:** 23/10/2026  
**Branch:** `fix/coerencia-fisica-dashboard`  
**Escopo:** correção isolada do E6.2, auditoria bibliográfica local e primeira sensibilidade do regime eletromecânico. E1–E5 não foram modificados.

## Arquivos

- `docs/tcc/gravbat_e63_e64_plano_codex.md`: cópia versionada do plano recebido.
- `docs/tcc/referencias_canonicas.md`: numeração [1]–[18], DOI, URLs, papel e status.
- `model/e6_controlled.py`: trajetória dinâmica de torque prescrito e chamada parametrizada do E4 passivo.
- `tests/test_e6_controlled.py`: partida/chegada, saturação e referência passiva.
- `outputs/e6/e6_sensibilidade_theta_G_R.csv`: sensibilidade inicial para 10°, 20°, 30° e 40°, `G` de 1 a 20 e seis cargas.
- `outputs/e6/e6_convergencia_e4.csv`: `dt=0,001`, `0,0005` e `0,0001 s`.
- Figuras SVG diagnósticas anteriores em `outputs/e6/` permanecem rastreáveis.

## Correções E6.3

O regime B agora possui estado dinâmico `x(t), v(t)`, parte do repouso e integra até a chegada. Para uma duração-alvo, a aceleração é `a=2L/T²` e o torque requerido é calculado a partir da força líquida. A energia cinética final é incluída no balanço; não existe mais estado com velocidade final não nula e energia cinética zero.

Estados distintos são usados para chegada, alvo inviável por ser mais rápido que a descida livre e bloqueio por saturação de torque. Um torque máximo insuficiente não é rotulado como bloqueio automaticamente: ele deve ser tratado como aceleração/descida em uma execução dinâmica; o bloqueio ocorre somente quando a saturação solicitada impede a condição especificada.

Para 10°, 60 s, o integrador dinâmico forneceu:

- `L=5,75877 m`, `v_final=0,0959795 m/s`;
- `tau_req=0,406909 N m`;
- `E_rol=6,67623 J`;
- `E_transmissao=5,20732 J`;
- `E_freio_eixo=46,86590 J`;
- `E_cinetica_final=0,02764 J`;
- resíduo `≈ -4,9×10^-14 J`.

Esse regime é um freio prescrito e dissipa a energia no eixo; sua energia elétrica é zero por construção. Ele não demonstra recuperação elétrica prolongada.

## Regime C e hipótese de transmissão

O regime C continua usando a relação eletromecânica do E4: FEM dependente de `omega`, corrente limitada por resistências e torque derivado de potência eletromagnética. A função foi parametrizada para `G`, `r_d`, `K_e`, resistência de fase e carga, sem torque ideal independente da corrente.

A estimativa estacionária do plano (`G≈10,3`, `P_AC≈0,626 W`) **não foi promovida a resultado**. Ela exige verificar convenções de constante de torque, número de fases, partida e chegada. A execução dinâmica passiva atual continua apresentando descargas de poucos segundos; portanto, a meta de 0,5 W AC por 60 s ainda não foi demonstrada.

## Convergência do integrador histórico E4

Para 10°, carga de 8 ohm e `G=1`:

| dt (s) | tempo (s) | E carga AC (J) | E cobre (J) | E cinética final (J) | resíduo (J) |
|---:|---:|---:|---:|---:|---:|
| 0,001 | 2,8590 | 4,86581 | 1,21645 | 45,42929 | 0,67222 |
| 0,0005 | 2,8590 | 4,86564 | 1,21641 | 45,42777 | 0,67394 |
| 0,0001 | 2,8590 | 4,86551 | 1,21638 | 45,42657 | 0,67531 |

O resíduo não converge monotonicamente para zero nesta implementação porque o evento de chegada e o avanço explícito de posição/velocidade introduzem uma parcela de discretização. O integrador histórico não foi alterado nem ajustado para fechar artificialmente o balanço.

## Sensibilidade inicial

Foi gerado CSV para `theta=10°,20°,30°,40°`, `G={1,3,5,8,10,12,15,20}` e `R_carga={1,2,4,8,16,100} ohm`, com status, duração, energia AC, potência média, velocidade final, cobre, energia cinética e resíduo. Combinações que excederam o limite de passos são registradas como `INTEGRACAO_EXCEDEU_MAX_PASSOS`, sem interpolação ou substituição por zero.

A varredura completa de 5°–60° e os mapas de calor/Pareto não foram publicados nesta rodada porque alguns cenários lentos excedem o limite do integrador atual e precisam primeiro de uma política aprovada de limite temporal e evento de parada. Produzir mapas antes dessa decisão misturaria resultados válidos e falhas numéricas.

## Bibliografia

`docs/tcc/referencias_canonicas.md` preserva [1]–[18]. Os DOI [6], [7], [9], [17] e [18] foram registrados conforme o plano recebido, mas a verificação externa do editor não foi executada neste ambiente. Os itens [1]–[5] e [10]–[16] permanecem sem DOI, sem invenção de identificadores. A sincronização local não equivale a sincronização automática com Google Docs.

## Verificação

- Testes específicos E6: 3 aprovados.
- Compilação do módulo E6: aprovada.
- `git diff --check`: aprovado.
- Suíte completa atual: 91 testes, 90 aprovados e 1 erro ambiental conhecido de limpeza de `TemporaryDirectory` no Windows.
- E1–E5 históricos: não modificados.

## Decisões científicas pendentes

1. Limite de torque, corrente, velocidade e temperatura para o gerador equivalente.
2. Convenção definitiva de `K_e`, torque por fase e fator de fases.
3. Política para cenários que excedem `max_passos`.
4. Tratamento de frenagem terminal e energia recuperável versus dissipada.
5. Aprovação para varredura completa 5°–60°, mapas de calor e análise Pareto após estabilizar o integrador.
6. Verificação externa dos metadados bibliográficos [6], [7], [9], [17] e [18].

Nenhum commit, push, merge ou deploy foi executado.
