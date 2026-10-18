# E5 — Escalabilidade e ciclo energético

**Classificação:** CALCULADO e SIMULADO (série sintética). **Data:** 12/10/2026. **Núcleo:** P0 congelado.

## Perguntas

Como massa, desnível, número de módulos e eficiências de recarga e descarga condicionam a capacidade energética de um sistema gravitacional modular? Em um excedente renovável sintético, quanta energia pode ser absorvida respeitando potência e capacidade?

## Modelo de ciclo

A energia potencial armazenável é E_g = m g H.

A energia elétrica de recarga é E_entrada_recarga = E_g / eta_subida.

A energia elétrica recuperável na descida é E_saida = eta_descida E_g.

Com eficiências constantes, eta_ciclo = eta_subida eta_descida.

As eficiências não foram medidas. São cenários paramétricos. O resultado E4 não foi transformado em eficiência universal: a razão específica carga AC/E_g do caso E4 de 8 ohm permanece válida somente para aquela trajetória e aqueles parâmetros equivalentes.

## Hipóteses da análise

- g = 9,81 m/s²;
- eta_subida = 0,80;
- eta_descida paramétrica = 0,55 e 0,80;
- módulos independentes e disponíveis;
- soma de energia linear apenas sob essa hipótese;
- sem dimensionamento estrutural, de segurança, transmissão ou frenagem.

## Capacidade por massa e desnível

A conversão é E_g(kWh) = m g H / 3.600.000 e E_g(Wh) = m g H / 3.600.

| massa (kg) | H (m) | E_g (kWh) | E_g (Wh) |
|---:|---:|---:|---:|
| 10 | 2 | 0,000055 | 0,055 |
| 10 | 10 | 0,000273 | 0,273 |
| 10 | 800 | 0,021800 | 21,800 |
| 100 | 2 | 0,000545 | 0,545 |
| 100 | 10 | 0,002725 | 2,725 |
| 100 | 800 | 0,218000 | 218,000 |
| 1.000 | 2 | 0,005450 | 5,450 |
| 1.000 | 10 | 0,027250 | 27,250 |
| 1.000 | 800 | 2,180000 | 2.180,000 |

Para 1.000 kg e 2 m, E_g = 5,450 Wh. Com eta_subida = 0,80 e eta_descida = 0,55, a energia de recarga é 6,8125 Wh e a energia recuperável é 2,9975 Wh; o rendimento de ciclo é 44%. Com descarga de 80%, a energia recuperável seria 4,360 Wh e o ciclo 64%.

## Escala modular

A capacidade total é calculada diretamente por E_total = N m g H, convertendo joules para kWh por 3.600.000.

| massa por módulo | H | número de módulos | capacidade total |
|---:|---:|---:|---:|
| 10 kg | 2 m | 10 | 0,000545 kWh |
| 100 kg | 10 m | 10 | 0,027250 kWh |
| 1.000 kg | 10 m | 10 | 0,272500 kWh |
| 1.000 kg | 800 m | 10 | 21,800000 kWh |

A agregação é soma linear de módulos independentes. Isso não implica potência, disponibilidade, espaço, segurança ou capacidade estrutural linear.

## Cenário topográfico hipotético inspirado na Serra do Mar

Premissas ilustrativas: H = 800 m, percurso = 8 km e inclinação média equivalente de aproximadamente 5,74°. Não são levantamento topográfico, trilho validado ou autorização de implantação.

### Um módulo de 1.000 kg

- energia potencial: **2,180 kWh**;
- energia elétrica de recarga a 80%: **2,725 kWh**;
- energia recuperável a 55%: **1,199 kWh**.

### Dez módulos de 1.000 kg

- energia potencial agregada: **21,800 kWh**;
- energia elétrica de recarga a 80%: **27,250 kWh**;
- energia recuperável a 55%: **11,990 kWh**;
- rendimento de ciclo hipotético: **44%**.

Esses valores são ordem de grandeza energética. Não é permitido extrapolar a dinâmica E4 de 6 kg por simples multiplicação. Estrutura, cabo, tambor, frenagem, segurança, percurso real e operação permanecem não dimensionados. Uso de resíduos como lastro é apenas hipótese futura, sem pressupor destinação ambiental ou viabilidade sanitária.

## Excedente renovável sintético

Foi usada uma série artificial de seis intervalos de uma hora, explicitamente sem dados do ONS:

| intervalo | excedente disponível (kW) | limite carga (kW) | energia absorvida da fonte (kWh) | estado armazenado (kWh) |
|---:|---:|---:|---:|---:|
| 1 | 0,0 | 0,4 | 0,00 | 0,00 |
| 2 | 0,5 | 0,4 | 0,40 | 0,32 |
| 3 | 1,2 | 0,4 | 0,40 | 0,64 |
| 4 | 0,8 | 0,4 | 0,40 | 0,96 |
| 5 | 0,0 | 0,4 | 0,00 | 0,96 |
| 6 | 0,6 | 0,4 | 0,05 | 1,00 |

A energia absorvida do excedente é 1,25 kWh de entrada, limitada pela capacidade; ela produz 1,00 kWh armazenado. Com eta_descida = 0,55, a energia elétrica disponibilizável posteriormente é 0,55 kWh.

Este cálculo representa energia potencialmente absorvível por um armazenamento idealizado. Não representa redução efetiva de curtailment, pois não modela rede, despacho, segurança ou restrições de transmissão.

## Verificações

- unidades convertidas entre J, Wh e kWh;
- eficiências entre zero e um;
- estado de carga limitado entre zero e a capacidade;
- absorção limitada por excedente, potência e capacidade;
- energia de saída limitada à energia armazenada vezes a eficiência de descarga;
- resultados E4 não foram extrapolados como eficiência universal;
- módulos somados apenas sob hipótese explícita de independência.

## Figuras essenciais

1. Capacidade ideal versus massa e desnível.
2. Capacidade agregada versus número de módulos.
3. Energia de recarga, saída e perdas para diferentes eficiências.
4. Série sintética de excedente, absorção e estado de carga.
5. Comparação de ordem de grandeza entre bancada e cenário hipotético de 800 m.

## Limitações

- Eficiências de subida e descarga são hipóteses paramétricas.
- O cenário de 800 m e 8 km é estritamente ilustrativo.
- Não há modelo de recarga eletromecânica, ciclo completo ou potência de carga/descarga dos módulos.
- Não há estrutura, segurança, cabo, transmissão, frenagem ou economia.
- A série de excedente é sintética e não prova curtailment mitigado.
- Não há validação experimental.
- O registro de testes permanece 73 aprovados em 74, com erro ambiental de limpeza temporária no Windows.

E5 encerra a análise experimental autorizada. Não foram iniciados novos experimentos.

