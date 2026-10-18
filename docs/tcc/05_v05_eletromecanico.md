# V0.5 — núcleo eletromecânico mínimo

## Escopo

Esta primeira implementação transforma a velocidade angular de saída em FEM de fases e torque resistente por balanço de potência. Ela é parametrizada: `K_e`, resistência, número de fases e eficiência do retificador precisam ser fornecidos pelo usuário, por datasheet, medição ou hipótese identificada.

## Hipótese explicitamente adotada

Foi usada uma FEM senoidal por fase, deslocada entre fases. Essa forma de onda é uma hipótese de ordem reduzida para a V0.5, não uma afirmação sobre o motor físico. A forma real deverá ser substituída por medição ou dado de fabricante quando o componente for identificado.

## Equações

`e_k = K_e ω sin(θ_e + 2πk/N_f)`

`v_k = e_k - R_k i_k`

`τ_em = e_k i_k / ω`, para `ω ≠ 0`; no repouso o módulo retorna torque eletromagnético nulo porque o balanço de potência não define torque estático.

`P_CC = η_r P_AC`

As grandezas estão em V, A, Ω, rad/s, N·m e W. O módulo não integra ainda o torque ao simulador mecânico, não escolhe carga elétrica e não modela retificador detalhado.

## Verificação

Os testes verificam proporcionalidade da FEM à velocidade, deslocamento entre fases, queda resistiva, torque por potência, separação da eficiência do retificador e rejeição de parâmetros inválidos. Os resultados são calculados; não são experimentais.

## Limitações e próxima etapa

O módulo ainda não identifica o motor, não usa `K_t`, não representa indutância, perdas magnéticas, comutação, ponte retificadora ou barramento dinâmico. A próxima etapa deverá conectar uma carga elétrica prescrita ao estado da V0.4 e refletir o torque eletromagnético na dinâmica, mantendo cada parâmetro rastreável.

## Catálogo inicial

Foi criado um catálogo de software com um único registro: `Modelo hipotético V0.5`. Ele possui valores exclusivamente para testar a interface e o pipeline e está marcado como **HIPÓTESE**. Não representa o motor físico disponível e não deve ser citado como dado experimental ou de fabricante. Motores reais somente serão adicionados com fabricante, código e fonte verificável.

Foi localizado e cadastrado como candidato real de referência o FAULHABER DM52100S. O datasheet fornece resistência, indutância, corrente, torque e amplitude de FEM em uma unidade relacionada ao passo. Usando 100 passos por revolução e 2,2 V por 1000 passos/s, foi derivado `K_e = 2,2/(20π) = 0,0350 V·s/rad`. O valor está marcado como **DATASHEET-DERIVADO** e deve ser confirmado por medição; o cadastro não significa que esse seja o motor do protótipo.

## Prévia de carga resistiva

Foi acrescentada uma estimativa de bancada com resistência de carga equivalente. A corrente é calculada a partir da FEM de pico e da soma da resistência de fase com a resistência de carga. A potência AC usa a média de uma senoide e é multiplicada pelo número de fases; a potência CC aplica a eficiência do retificador cadastrada. O torque é estimado por `τ = P_AC/|ω|`. Essa aproximação é apenas **CALCULADA/HIPÓTESE**: não representa ainda a ponte retificadora, a ligação elétrica real ou o torque integrado à trajetória.

## Primeiro acoplamento mecânico

O torque estimado no ponto de operação de referência agora é aplicado à função de acoplamento V0.4. Isso produz uma trajetória comparativa com torque eletromecânico constante equivalente. A aproximação é **QUASE ESTACIONÁRIA** e serve para verificar o sentido do acoplamento e a redução da aceleração. Não é ainda o modelo dinâmico final, pois a corrente, a FEM e o torque real variam com velocidade e posição elétrica.

O balanço inicial de ciclo foi implementado separadamente em `simulation/cycle.py`. A subida usa potência externa e eficiência prescritas; portanto, energia de recarga, tempo e saldo são **CALCULADOS** sob **HIPÓTESES**, não medições.

## Integração numérica com torque variável

Foi acrescentado um integrador explícito em `simulation/electromechanical_dynamic.py`. A cada passo, a velocidade define a FEM, a corrente e o torque resistente; esse torque altera a aceleração e a posição seguintes. O passo temporal é configurável. A verificação de carga desprezível compara a trajetória numérica com a solução analítica da V0.4, dentro de tolerância explícita.

O integrador ainda usa a aproximação de carga resistiva equivalente e não representa a ponte retificadora real. Portanto, seus resultados são **SIMULADOS** sob parâmetros de **HIPÓTESE**, **DATASHEET** ou **MEDIDO**, conforme o cadastro selecionado.

A auditoria do TCC-1 mostrou que o balanço final ainda precisa separar explicitamente gerador, retificador, conversor e carga. A eficiência global não deve ser usada para ocultar essas transformações.
