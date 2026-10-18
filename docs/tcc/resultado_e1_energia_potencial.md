# E1 — Energia potencial gravitacional

**Classificação:** CALCULADO. **Data:** 12/10/2026. **Versão:** núcleo P0 congelado.

## Pergunta

Como massa e desnível vertical determinam a energia potencial disponível, antes de perdas e conversão?

## Método

Aplicou-se diretamente E_g = m g H, com g = 9,81 m/s². A energia útil não participa do resultado principal. A matriz usa massas de 10, 100, 1.000 e 10.000 kg e desníveis de 1, 2, 5, 10 e 20 m.

## Resultados — energia potencial bruta

| massa (kg) | H (m) | E_g (J) | E_g (Wh) | E_g (kWh) |
|---:|---:|---:|---:|---:|
| 10 | 1 | 98.10 | 0.027 | 0.000027 |
| 10 | 2 | 196.20 | 0.055 | 0.000055 |
| 10 | 5 | 490.50 | 0.136 | 0.000136 |
| 10 | 10 | 981.00 | 0.273 | 0.000273 |
| 10 | 20 | 1962.00 | 0.545 | 0.000545 |
| 100 | 1 | 981.00 | 0.273 | 0.000273 |
| 100 | 2 | 1962.00 | 0.545 | 0.000545 |
| 100 | 5 | 4905.00 | 1.363 | 0.001362 |
| 100 | 10 | 9810.00 | 2.725 | 0.002725 |
| 100 | 20 | 19620.00 | 5.450 | 0.005450 |
| 1000 | 1 | 9810.00 | 2.725 | 0.002725 |
| 1000 | 2 | 19620.00 | 5.450 | 0.005450 |
| 1000 | 5 | 49050.00 | 13.625 | 0.013625 |
| 1000 | 10 | 98100.00 | 27.250 | 0.027250 |
| 1000 | 20 | 196200.00 | 54.500 | 0.054500 |
| 10000 | 1 | 98100.00 | 27.250 | 0.027250 |
| 10000 | 2 | 196200.00 | 54.500 | 0.054500 |
| 10000 | 5 | 490500.00 | 136.250 | 0.136250 |
| 10000 | 10 | 981000.00 | 272.500 | 0.272500 |
| 10000 | 20 | 1962000.00 | 545.000 | 0.545000 |

## Relações observadas

- Mantido H, a energia cresce linearmente com a massa.
- Mantida a massa, a energia cresce linearmente com H.
- Para 1.000 kg e 2 m, E_g = 19.620 J = 5,450 Wh.
- Para 10 kg e 2 m, E_g = 196,2 J = 0,0545 Wh.
- A inclinação não aparece na equação principal: com o mesmo desnível, ela altera a geometria e a força ao longo do percurso, mas não a energia potencial inicial.

## Energia útil condicionada

Se uma eficiência global de descarga for assumida, E_útil = E_g η. Isso é uma estimativa condicionada, não uma medição. Para 1.000 kg e 2 m:

| eficiência assumida | energia útil (Wh) |
|---:|---:|
| 55% | 2,998 Wh |
| 80% | 4,360 Wh |

Eficiência, perdas mecânicas e conversão eletromecânica serão analisadas nos Experimentos 2 e 4.

## Interpretação

O E1 estabelece a escala energética ideal. Ele permite verificar a ordem de grandeza de uma massa e um desnível sem atribuir potência, duração ou atendimento de carga. Potência e tempo dependem da dinâmica e ficam fora deste experimento.

## Limitações

- Não inclui perdas, eficiência, potência, velocidade ou tempo de descarga.
- Não representa recarga nem rendimento de ciclo.
- Não é validação experimental.
- A matriz é análise paramétrica, não otimização.

## Reprodutibilidade

A tabela foi gerada pela equação E_g = m g H, com g fixado em 9,81 m/s² e as listas de massas e alturas registradas acima.

