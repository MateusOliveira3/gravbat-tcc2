# Comparação paramétrica vertical × inclinada

**Classificação:** CALCULADO e SIMULADO sob hipóteses documentadas.  
**Cenário comum:** `m=6 kg`, `H=1 m`, `g=9,81 m/s²`, `c_r=0,02`, `θ={10°,20°,30°,40°}`. A coluna de 90° é somente referência geométrica e energética ideal.

## Método

A análise reutiliza `model.geometry`, `model.mechanics`, `simulation.simulator`, `model.coupling` e `simulation.electromechanical_dynamic`. Os resultados completos estão em `matriz_resultados_comparativos.csv`.

E1/E2 foram conferidos por cálculo independente:

- `E_g = m g H = 58,86 J` para todos os ângulos;
- `L = H/sen(θ)`;
- `F_g = m g sen(θ)`;
- `F_rol = c_r m g cos(θ)`;
- `E_rol = F_rol L`.

O caso de 90° possui `L=0` apenas para marcar o limite ideal. Não foram executados E3 ou E4 a 90°.

## Resultados analíticos E1/E2

| θ | L (m) | E_g (J) | F_g (N) | F_rol (N) | F_liq (N) | E_rol (J) |
|---:|---:|---:|---:|---:|---:|---:|
| 10° | 5,7588 | 58,86 | 10,2209 | 1,1593 | 9,0616 | 6,6762 |
| 20° | 2,9238 | 58,86 | 20,1313 | 1,1062 | 19,0251 | 3,2343 |
| 30° | 2,0000 | 58,86 | 29,4300 | 1,0195 | 28,4105 | 2,0390 |
| 40° | 1,5557 | 58,86 | 37,8345 | 0,9018 | 36,9327 | 1,4029 |
| 90° ideal | — | 58,86 | 58,86 | 0 | 58,86 | — |

O resultado demonstra que a energia potencial permanece constante, enquanto o percurso e o trabalho de rolamento diminuem com o aumento da inclinação.

## E3 — torque mecânico

Foram calculados dois regimes:

- `τ=0,1 N·m` absoluto;
- `τ=0,5 τ_lim(θ)` normalizado por cenário.

| θ | τ_lim (N·m) | a absoluta (m/s²) | t absoluta (s) | v final absoluta (m/s) | P eixo absoluta (W) | a normalizada (m/s²) | t normalizada (s) | P eixo normalizada (W) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10° | 0,4078 | 1,1399 | 3,1787 | 3,6234 | 3,6234 | 0,7551 | 3,9054 | 6,0128 |
| 20° | 0,8561 | 2,8005 | 1,4450 | 4,0467 | 4,0467 | 1,5854 | 1,9205 | 13,0338 |
| 30° | 1,2785 | 4,3647 | 0,9573 | 4,1784 | 4,1784 | 2,3675 | 1,2998 | 19,6716 |
| 40° | 1,6620 | 5,7851 | 0,7334 | 4,2426 | 4,2426 | 3,0777 | 1,0055 | 25,7152 |

O torque normalizado não representa a mesma carga absoluta entre ângulos. Por isso, seus resultados não devem ser comparados como potência de um mesmo equipamento.

## E4 — conversão eletromecânica

Parâmetros mantidos: `r_d=0,05 m`, `G=1`, `η_t=0,90`, `K_e=0,1 V·s/rad`, `R_fase=2 Ω`, duas fases, `η_retificador=0,90`, `R_carga=8 Ω`, passo `0,001 s`.

| θ | status | duração (s) | v final (m/s) | energia AC (J) | energia CC estimada (J) | perda cobre (J) | energia cinética final (J) | AC/E_g |
|---:|:---|---:|---:|---:|---:|---:|---:|---:|
| 10° | DESCE | 2,8590 | 3,8914 | 4,8658 | 4,3792 | 1,2165 | 45,4293 | 8,27% |
| 20° | DESCE | 1,3810 | 4,1626 | 2,6181 | 2,3563 | 0,6545 | 51,9807 | 4,45% |
| 30° | DESCE | 0,9300 | 4,2555 | 1,8275 | 1,6448 | 0,4569 | 54,3285 | 3,10% |
| 40° | DESCE | 0,7170 | 4,2985 | 1,4319 | 1,2887 | 0,3580 | 55,4302 | 2,43% |

A energia AC foi integrada a partir de `potencia_ac_W`; a energia CC é a mesma parcela multiplicada por `η_retificador`. A energia eletromagnética e a perda de cobre foram mantidas separadas. Esses resultados são do equivalente eletromecânico e não constituem medição.

## Interpretação crítica

- **Inclinação × energia mecânica:** para `m` e `H` fixos, `E_g` não muda. A rampa mais rasa aumenta o percurso e o trabalho de rolamento.
- **Inclinação × potência e duração:** ângulos maiores aumentam a força líquida e reduzem a duração nos cenários calculados. Isso depende da condição inicial, do torque e do critério de comparação.
- **Inclinação × energia elétrica:** no E4 específico, a energia AC absoluta diminui com o ângulo porque a descarga mais rápida deixa menos tempo sob o torque eletromecânico equivalente. Isso é uma tendência condicionada a `K_e`, resistências, carga, raio e transmissão; não é uma lei universal.
- **Vertical:** a coluna de 90° informa apenas `mgH` e o limite geométrico. Não representa uma suspensão vertical com cabo, motor, perdas ou segurança próprios.

## Verificação independente e estados

As grandezas E1/E2 foram recalculadas por expressões analíticas independentes. Os resíduos de balanço do E3 ficaram na ordem de arredondamento numérico. No E4, todos os quatro cenários inclinados concluíram a descida; não houve caso bloqueado nesta configuração. A classificação `DESCE` não implica validação física do gerador.

## Limitações

- O torque E3 é aplicado como carga refletida ao tambor por `G τ/(η_t r_d)`.
- E3 e E4 não são a mesma trajetória: torque constante versus torque dependente da velocidade.
- Não há modelo vertical físico completo.
- `c_r`, parâmetros elétricos, rendimento e retificação são hipóteses.
- Não há análise estrutural, econômica, de controle ativo ou validação experimental.

## Arquivos gráficos

- `figuras_consolidadas/figura_comparacao_geometria.svg`
- `figuras_consolidadas/figura_comparacao_forcas.svg`
- `figuras_consolidadas/figura_comparacao_e4.svg`

As figuras são reconstruções quantitativas a partir da matriz CSV e identificadas como calculadas/simuladas.

## Revisão da referência de 90°

A referência ideal foi corrigida para `L=H/sen(90°)=1 m`, `F_g=58,86 N`, `F_rol=0 N`, `F_liq=58,86 N` e `E_rol=0 J`. Esses valores são apenas o limite matemático do modelo de rampa. Não há E3 ou E4 para 90° e a referência não representa uma suspensão vertical real.

## Revisão energética do E4

A matriz agora inclui duração, velocidade final, energia potencial inicial, energia AC, energia CC estimada, potência média AC, energia cinética final, frações `E_AC/E_g` e `E_k/E_g`, além da perda de cobre. A energia CC é uma transformação da energia AC e não deve ser somada a ela.

A energia AC integrada diminui de 4,8658 J a 10° para 1,4319 J a 40°, enquanto a potência média AC cresce porque a duração cai mais rapidamente. `E_AC/E_g` é uma fração energética do cenário simulado, não eficiência de ciclo completo.

A implementação atual do E4 disponibiliza explicitamente energia eletromagnética acumulada, energia AC integrada e perda de cobre. A perda de transmissão não é uma saída independente do integrador E4; portanto não foi inventada nem somada ao balanço comparativo. O resíduo deve ser interpretado com o passo de 0,001 s e com a discretização documentada no relatório E4.

A chegada ao final ocorre com energia cinética remanescente. Ela não representa energia elétrica recuperável em uma etapa posterior: isso exigiria um modelo adicional de desaceleração ou frenagem regenerativa.
