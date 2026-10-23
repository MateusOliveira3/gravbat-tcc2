# Discussão energética comparativa

## Escopo

Esta discussão usa a matriz `docs/tcc/matriz_resultados_comparativos.csv`, os modelos E1/E2, o modelo mecânico V0.4 do E3 e o integrador eletromecânico V0.5 do E4. Os resultados são CALCULADOS ou SIMULADOS sob hipóteses; não são medições.

## Compromisso entre potência, duração, extração elétrica e energia cinética remanescente

Para `m=6 kg` e `H=1 m`, a energia potencial inicial permanece `E_g=58,86 J` em todos os ângulos. A inclinação não cria energia adicional.

O aumento de θ reduz o comprimento da trajetória: de 5,7588 m a 10° para 1,5557 m a 40°. No modelo de rolamento equivalente, o trabalho dissipado também diminui de 6,6762 J para 1,4029 J. A força líquida disponível aumenta de 9,0616 N para 36,9327 N.

No E3, isso produz maior aceleração e menor duração. Os resultados dependem do torque adotado. O regime de torque absoluto de 0,1 N·m não é o mesmo carregamento físico do regime normalizado em `0,5 τ_lim`; portanto os dois regimes respondem perguntas diferentes.

No E4, a potência média AC aumenta nos cenários calculados, enquanto a energia AC integrada diminui:

| θ | duração (s) | energia AC (J) | potência média AC (W) | energia cinética final (J) | E_AC/E_g | E_k/E_g |
|---:|---:|---:|---:|---:|---:|---:|
| 10° | 2,8590 | 4,8658 | 1,7018 | 45,4293 | 8,27% | 77,20% |
| 20° | 1,3810 | 2,6181 | 1,8965 | 51,9807 | 4,45% | 88,31% |
| 30° | 0,9300 | 1,8275 | 1,9651 | 54,3285 | 3,10% | 92,30% |
| 40° | 0,7170 | 1,4319 | 1,9969 | 55,4302 | 2,43% | 94,18% |

A tendência ocorre porque o modelo elétrico extrai potência durante a trajetória, mas a descarga mais rápida reduz o tempo de integração. A energia cinética remanescente cresce com o ângulo, mostrando que chegar ao fim da rampa não significa chegar em repouso.

## Balanço energético e nomenclatura

O E4 separa:

- energia eletromagnética acumulada;
- energia AC na carga;
- perda resistiva no cobre;
- energia CC estimada após o retificador;
- energia cinética final.

A energia CC é a energia AC multiplicada pela eficiência de retificação e não deve ser somada à energia AC. A perda de transmissão não aparece como parcela independente no integrador E4 comparativo e permanece uma limitação declarada. O resíduo energético é numérico e deve ser lido com o passo de integração de 0,001 s.

Nenhuma parcela foi interpretada como energia recuperável em uma frenagem posterior. Isso exigiria outro modelo.

## Conclusões permitidas

1. Para massa e desnível constantes, a energia potencial ideal é invariável.
2. Aumentar a inclinação reduz percurso e perdas de rolamento no modelo adotado.
3. A força motriz aumenta e a duração diminui nos cenários estudados.
4. No E4, potência média AC e energia AC integrada respondem de forma diferente à inclinação.
5. A extração elétrica e a energia cinética final dependem dos parâmetros eletromecânicos e da carga.

## Conclusões não permitidas

- não há inclinação universalmente ótima;
- não foi demonstrada superioridade sobre uma arquitetura vertical real;
- `E_AC/E_g` não é rendimento de ciclo completo;
- a energia cinética final não é energia elétrica recuperada;
- não há validação experimental ou demonstração de viabilidade estrutural.

## Rastreabilidade

Os dados vêm de `matriz_resultados_comparativos.csv`. A geometria e as forças são calculadas por `model.geometry` e `model.mechanics`; E3 por `model.coupling`; E4 por `simulation.electromechanical_dynamic` e `model.electromechanics`. A referência de 90° é somente ideal e não alimenta E3/E4.
