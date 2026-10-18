# 19 — Matriz de experimentos computacionais do TCC-2

Grandezas fechadas são CALCULADAS; trajetórias temporais são SIMULADAS; parâmetros sem medição são HIPÓTESES.

| Experimento | Pergunta e variáveis | Método | Resultado/figura | Limitação |
|---|---|---|---|---|
| 1. Massa e energia | Como massa, altura e eficiência alteram energia? Independentes: massa, desnível, eficiência. | Energia gravitacional e energia útil; varredura simples. | Energia versus massa e desnível. | Não inclui estrutura, ciclo ou envelhecimento. |
| 2. Inclinação e perdas | Qual o compromisso geométrico? Independentes: ângulo, comprimento, desnível, coeficiente de rolamento. | Relações geométricas e força disponível; comparar comprimento fixo e desnível fixo. | Comprimento, força e perda versus inclinação. | Coeficiente equivalente; estrutura não dimensionada. |
| 3. Carga e potência | Como torque resistente altera descarga? Independentes: massa, carga, raio e relação. | Integrador eletromecânico assinado. | Posição, velocidade, torque, potência, tempo e caso de parada. | Sem inércia rotacional detalhada. |
| 4. Conversão | Quanto perdas reduzem energia útil? Independentes: eficiência, resistência, carga e parâmetros do gerador. | Cadeia de eficiências e modelo elétrico equivalente. | Balanço de potência e energia. | Parâmetros não medidos e modelo multifásico reduzido. |
| 5. Escala e aplicação | Quantos módulos atendem evento definido por energia, potência e duração? Qual energia de recarga e rendimento de ciclo são necessários? | Módulos por energia e potência; estimativa de energia de recarga e rendimento de ciclo; marcar pico sem duração como insuficiente. | Módulos versus energia e potência, com recarga separada. | Não prova despacho, curtailment mitigado ou economia; não exige novo motor, controlador ou eletrônica detalhada. |

Cada execução registra versão, geometria, massa, ângulo, altura, comprimento, perdas, eficiência, velocidade, passo, parâmetros elétricos e status.

## Figuras essenciais

1. Energia útil versus massa e desnível — CALCULADO.
2. Comprimento e força versus inclinação nos dois controles — CALCULADO.
3. Posição, velocidade e energia no tempo com e sem carga — SIMULADO.
4. Potência eletromagnética, carga e cobre — SIMULADO/CALCULADO.
5. Sensibilidade a perdas — CALCULADO.
6. Módulos necessários por energia e potência — CALCULADO.
7. Convergência temporal e parada — SIMULADO/VERIFICADO.

Toda figura terá eixos, unidades, condições, versão, classificação epistemológica e limitação.

A sequência é 1 e 2, depois 3 e 4, e por fim 5. Não iniciar otimização ou larga escala antes da interpretação básica.

