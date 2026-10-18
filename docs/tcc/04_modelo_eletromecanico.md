# Fase 5A — definição e fundamentação do modelo eletromecânico

## Escopo e objetivo científico

Esta fase responde à pergunta: **qual modelo de máquina elétrica é justificável para representar o acoplamento entre a saída mecânica do GravBat e uma carga elétrica, sem inventar parâmetros do componente físico?** A Fase 5A é documental e investigativa. Nenhum gerador foi implementado no simulador e a V0.4 permanece encerrada.

No TCC-1, a arquitetura é descrita apenas em nível conceitual: uma máquina de baixa rotação, com uso proposto de motor de passo, seguida de retificação, barramento CC e eletrônica de potência. O texto também prevê medição de tensão e corrente no gerador e no barramento. Não há identificação do motor real, curva de FEM, constante `K_e`, constante `K_t`, resistência ou indutância dos enrolamentos.

## Princípio físico e separação de subsistemas

O **GERADOR** converte velocidade angular mecânica em tensões induzidas nas fases AC. O **RETIFICADOR** converte essas fases em uma grandeza CC pulsante ou filtrada. A **ELETRÔNICA** contém barramento, conversor, carga e controle. A perda e o torque de cada bloco devem ser contabilizados separadamente.

Para uma máquina de `N_f` fases, uma formulação candidata por fase é:

`v_k = R_k i_k + L_k di_k/dt + e_k(θ_e, ω)`

`e_k(θ_e, ω) = K_{e,k} ω f_k(θ_e)`

onde `v_k` é tensão de fase [V], `i_k` corrente [A], `R_k` resistência [Ω], `L_k` indutância [H], `ω` velocidade mecânica [rad/s], `θ_e` ângulo elétrico [rad], `K_e` constante de FEM [V·s/rad] e `f_k` forma de onda adimensional obtida de medição, datasheet ou hipótese explicitamente declarada. Para um rotor com `p` pares de polos, `θ_e = p θ_m` e `ω_e = p ω`; em um motor de passo híbrido a relação exata deve ser confirmada pela geometria e pelo número de dentes/polos.

O torque eletromagnético pode ser calculado por balanço de potência quando `ω ≠ 0`:

`τ_em ω = Σ_k e_k i_k`  e  `τ_em = Σ_k e_k i_k / ω`.

Em uma descrição equivalente, pode-se usar `τ_em = K_t i_eq`, mas `K_t` só deve ser usado depois de definida a convenção de corrente e de validada a equivalência com a máquina real. Em unidades SI, a relação numérica entre `K_e` e `K_t` pode coincidir sob convenções compatíveis; isso não autoriza igualar constantes obtidas de ensaios com definições diferentes.

O retificador deverá ser modelado depois da identificação das fases. Para uma ponte ideal, `P_CC = V_CC I_CC` e `P_CC = η_r P_AC`, com `η_r` explicitamente separado de perdas em cobre `Σ R_k i_k²`, perdas magnéticas e perdas eletrônicas. A topologia (ponte por fase, ponte trifásica, retificação de onda completa ou outra) ainda está **A DEFINIR**.

## Modelos candidatos e decisão

O modelo de gerador CC simplificado (`E = K_e ω`, `τ = K_t I`, resistência série) é útil como ensaio de sensibilidade, mas não representa diretamente a natureza multifásica de um motor de passo. Um motor de passo possui fases discretas e FEM dependente da posição elétrica; fontes técnicas de fabricante descrevem sequência de excitação, número de fases e a relevância da FEM em rotação contínua (Oriental Motor, Technical Manual, 2024, https://www.orientalmotor.eu/system/files/document/tech/technicalmanual_stepping_10e.pdf).

O modelo recomendado para a primeira V0.5 é um **modelo equivalente por fase, permanente-magnético, de ordem reduzida e identificável**:

1. usar `ω_saida` já calculada pela V0.4;
2. obter `e_k(ω, θ)` de ensaio de circuito aberto ou de datasheet do motor identificado;
3. iniciar com `R_k` e, se a escala temporal justificar, `L_k`; não assumir forma senoidal sem evidência;
4. conectar uma retificação ideal parametrizada somente após definir a ligação das fases;
5. calcular a corrente da carga e `τ_em` por potência elétrica ou por `K_t` validado;
6. refletir `τ_em` pela transmissão e reintegrar a dinâmica mecânica.

Esse nível é suficiente para testar o acoplamento eletromecânico. Um modelo d-q completo, saturação, cogging, perdas no ferro, comutação detalhada e controle PWM ficam para etapas posteriores, caso os dados do componente e a pergunta científica exijam isso.

## Parâmetros necessários e status

| Parâmetro | Símbolo | Unidade | Origem esperada | Status |
|---|---:|---:|---|---|
| velocidade de saída | `ω_saida` | rad/s | V0.4 calculada | CALCULADO |
| relação de transmissão | `G` | — | geometria/hipótese do projeto | HIPÓTESE/entrada |
| raio do tambor | `r_d` | m | geometria/medição | HIPÓTESE/entrada |
| número de fases | `N_f` | — | etiqueta/datasheet/inspeção | A DEFINIR |
| conexão das fases | — | — | inspeção/datasheet | A DEFINIR |
| constante de FEM | `K_e` ou `K_{e,k}` | V·s/rad | ensaio de circuito aberto ou datasheet | A DEFINIR |
| constante de torque | `K_t` | N·m/A | ensaio/datasheet, com convenção registrada | A DEFINIR |
| resistência de fase | `R_k` | Ω | medição ou datasheet | A DEFINIR |
| indutância de fase | `L_k` | H | medição ou datasheet | A DEFINIR |
| forma de onda da FEM | `f_k(θ)` | — | osciloscópio/ensaio ou datasheet | A DEFINIR |
| passos por volta/polos efetivos | `N_s`, `p` | passos/rev, — | etiqueta/datasheet/geometria | A DEFINIR |
| corrente de fase/saída | `i_k`, `I_CC` | A | medição/modelo de carga | A DEFINIR |
| tensão de fase/barramento | `v_k`, `V_CC` | V | medição/modelo de carga | A DEFINIR |
| inércia do rotor | `J_r` | kg·m² | datasheet/ensaio | A DEFINIR |
| eficiência/topologia do retificador | `η_r` | — | circuito real ou hipótese explícita | A DEFINIR |
| carga/barramento/conversor | — | — | especificação do experimento | A DEFINIR |

Nenhum desses campos deve receber valor numérico arbitrário. `G`, `r_d` e demais entradas mecânicas continuam sendo as hipóteses configuráveis documentadas nas fases anteriores; elas não identificam o motor.

## Auditoria do componente físico

O TCC-1 não informa fabricante, part number, número de fios, número de fases, passo angular ou datasheet do motor disponível. Portanto, **Componente real ainda não identificado**. Antes da V0.5 são necessários: fotografias legíveis da etiqueta e dos conectores, fabricante/part number, número e cores dos fios, resistência entre enrolamentos, indutância se disponível, passo angular ou passos por volta, corrente/tensão nominais, torque nominal/holding torque, massa e dimensões do rotor, além do esquema do retificador pretendido.

Datasheets de motores comerciais mostram por que a identificação é indispensável: resistência e indutância de fase variam entre modelos e são parâmetros publicados individualmente (por exemplo, Arcus T3 NEMA 23, https://arcus-technology.com/products/stepper-motors/t3-ultra-performance-stepper-motor-nema-23/). Esse exemplo não é o motor do GravBat e não deve ser usado como substituto.

## Hipóteses, limitações e classificação

**TEÓRICO/ANALÍTICO:** equações de circuito, potência e torque. **CALCULADO:** `ω_saida` e grandezas derivadas da V0.4. **SIMULADO:** qualquer trajetória futura com parâmetros elétricos. **EXPERIMENTAL:** somente medições futuras de FEM, corrente, tensão ou torque. **HIPÓTESE:** forma de onda, eficiência e carga quando explicitamente escolhidas. **LITERATURA/DATASHEET:** valores publicados e rastreáveis.

As limitações atuais são a ausência de identificação do motor, ausência de curva de FEM, desconhecimento da retificação e da carga, e impossibilidade de validar `K_e`, `K_t`, perdas e aquecimento. O modelo não permite afirmar potência elétrica real, eficiência ou capacidade de eliminar curtailment. Ele poderá apenas investigar o acoplamento sob parâmetros medidos, de datasheet ou cenários hipotéticos identificados.

## Proposta mínima para a V0.5 (ainda não implementada)

`ω_saida → e_k(θ,ω) → circuito das fases → retificador → V_CC,I_CC → P_el → τ_em → τ_refletido → dinâmica da massa`.

O primeiro incremento deve usar uma carga elétrica prescrita e um retificador ideal parametrizado, mantendo a forma de FEM como entrada identificável. Depois de obter medições do motor, pode-se acrescentar `R_k`, `L_k`, perdas do retificador e a dinâmica do barramento. Nenhuma implementação será iniciada até a revisão desta definição.


### Perfis paramétricos V1.0 (12 V e 30 V)

Foram adicionados dois perfis de estudo para permitir análise de sensibilidade de tensão. Eles são **HIPÓTESE-PARAMÉTRICA**: os valores de `K_e` e resistência foram escolhidos como entradas de exploração e não como especificações de um motor comercial. A tensão nominal indicada no nome não determina, sozinha, a FEM gerada. Esses perfis não devem ser citados como dados experimentais ou de fabricante.

### Comparação de perfis na V1.0

A interface calcula a FEM de pico, potência AC e torque resistente para todos os perfis cadastrados no mesmo ponto de rotação e mesma carga resistiva. A tabela é **CALCULADA**; não representa ensaio comparativo nem curva completa de desempenho. O FAULHABER é a referência de **DATASHEET-DERIVADO**, enquanto os perfis de 12 V e 30 V permanecem **HIPÓTESE-PARAMÉTRICA**.

### Ponte de diodos como freio eletromagnético

Na arquitetura de bancada, a ponte de diodos retifica a tensão AC produzida pelo motor de passo. Quando conectada a uma carga ou barramento CC, permite corrente elétrica e produz torque eletromagnético resistente. Esse torque pode reduzir a velocidade sem servo motor fornecendo potência mecânica continuamente. A ponte de diodos, isoladamente, não garante velocidade constante: a força de frenagem depende da FEM, da corrente e da carga conectada. Para regular uma referência como aproximadamente 2 cm/s, a carga elétrica ou um conversor CC-CC deverá ser dimensionado ou controlado.

A caixa de engrenagens pode aumentar a velocidade angular do gerador e reduzir o torque refletido, respeitando perdas, limites mecânicos e relação de transmissão. A relação de engrenagem não altera a energia disponível e não deve ser usada para mascarar perdas.
