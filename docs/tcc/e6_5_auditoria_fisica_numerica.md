# E6.5 — Auditoria física, numérica e bibliográfica

**Data:** 23/10/2026  
**Branch:** `fix/coerencia-fisica-dashboard`  
**Escopo:** auditoria independente e correções isoladas do E6. Não houve alteração em E1–E5.

## Fontes recebidas

Foram lidos integralmente:

- `gravbat_e6_auditoria_analitica.md`;
- `gravbat_e6_referencia_analitica.csv`;
- `gravbat_referencias_canonicas_completas.md`.

O catálogo completo foi incorporado em `docs/tcc/referencias_canonicas.md`, preservando [1]–[18]. A incorporação é local; não altera o Google Docs e não constitui verificação externa automática.

## 1. Perda de transmissão e resíduo E4

O código histórico calcula `F_carga = G tau/(eta_t r_d)`, portanto a eficiência de transmissão já atua na força refletida. Entretanto, o balanço usado na auditoria anterior somava apenas rolamento, energia AC, cobre e energia cinética. Faltava explicitar a perda de transmissão:

`E_trans = (E_AC + E_cobre) (1/eta_t - 1)`.

Para 10°, `dt=0,001 s`, o resíduo bruto é `0,67222 J`; a transmissão estimada é `0,67581 J`; o resíduo corrigido fica `-0,00359 J`. Para `dt=0,0005` e `0,0001 s`, os resíduos corrigidos são `-0,00184` e `-0,00046 J`. A solução analítica independente fecha o balanço até arredondamento (`~10^-14 J`).

A interpretação é consistente: o resíduo bruto não representa energia desaparecida; é a fronteira de transmissão omitida, somada à discretização do evento de chegada.

## 2. Diferença do regime B

A diferença publicada de `0,08291 J` não é uma nova perda física. Ela resulta de fronteiras incompatíveis entre a referência estacionária e o estado final: o cálculo usava `v=L/T` para descrever a velocidade, mas zerava ou omitía a energia cinética final e aplicava a eficiência em uma parcela diferente do fluxo. A versão dinâmica corrigida calcula o evento de chegada e inclui `E_k = m v_final²/2`.

Para 10° e 60 s, a execução independente fornece `v_final=0,191959 m/s`, `E_k=0,11054 J`, `E_rol=6,67623 J`, `E_trans=5,20732 J` e `E_freio_eixo=46,86590 J`, fechando `E_g=58,86 J` com resíduo inferior a `10^-13 J`. A referência estritamente estacionária deve ser tratada como limite cinemático, não como trajetória de partida do repouso.

## 3. Convenção elétrica e amortecimento

`model/electromechanics.py` calcula FEM de pico, corrente por `R_fase + R_carga`, potência de carga e cobre por fase, e multiplica as potências médias por `fases`. O torque usado no integrador é `P_em/|omega|`, já totalizado. Com `omega=G v/r_d`, a linearização produz:

`b(G) = (fases/2) K_e² G² / [eta_t r_d² (R_fase+R_carga)]`.

Para duas fases e os parâmetros do E4, `b(1)=0,444444 N s/m`, coincidindo com o valor auditado. Isso confirma a convenção efetiva do código; não foi feito ajuste para coincidir com a hipótese analítica. A equivalência não valida um gerador físico nem resolve fatores de retificação, indutância ou limites térmicos.

## 4. Comparação E4 versus solução analítica

Arquivo completo: `outputs/e6/e6_comparacao_analitico_e4.csv`.

| θ | erro relativo de tempo | erro absoluto de velocidade (m/s) | erro absoluto de E_AC (J) |
|---:|---:|---:|---:|
| 10° | 1,05×10⁻⁶ | 1,33×10⁻⁴ | 3,48×10⁻⁴ |
| 20° | −1,15×10⁻⁴ | −3,10×10⁻⁴ | −6,96×10⁻⁴ |
| 30° | 3,71×10⁻⁴ | 1,67×10⁻³ | 2,13×10⁻³ |
| 40° | −3,71×10⁻⁴ | −1,40×10⁻³ | −1,47×10⁻³ |

A concordância é compatível com a discretização do integrador histórico. A solução analítica é usada como referência independente, sem substituir o E4.

## 5. Implementação numérica independente

Foi criado `model/e6_analytic.py`, com solução fechada para `m dv/dt = F0 − b v`, raiz monotônica para o evento `x(T)=L`, estados finitos e balanço analítico. Os testes verificam `G=1` e `G=14,567`, incluindo a referência de 60 s.

O integrador dinâmico E6 continua separado em `model/e6_controlled.py`. Ele registra chegada, saturação, alvo inviável, velocidade residual e resíduos. Cenários que excedem o horizonte do integrador histórico não são convertidos em sucesso.

## 6. Hipótese G≈14,57

Para 10°, `G=14,5671456`, a solução analítica fornece aproximadamente:

- `T=60 s`;
- `v_final=0,09608 m/s`;
- `E_AC=37,5524 J`;
- `P_AC média=0,62587 W`;
- `E_k=0,02769 J`.

Esses valores são benchmark analítico do equivalente linear, não simulação validada de uma máquina. A dinâmica histórica deve ser verificada com o mesmo tratamento de partida, chegada e limites antes de declarar viabilidade.

## 7. Frenagem terminal e varreduras

A separação entre energia recuperada e frenagem dissipativa está implementada no regime B: o freio prescrito aparece como `E_freio_eixo`, enquanto `E_carga_J=0`. A frenagem regenerativa eletromagnética com limite de corrente ainda não foi implementada, portanto não foi inventada uma recuperação terminal.

Foi gerado `outputs/e6/e6_sensibilidade_theta_G_R.csv` para a malha inicial de ângulos, transmissão e carga, com status de integração. O gargalo numérico permanece em cenários lentos do integrador histórico. Por isso, mapas de calor completos e Pareto não foram publicados como resultados científicos nesta etapa; somente cenários válidos devem ser visualizados após definir o horizonte e o evento de parada.

## 8. Rolamento e bibliografia

A sensibilidade `c_r=0,006`, `0,020` e `0,050` permanece uma análise paramétrica a executar com os mesmos critérios de validade; os valores devem ser rotulados como cenários inspirados na literatura, não como propriedades medidas. O catálogo [1]–[18] agora está completo localmente, sem DOI inventado para livros e relatórios.

## Verificação

- Testes E6 específicos: 5 aprovados.
- Compilação: aprovada.
- `git diff --check`: aprovado.
- Suíte completa histórica: 93 testes após os novos testes, com 92 aprovados e 1 erro ambiental de limpeza Windows; nenhuma falha científica identificada.
- E1–E5: preservados.

Nenhum commit, push, merge ou alteração no Google Docs foi executado.
