# E2 — Geometria e perdas por rolamento

**Classificação:** CALCULADO. **Data:** 12/10/2026. **Núcleo:** P0 congelado.

## Objetivo

Investigar como a inclinação modifica desnível, comprimento, força gravitacional disponível e perda mecânica equivalente por rolamento, sem assumir velocidade, controle ou conversão elétrica.

## Hipóteses e parâmetros

- massa: m = 6 kg;
- coeficiente de rolamento equivalente: c_r = 0,02;
- gravidade: g = 9,81 m/s²;
- Cenário A: comprimento fixo L = 1,20 m;
- Cenário B: desnível fixo H = 1,00 m;
- ângulos: 2°, 5°, 10°, 20°, 30°, 45°, 60° e 80°.

Massa e coeficiente são hipóteses coerentes com os valores de bancada já usados no TCC. Não representam medição do protótipo.

## Equações

Cenário A:
H = L sen(θ); E_g = m g H; F_g = m g sen(θ); F_rol = c_r m g cos(θ); E_rol = F_rol L.

Cenário B:
L = H/sen(θ); E_g = m g H; F_g = m g sen(θ); F_rol = c_r m g cos(θ); E_rol = c_r m g H cot(θ).

A energia de rolamento é trabalho mecânico dissipado no percurso. Não é energia elétrica útil.

## Cenário A — comprimento constante

| θ (°) | H (m) | E_g (J) | F_g (N) | F_rol (N) | E_rol (J) | F_g > F_rol? |
|---:|---:|---:|---:|---:|---:|:---:|
| 2 | 0.0419 | 2.4650 | 2.0542 | 1.1765 | 1.4118 | sim |
| 5 | 0.1046 | 6.1560 | 5.1300 | 1.1727 | 1.4073 | sim |
| 10 | 0.2084 | 12.2651 | 10.2209 | 1.1593 | 1.3912 | sim |
| 20 | 0.4104 | 24.1576 | 20.1313 | 1.1062 | 1.3274 | sim |
| 30 | 0.6000 | 35.3160 | 29.4300 | 1.0195 | 1.2234 | sim |
| 45 | 0.8485 | 49.9444 | 41.6203 | 0.8324 | 0.9989 | sim |
| 60 | 1.0392 | 61.1691 | 50.9743 | 0.5886 | 0.7063 | sim |
| 80 | 1.1818 | 69.5589 | 57.9658 | 0.2044 | 0.2453 | sim |

## Cenário B — desnível constante

| θ (°) | L (m) | E_g (J) | F_g (N) | F_rol (N) | E_rol (J) | F_g > F_rol? |
|---:|---:|---:|---:|---:|---:|:---:|
| 2 | 28.6537 | 58.8600 | 2.0542 | 1.1765 | 33.7106 | sim |
| 5 | 11.4737 | 58.8600 | 5.1300 | 1.1727 | 13.4555 | sim |
| 10 | 5.7588 | 58.8600 | 10.2209 | 1.1593 | 6.6762 | sim |
| 20 | 2.9238 | 58.8600 | 20.1313 | 1.1062 | 3.2343 | sim |
| 30 | 2.0000 | 58.8600 | 29.4300 | 1.0195 | 2.0390 | sim |
| 45 | 1.4142 | 58.8600 | 41.6203 | 0.8324 | 1.1772 | sim |
| 60 | 1.1547 | 58.8600 | 50.9743 | 0.5886 | 0.6797 | sim |
| 80 | 1.0154 | 58.8600 | 57.9658 | 0.2044 | 0.2076 | sim |

## Verificação independente da força motriz

| θ (°) | F_g (N) | F_rol (N) | F_g − F_rol (N) |
|---:|---:|---:|---:|
| 2 | 2.0542 | 1.1765 | 0.8777 |
| 5 | 5.1300 | 1.1727 | 3.9573 |
| 10 | 10.2209 | 1.1593 | 9.0616 |
| 20 | 20.1313 | 1.1062 | 19.0251 |
| 30 | 29.4300 | 1.0195 | 28.4105 |
| 45 | 41.6203 | 0.8324 | 40.7879 |
| 60 | 50.9743 | 0.5886 | 50.3857 |
| 80 | 57.9658 | 0.2044 | 57.7614 |

A condição F_g > F_rol equivale a tan(θ) > c_r. Para c_r = 0,02, o limiar é θ > arctan(0,02) = 1,146°. Assim, 2° já possui força motriz líquida positiva, enquanto ângulos abaixo desse limiar não devem ser tratados como descida espontânea.

No cenário B, θ próximo de zero faz L = H/sen(θ) crescer sem limite. Por isso 0° foi excluído; a equação evidencia a inviabilidade geométrica do limite, sem impor um limite estrutural.

## Figuras científicas previstas

1. Cenário A: H e E_g em função de θ, com L fixo. Mostra que energia varia com o desnível gerado pela inclinação.
2. Cenário B: L e E_rol em função de θ, com H fixo, em escala adequada. Mostra o crescimento geométrico e das perdas em ângulos pequenos.
3. F_g e F_rol em função de θ, com linha de força líquida nula. Mostra o limiar de partida.

As figuras devem indicar condições, unidades, versão e classificação CALCULADO. Não foram geradas nesta etapa; ficam especificadas para a etapa de resultados gráficos.

## Verificações atendidas

1. H = L sen(θ): aplicado em todos os pontos do Cenário A.
2. Com L fixo, E_g varia com θ: confirmado na tabela A.
3. Com H fixo, E_g permanece 58,86 J: confirmado na tabela B.
4. Com H fixo, L cresce quando θ diminui: confirmado na tabela B.
5. E_g e E_rol estão em joules; forças estão em newtons.
6. Pontos com F_g ≤ F_rol não são classificados como descarga espontânea.

## Interpretação

Com comprimento fixo, inclinações maiores produzem maior desnível e energia potencial, mas também aumentam a força motriz. Com desnível fixo, a energia potencial é invariável; reduzir a inclinação alonga a rampa e aumenta o trabalho de rolamento equivalente. A inclinação é, portanto, compromisso geométrico e de perdas, não fonte adicional de energia.

## Limitações

- c_r é coeficiente equivalente hipotético, não medição.
- Não há velocidade, potência, controle, cabo, tambor ou eficiência elétrica.
- A perda por rolamento não foi convertida em energia útil.
- Não há análise estrutural, econômica ou de segurança.
- O resultado é calculado e não valida o protótipo.

