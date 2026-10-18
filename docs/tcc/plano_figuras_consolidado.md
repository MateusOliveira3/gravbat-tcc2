# Plano de figuras consolidado E1–E5

Foram geradas quatro figuras SVG quantitativas reconstruídas a partir de equações e dados documentados. Elas são apoio à redação e não dados experimentais.

| Arquivo | Experimento | Evidência | Fonte/procedimento | Limitação |
|---|---|---|---|---|
| figuras_consolidadas/figura_01_e1_energia.svg | E1 | CALCULADO | E=m g H; m={10,100,1000,10000} kg; H={2,10,800} m; eixo vertical logarítmico | Não inclui eficiência ou potência |
| figuras_consolidadas/figura_02_e2_geometria.svg | E2 | CALCULADO | H=1 m, m=6 kg, c_r=0,02; L=H/sen(theta); E_rol=c_r m g H cot(theta) | Painéis separados para comprimento (m) e energia (J) |
| figuras_consolidadas/figura_03_e3_potencia.svg | E3 | CALCULADO | V0.4; tau/tau_lim de 0,01 a 0,99; eta_t=0,90; ponto 2/3 marcado em 2,9881 W | Curva analítica; torque constante, não motor real |
| figuras_consolidadas/figura_04_e5_excedente.svg | E5 | SIMULADO sintético | Excedente [0,0;0,5;1,2;0,8;0;0,6] kW; absorção [0;0,4;0,4;0,4;0;0,05] kW; SOC [0;0,32;0,64;0,96;0,96;1] kWh | Não usa dados ONS e não prova curtailment |

## Figuras pendentes

A curva temporal detalhada de E4 não foi gerada porque o relatório preserva resultados agregados, não a série completa de estados para cada carga. Gerá-la exigiria nova execução, que fica fora desta rodada.

As figuras têm título, eixos numerados, unidades, fonte, parâmetros e classificação. Os pontos foram calculados com as equações e séries acima, sem coordenadas visuais arbitrárias. As tabelas dos relatórios continuam sendo a fonte quantitativa primária.

