# Auditoria de reprodutibilidade E1–E5

**Data da auditoria:** 23/10/2026  
**Branch auditada:** `fix/coerencia-fisica-dashboard`  
**Commit de referência:** `868fe53 Integra dashboard compacto e documentacao para apresentacao`

## Escopo e método

Esta auditoria verifica se os experimentos consolidados podem ser reexecutados a partir do código, dos relatórios e das dependências atualmente versionados. Nenhum modelo, equação, parâmetro ou resultado E1–E5 foi alterado. Os rótulos usados abaixo são: **CALCULADO** (equação avaliada diretamente), **SIMULADO** (execução numérica), **HIPÓTESE** (parâmetro ou arquitetura assumida) e **VERIFICADO** (propriedade conferida por teste ou cálculo independente).

Foram executados:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py config.py verificar_dashboard.py model\*.py simulation\*.py dashboard\*.py
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

A compilação Python passou. A suíte teve **88 testes: 87 aprovados e 1 erro ambiental** na limpeza de diretório temporário do Windows (`PermissionError: [WinError 5]`) em `tests.test_mechanics.TesteMecanico.test_Q_importacao_sem_efeitos`; não houve falha funcional ou científica identificada.

## Matriz de reprodução

| Experimento | Implementação auditada | Evidência reproduzida | Classificação | Estado |
|---|---|---|---|---|
| E1 — energia potencial | `model/energy.py`, relatórios E1 | `E=m g H` | CALCULADO / VERIFICADO | Reproduzível |
| E2 — geometria e perdas | `model/geometry.py`, `model/mechanics.py` | `H=L sen(theta)`, forças e rolamento | CALCULADO / VERIFICADO | Reproduzível |
| E3 — torque e potência | `model/coupling.py`, `simulation/simulator.py` | V0.4 com torque constante | SIMULADO / VERIFICADO | Reproduzível sob hipóteses V0.4 |
| E4 — conversão eletromecânica | `simulation/electromechanical_dynamic.py`, `model/electromechanics.py` | Integração dependente da velocidade | SIMULADO / HIPÓTESE | Reproduzível com limitações |
| E5 — escala e ciclo | relatório E5 e fórmulas documentadas | `N m g H / 3.600.000` e série sintética | CALCULADO / SIMULADO | Reproduzível como cálculo idealizado |

## Conferência numérica independente

Cenário comum da comparação: `m=6 kg`, `H=1 m`, `g=9,81 m/s²`, `c_r=0,02`, ângulos de 10°, 20°, 30° e 40°. A referência vertical de 90° é apenas limite geométrico e energético ideal.

| Ângulo | L (m) | Fg,t (N) | Frol (N) | F líquida (N) | Erol (J) |
|---:|---:|---:|---:|---:|---:|
| 10° | 5,758770 | 10,220932 | 1,159316 | 9,061616 | 6,676233 |
| 20° | 2,923804 | 20,131306 | 1,106206 | 19,025099 | 3,234330 |
| 30° | 2,000000 | 29,430000 | 1,019485 | 28,410515 | 2,038970 |
| 40° | 1,555724 | 37,834479 | 0,901788 | 36,932691 | 1,402932 |
| 90° ideal | 1,000000 | 58,860000 | 0 | 58,860000 | 0 |

Para todos os ângulos, `E_g = m g H = 58,86 J`. Os valores foram obtidos independentemente e coincidem com `docs/tcc/matriz_resultados_comparativos.csv` dentro do arredondamento publicado. Isso verifica a tese geométrica central de E2: mantendo massa e desnível, a energia potencial permanece constante, enquanto comprimento e perdas por rolamento mudam.

### E3

A execução de `simular` seguida de `acoplar` usa o torque no eixo de saída do modelo V0.4, com reflexão `F_carga = G tau/(eta_t r_d)`. Para `tau=0,1 N m`, `r_d=0,05 m`, `G=1` e `eta_t=0,90`, os casos de 10°–40° permaneceram em `DESCE_COM_CARGA`. O balanço interno fecha numericamente (resíduo da ordem de `10^-14 J` nos casos reproduzidos). O tempo, a velocidade e a potência dependem do torque absoluto e da geometria; não são uma única trajetória física compartilhada com E4.

### E4

A integração `simular_descida_eletromecanica` completou os quatro cenários com os parâmetros de bancada do código (`K_e=0,1`, `R_fase=2 ohm`, duas fases, carga de 8 ohm, `r_d=0,05 m`, `G=1`, `eta_t=0,90`, passo de 0,001 s). Uma execução independente forneceu:

| Ângulo | status | tempo (s) | velocidade final (m/s) | energia eletromagnética integrada (J) | cobre acumulado (J) |
|---:|---|---:|---:|---:|---:|
| 10° | DESCE | 2,859 | 3,8914 | 6,0823 | 1,2165 |
| 20° | DESCE | 1,381 | 4,1626 | 3,2726 | 0,6545 |
| 30° | DESCE | 0,930 | 4,2555 | 2,2844 | 0,4569 |
| 40° | DESCE | 0,717 | 4,2985 | 1,7899 | 0,3580 |

Esses números são **simulação de um equivalente eletromecânico hipotético**, não medição de gerador. O relatório E4 também registra a distinção entre energia eletromagnética, energia na carga AC, energia CC estimada e perda de cobre; elas não devem ser somadas sem respeitar a definição de cada parcela. O histórico do E4 registra a correção do balanço de 100 ohm (`E_em=0,05965896 J`, `E_carga=0,05848918 J`, `E_cobre=0,00116978 J`).

### E5

A conferência direta de `N m g H / 3.600.000` reproduziu, para dez módulos de 1.000 kg a 800 m, `21,8 kWh`; para um módulo, `2,18 kWh`. A tabela documentada também contém `0,000545 kWh` (10 módulos de 10 kg a 2 m), `0,027250 kWh` (10 módulos de 100 kg a 10 m) e `0,272500 kWh` (10 módulos de 1.000 kg a 10 m). A série de excedente solar/eólico é explicitamente **SIMULADA e sintética**; não demonstra curtailment mitigado.

## Figuras e rastreabilidade

Figuras consolidadas disponíveis:

- `docs/tcc/figuras_consolidadas/figura_01_e1_energia.svg`
- `docs/tcc/figuras_consolidadas/figura_02_e2_geometria.svg`
- `docs/tcc/figuras_consolidadas/figura_03_e3_potencia.svg`
- `docs/tcc/figuras_consolidadas/figura_04_e5_excedente.svg`

Figuras comparativas já produzidas:

- `docs/tcc/figuras_consolidadas/figura_comparacao_geometria.svg`
- `docs/tcc/figuras_consolidadas/figura_comparacao_forcas.svg`
- `docs/tcc/figuras_consolidadas/figura_comparacao_e4.svg`
- `docs/tcc/figuras_consolidadas/figura_comparacao_e4_potencia.svg`

Foi conferida a presença dos arquivos e suas raízes SVG. A figura temporal detalhada do E4 permanece pendente. A inspeção visual final no navegador não foi concluída nesta auditoria: o acesso automatizado ao Streamlit/local HTTP permanece indisponível neste ambiente. Portanto, a existência e a rastreabilidade estática das figuras não equivalem a aprovação visual da interface.

## Divergências e limitações

1. A suíte contém um erro ambiental de limpeza no Windows; ele deve ser reproduzido ou resolvido no computador do orientador antes de declarar uma suíte completamente verde.
2. E3 (torque constante) e E4 (torque eletromagnético dependente da velocidade) são modelos diferentes; seus tempos e energias não devem ser apresentados como uma única trajetória.
3. Os parâmetros de E4 são hipóteses de equivalente de gerador e carga, sem caracterização experimental.
4. E5 é escalabilidade idealizada e série sintética, sem validação estrutural, econômica ou de curtailment.
5. Não há validação experimental física dos modelos.
6. A interface precisa de inspeção manual no navegador antes da apresentação ao orientador.

## Veredito de reprodutibilidade

O núcleo computacional E1–E5 está **reproduzível para estudo computacional**, com a ressalva do erro ambiental de limpeza e das hipóteses explicitadas. O projeto ainda não deve ser declarado visualmente pronto para apresentação sem uma execução local do Streamlit e conferência manual da animação, gráficos, parâmetros e auditoria.
