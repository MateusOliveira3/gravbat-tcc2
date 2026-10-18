# E4 — Conversão eletromecânica

**Classificação:** SIMULADO/CALCULADO sob hipóteses eletromecânicas. **Data:** 12/10/2026. **Núcleo:** P0 congelado.

## Pergunta

Como os parâmetros eletromecânicos e a resistência de carga influenciam potência elétrica, energia recuperada, velocidade e duração da descarga?

## Auditoria do modelo existente

O modelo disponível é o equivalente parametrizado em `model/electromechanics.py`, integrado por `simulation/electromechanical_dynamic.py`.

Para velocidade linear v, raio r_d e relação G:

- velocidade angular: omega = G v/r_d;
- FEM de pico: e = K_e |omega|;
- corrente de pico equivalente: I = e/(R_fase + R_carga);
- potência na carga: P_carga = n_fases · 0,5 · I² R_carga;
- perda no cobre: P_cobre = n_fases · 0,5 · I² R_fase;
- potência eletromagnética: P_em = P_carga + P_cobre;
- torque resistente: tau_em = P_em/|omega|;
- potência CC estimada: P_CC = eta_retificador P_carga.

A convenção é dissipativa: o torque eletromagnético é refletido à massa como força resistente G tau_em/(eta_t r_d). O rendimento mecânico aparece uma vez nessa reflexão. A integração acumula P_em e a perda de cobre por regra trapezoidal. A energia entregue à carga deve ser integrada separadamente a partir de P_carga; energia CC é eta_retificador vezes essa parcela.

Não há modelo de ponte retificadora real, forma de onda completa, inércia rotacional ou controle ativo.

## Cenário de referência

m = 6 kg; L = 1,20 m; theta = 10°; c_r = 0,02; r_d = 0,05 m; G = 1; eta_t = 0,90; partida do repouso; passo temporal de 0,001 s.

Parâmetros eletromecânicos usados como hipótese do modelo: K_e = 0,1 V s/rad, R_fase = 2 ohm, 2 fases, eta_retificador = 0,90. Eles são parâmetros disponíveis no projeto/testes, não medição do protótipo nem especificação confirmada de fabricante.

## Varredura limitada de carga

| R_carga (ohm) | status | tempo (s) | velocidade final (m/s) | energia eletromagnética (J) | energia carga AC (J) | energia CC estimada (J) | perda cobre (J) | potência carga máxima (W) |
|---:|:---:|---:|---:|---:|---:|---:|---:|---:|
| 1e12 | DESCE | 1,261 | 1,9044 | 0,0000 | 0,0000 | 0,0000 | 0,0000 | 0,0000 |
| 100 | DESCE | 1,263 | 1,8988 | 0,0597 | 0,0585 | 0,0526 | 0,0012 | 0,1386 |
| 4 | DESCE | 1,294 | 1,8063 | 0,9760 | 0,6507 | 0,5856 | 0,3253 | 1,4501 |
| 2 | DESCE | 1,312 | 1,7593 | 1,4370 | 0,7185 | 0,6467 | 0,7185 | 1,5475 |
| 1 | DESCE | 1,329 | 1,7113 | 1,8745 | 0,6248 | 0,5623 | 1,2496 | 1,3015 |
| 8 | DESCE | 1,281 | 1,8458 | 0,5958 | 0,4766 | 0,4290 | 0,1192 | 1,0902 |
| 0,1 | DESCE | 1,361 | 1,6326 | 2,5875 | 0,1232 | 0,1109 | 2,4643 | 0,2418 |
| 0,001 | DESCE | 1,367 | 1,6204 | 2,7032 | 0,00135 | 0,00122 | 2,7018 | 0,0026 |

A carga intermediária de 8 ohm foi escolhida para o balanço representativo. As cargas adicionais de 1, 2 e 4 ohm mostram o entorno da resistência de fase de 2 ohm, sem assumir que casamento de resistências maximize a energia integrada. A carga de 0,001 ohm produz forte dissipação resistiva e baixa energia útil na carga. Nenhum caso desta varredura para antes do fim, pois os parâmetros K_e e R_fase adotados não geram frenagem suficiente para superar a força motriz. Isso é um resultado do cenário hipotético, não evidência de que a parada seja impossível; o teste P0 independente de desaceleração permanece a referência para essa propriedade do integrador.

## Verificação de identidade da potência eletromagnética em 100 ohm

A reprodução com passo de 0,001 s forneceu E_em = 0,05965896 J, E_carga = 0,05848918 J e E_cobre = 0,00116978 J. A soma E_carga + E_cobre = 0,05965896 J, portanto a identidade fecha. Os valores anteriores de 0,0573 J e 0,0012 J eram erro de transcrição/arredondamento da integração da carga, não inconsistência do modelo.

## Convergência temporal em 8 ohm

| passo (s) | tempo (s) | energia carga (J) | energia cinética final (J) | resíduo (J) |
|---:|---:|---:|---:|---:|
| 0,001 | 1,2810 | 0,4766246 | 10,2205699 | -0,0086093 |
| 0,0005 | 1,2805 | 0,4760626 | 10,2126045 | 0,0001367 |
| 0,00025 | 1,2805 | 0,4760541 | 10,2124242 | 0,0003288 |

A energia na carga e a energia cinética estabilizam entre 0,0005 e 0,00025 s. O resíduo permanece inferior a 0,009 J nos três casos e resulta da discretização temporal e do avanço de posição/velocidade no integrador. Não é declarada ordem de convergência.

As potências médias na carga AC, obtidas por energia integrada dividida pelo tempo da mesma trajetória, são aproximadamente: 0,0000 W (1e12 ohm), 0,0453 W (100 ohm), 0,3720 W (8 ohm), 0,0905 W (0,1 ohm) e 0,0010 W (0,001 ohm). Elas não devem ser confundidas com as potências instantâneas máximas da tabela.

## Balanço representativo: R_carga = 8 ohm

Para a mesma trajetória eletromecânica integrada:

- energia potencial gravitacional: 12,2651 J;
- perda por rolamento: 1,3912 J;
- energia cinética final: 10,2206 J;
- potência eletromagnética integrada: 0,5958 J;
- energia na carga AC: 0,4766 J;
- perda resistiva no cobre: 0,1192 J;
- energia CC estimada após retificador: 0,4290 J;
- trabalho mecânico na entrada da transmissão: 0,6620 J;
- perda estimada na transmissão: 0,0662 J.

O balanço aproximado é:

E_g = E_rol + E_perda_trans + E_em + E_cinetica_final

12,2651 = 1,3912 + 0,0662 + 0,5958 + 10,2206 J

O resíduo é aproximadamente -0,0086 J, compatível com o passo temporal e o tratamento discreto da posição/velocidade. A energia cinética final não é energia elétrica recuperada.

## Verificações

- P_em = P_cobre + P_carga: confirmado numericamente no modelo.
- Dissipações resistivas são não negativas.
- Carga alta reduz a extração; carga muito baixa aumenta a parcela dissipada no cobre.
- Potência instantânea, energia integrada e potência média são grandezas distintas.
- A trajetória com 8 ohm não deve ser comparada diretamente à trajetória torque-constante do E3 como se fosse a mesma descarga.
- A integração usa passo 0,001 s; o fechamento P0 já registrou convergência temporal para o cenário eletromecânico.

## Figuras necessárias

1. Velocidade e posição versus tempo para 1e12, 8, 0,1 e 0,001 ohm.
2. Potência de carga, potência de cobre e potência eletromagnética versus tempo para 8 ohm.
3. Balanço energético do caso de 8 ohm.

As figuras são especificadas para consolidação posterior; não foram geradas nesta rodada.

## Limitações

- parâmetros elétricos hipotéticos e não medidos;
- máquina representada por equivalente de FEM e resistência;
- ponte retificadora não modelada em detalhe;
- ausência de inércia rotacional detalhada;
- ausência de controle ativo e dimensionamento térmico;
- ausência de recarga e rendimento de ciclo completo;
- ausência de validação experimental;
- rendimento de transmissão e eficiência do retificador assumidos;
- baixa carga pode resultar em grande dissipação no cobre, conforme a formulação equivalente.

E4 determina apenas o que este modelo permite calcular sobre energia elétrica recuperável. E5 permanece fora desta entrega.

