# GRAVBAT-L1 — Especificação geométrica e cinemática preliminar

**TCC II · Engenharia de Energia · UFSC**  
**Status:** proposta conceitual para modelagem e representação computacional. Não constitui projeto executivo, dimensionamento estrutural ou seleção definitiva de componentes.

## 1. Objetivo

Definir uma arquitetura mecânica de referência para o protótipo de laboratório GravBat-L1, preservando a distinção entre grandezas calculadas pelo núcleo, parâmetros hipotéticos de representação e componentes ainda não dimensionados.

## 2. Configuração de referência

| Parâmetro | Valor inicial | Classificação |
|---|---:|---|
| Massa móvel total | 6 kg | hipótese de cenário |
| Comprimento geométrico de referência | 1,20 m | entrada do modo Laboratório |
| Inclinação | 10° | entrada do cenário |
| Coeficiente de resistência equivalente | 0,02 | hipótese mecânica |
| Diâmetro nominal do tambor | 0,10 m | hipótese de representação |
| Raio efetivo inicial | 0,05 m | entrada de transmissão |
| Multiplicação de rotação | 5:1 | hipótese investigativa |
| Velocidade-alvo | 0,02 m/s | hipótese cinemática |

## 3. Coordenadas e percurso

A coordenada longitudinal `s` tem origem na posição superior inicial do carro e cresce no sentido da descida: `s=0` no topo e `s=L` no final geométrico do percurso modelado.

O núcleo atual usa `Geometria.L_m` como comprimento do experimento ou cenário idealizado. A representação do equipamento deve distinguir esse comprimento do percurso útil:

\[
L_{\mathrm{útil}}=L_{\mathrm{trilho}}-d_{\mathrm{sup}}-d_{\mathrm{inf}}
\]

\[
H_{\mathrm{útil}}=L_{\mathrm{útil}}\sin(\theta)
\]

Essa distinção será apenas representacional nesta etapa. Os resultados E1–E5 não serão substituídos silenciosamente por `L_útil`.

## 4. Estrutura e carro

A vista principal deve mostrar dois perfis longitudinais paralelos, base rígida, apoios, carro estrutural, rodas ou rolamentos, massa identificada, ponto de ancoragem do cabo, batentes e afastamento de segurança do conjunto de transmissão. As dimensões do carro, rodas, apoios e batentes são esquemáticas até existir dimensionamento estrutural.

## 5. Cabo e tambor

O cabo deve permanecer ligado ao ponto de ancoragem do carro e tangente ao tambor durante toda a trajetória. As hipóteses iniciais são cabo inextensível, ausência de escorregamento, raio efetivo constante, enrolamento em camada única e alinhamento adequado.

Com raio efetivo `r`:

\[
\omega_t=v_{\mathrm{trilho}}/r,\qquad \Delta\varphi_t=s/r
\]

O módulo `model.cable.GeometriaCabo` representa tipo, diâmetro do cabo, diâmetro do núcleo e comprimento disponível, mas ainda não modela ancoragem, tangência, raio variável por camadas ou resistência do cabo.

## 6. Transmissão mecânica

Uma engrenagem maior solidária ao eixo do tambor aciona uma engrenagem menor no eixo de saída:

\[
\omega_{\mathrm{saída}}=G\omega_t,\qquad G=5
\]

A transmissão aumenta a rotação e reduz o torque disponível, além de introduzir perdas. O módulo `model.transmission.cinematica` já calcula rotação do tambor e do eixo de saída a partir da velocidade linear, raio e relação `G`. O padrão atual do dashboard é `G=1,0`; `G=5` permanece hipótese investigativa até ser explicitamente selecionado.

## 7. Torque, máquina elétrica e segurança

O limite simplificado de torque no tambor não representa torque efetivamente transmitido ao gerador durante toda a descida livre. A velocidade de `0,02 m/s` continua sendo hipótese cinemática. A máquina elétrica, PWM, encoder e frenagem eletromagnética não são considerados implementados.

A arquitetura deve indicar batentes, sensores de fim de curso como possibilidade futura, frenagem mecânica independente e afastamento entre carro e transmissão.

## 8. Representação gráfica planejada

A vista lateral principal, em escala uniforme, deve mostrar trilhos, carro, cabo, tambor, cotas `L`, `H` e `θ` e limites de deslocamento. Um detalhe ampliado, identificado como **vista esquemática, fora de escala**, deve mostrar tambor, eixo, engrenagem maior, engrenagem menor, eixo de saída, gerador e indicação `G=5:1`.

A posição do carro, o cabo desenrolado e a rotação esquemática devem compartilhar o mesmo instante de animação.

## 9. Correspondência com o código atual

| Especificação | Código atual | Situação |
|---|---|---|
| `θ` em graus | `Geometria.theta_graus` | compatível |
| `L` no Laboratório | `geometria(..., modo="laboratorio", L_m=...)` | compatível |
| `H` no Terreno | `geometria(..., modo="terreno", H_m=...)` | compatível |
| `H=L sen(θ)` e `L=H/sen(θ)` | `model.geometry.geometria` | implementado |
| `s` da trajetória | `Estado.posicao_m` | 0 até `L` |
| velocidade no trilho | `Estado.velocidade_m_s` | compatível |
| cabo e núcleo | `GeometriaCabo` | parcial |
| raio efetivo | `app.py` / `cinematica` | entrada separada |
| relação de transmissão | `model.transmission.cinematica` | implementada; padrão `G=1` |
| percurso útil | não existe no núcleo | pendente |
| engrenagens físicas | não modeladas geometricamente | pendente |
| gerador e suportes | modelos separados | representação futura |
| batentes e segurança | não modelados como componentes físicos | representação futura |

## 10. Critérios para a próxima implementação

Verificar inclinações de 10°, 30° e 40°; comprimento fixo e desnível fixo; posições inicial, intermediária e final; continuidade do cabo; rotação compatível do tambor; sentido e razão das engrenagens; ausência de colisões; coerência entre percurso, tempo, velocidade e animação; sincronização com o gráfico; preservação dos resultados E1–E5.

## 11. Limitações

O GravBat-L1 permanece um modelo computacional em desenvolvimento. Ainda não há validação experimental, dimensionamento estrutural completo, seleção definitiva de gerador, caracterização da transmissão, modelagem de camadas de cabo, inércia detalhada, controle ativo ou sistema de segurança dimensionado.

Esta especificação documenta a arquitetura de referência e suas convenções. Não autoriza alterar modelos físicos ou experimentos E1–E5.
