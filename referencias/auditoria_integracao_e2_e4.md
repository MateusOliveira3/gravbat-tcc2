# Auditoria de integração científica E2–E4

**Pergunta central:** como a inclinação de uma trajetória guiada influencia parâmetros geométricos, mecânicos e eletromecânicos, em comparação com uma referência vertical, para massa e desnível equivalentes?

## Escopo e critério

E2, E3 e E4 não são uma única trajetória física. E2 é uma análise geométrica de inclinação e rolamento; E3 é o modelo V0.4 de torque resistente constante; E4 é o integrador V0.5 com torque dependente da velocidade e parâmetros elétricos equivalentes. A classificação abaixo evita tratar a continuidade de dados como se fosse validação de um único equipamento.

## Matriz de suficiência

| Pergunta | Hipótese | Equação implementada | Código | Referência | Cenário | Resultado existente | Conclusão permitida | Lacuna | Recomendação | Classificação |
|---|---|---|---|---|---|---|---|---|---|---|
| A inclinação altera o comprimento para H fixo? | Rampa retilínea, 0 < θ < 90° | `L=H/sen(θ)` | `model/geometry.py:geometria` | REF-002; REF-004 | E2, modo terreno | L cresce quando θ diminui | Geometria muda de forma determinística | Sem comparação vertical física | Usar vertical apenas como limite ideal | DEMONSTRADO |
| A energia potencial muda com θ para m,H fixos? | Campo gravitacional uniforme | `E_g=mgH` | `model/energy.py`, E1 | REF-003 como referência vertical | E1/E2 | E_g constante no cenário de H fixo | A inclinação não cria energia | Perdas de arquiteturas diferentes não comparadas | Manter E1 como linha de base | DEMONSTRADO |
| Como força e rolamento variam com θ? | `c_r` equivalente constante | `F_g=mg senθ`; `F_rol=c_r mg cosθ`; `E_rol=c_r mgH cotθ` | `model/mechanics.py`, E2 | REF-001; REF-002 | E2 | Força líquida e perdas tabeladas; limiar `tanθ>c_r` | Inclinação altera movimento e perdas sob a hipótese | `c_r` não é medido nem transferido da literatura | Comparar tendências e declarar hipótese | DEMONSTRADO |
| O θ de E2 influencia E3? | E3 recebe a mesma instância `base` | `F_0=mg(senθ-c_r cosθ)` | `model/coupling.py:acoplar` | REF-004 como contraste | E3 | `base.forcas.disponivel_N` e `base.geometria.L_m` entram no torque limite e tempo | Há integração de software entre E2 e E3 | E3 usa cenário próprio (`L=1,2 m`, θ=10°) e torque constante | Não misturar tabelas como uma mesma descarga | PARCIALMENTE DEMONSTRADO |
| E3 usa a mesma definição de L,H,v de E2? | `s` é distância ao longo do trilho; repouso e aceleração constante | `t=sqrt(2L/a)`, `v=a t` | `model/coupling.py` | REF-001; REF-004 | E3 | L e forças vêm de `base`; H aparece no balanço | Convenção de posição é compatível | H não participa diretamente da aceleração após `base`; não há velocidade prescrita | Rotular E3 como percurso fixo torque-constante | PARCIALMENTE DEMONSTRADO |
| O cabo está geometricamente consistente? | Raio constante, sem escorregamento | `ω_tambor=v_trilho/r`; `ω_saida=Gω` | `model/transmission.py:cinematica` | REF-004 | E3/E4 | Velocidade linear do trilho é convertida em rotação | Cinemática básica é consistente | Não modela camadas, inércia ou cabo real | Tratar como transmissão idealizada | PARCIALMENTE DEMONSTRADO |
| E4 recebe condições compatíveis? | Mesmo `base`, carga resistiva equivalente e parâmetros elétricos hipotéticos | `ω=Gv/r`; `F_carga=Gτ/(ηr)` | `simulation/electromechanical_dynamic.py` | REF-004 | E4 | Usa força disponível, massa e L da base; calcula torque conforme v | E4 é um aprofundamento eletromecânico do cenário mecânico | Trajetória e duração diferem de E3; não é a mesma descarga | Comparar somente grandezas homólogas | PARCIALMENTE DEMONSTRADO |
| O balanço de E3 fecha? | Torque e perdas constantes | `E_g=E_rol+E_perda_trans+E_eixo+E_k` | `model/coupling.py`, relatório E3 | REF-001/004 apenas como contexto | Torque ótimo | Balanço fecha por arredondamento | Consistência energética interna demonstrada | Não é validação experimental | Preservar separação E3/E4 | DEMONSTRADO |
| O balanço de E4 fecha? | Integração discreta, FEM equivalente e perdas resistivas | `E_g≈E_rol+E_perda_trans+E_em+E_k` | `simulation/electromechanical_dynamic.py`, relatório E4 | REF-004 como contraste | 8 Ω e varredura | Resíduo pequeno e convergência temporal documentada | Modelo fecha dentro da discretização declarada | Não há gerador caracterizado nem validação | Não chamar de medição | PARCIALMENTE DEMONSTRADO |
| É possível comparar ângulos com m,H fixos? | Recalcular `L` em modo terreno | `L=H/senθ` | `model/geometry.py`, `dashboard/scenarios.py` | REF-002/004 | E2 | Varredura de inclinação preserva H | Comparação paramétrica é possível | E3/E4 ainda não têm varredura integrada comum | Produzir matriz vertical ideal × ângulos inclinados | PARCIALMENTE DEMONSTRADO |
| A referência vertical é um equipamento completo? | Vertical como caso energético ideal | `E_g=mgH` | E1 e referências verticais | REF-003 | Comparação conceitual | Apenas energia potencial é comum | Não há comparação de perdas e transmissão reais | Não chamar vertical de θ=90° equivalente completo | NÃO DEMONSTRADO |

## Diagnóstico de integração

### O que já pode ser defendido

1. O núcleo geométrico calcula corretamente comprimento, desnível e ângulo em unidades SI.
2. E2 demonstra, sob `c_r` equivalente, o compromisso entre inclinação, força motriz e perdas.
3. E3 reutiliza a força líquida e o comprimento da simulação mecânica, mantendo `s` e `v` ao longo do trilho.
4. E4 reutiliza massa, força disponível e geometria da base, mas introduz um acoplamento elétrico dependente da velocidade.
5. Os balanços internos de E3 e E4 estão documentados separadamente.

### O que ainda não responde completamente à pergunta central

- Não existe uma arquitetura vertical física completa implementada para comparar perdas, transmissão e conversão.
- E3 e E4 usam trajetórias diferentes: torque constante em E3 e torque dependente da velocidade em E4.
- A literatura inclinada consultada em HTML (REF-004) usa co-simulação e parâmetros próprios; ela sustenta a relevância das grandezas, não os números do GravBat.
- REF-001 e REF-002 têm metadados confirmados, mas ainda não foram lidos integralmente.
- `c_r`, parâmetros elétricos, rendimento de transmissão e retificador são hipóteses ou equivalentes, não medições.

### Inconsistências metodológicas a explicitar

1. **Continuidade nominal não é identidade física:** passar a mesma `base` de E2 para E3/E4 não torna os experimentos uma única trajetória.
2. **Altura e comprimento:** E3 usa `L` diretamente na dinâmica; `H` aparece no balanço energético. Isso é coerente para uma rampa fixa, mas deve ser declarado.
3. **Velocidade:** E3 calcula velocidade pela aceleração; E4 também integra velocidade, enquanto a interface possui uma hipótese separada de velocidade-alvo. Não comparar essas curvas como se fossem o mesmo regime.
4. **Perdas:** E3 separa rolamento e transmissão; E4 acrescenta perdas resistivas e transmissão. O relatório deve evitar somar parcelas de trajetórias diferentes.
5. **Vertical:** `θ=90°` pode ser usado como referência geométrica/energética ideal, mas não como modelo de trilho, cabo ou suspensão real.

## Menor conjunto de análises adicionais necessário

Sem alterar o núcleo, a suficiência científica pode ser reforçada com análises documentais e gráficos derivados dos modelos já existentes:

1. Uma tabela comum para m e H fixos, comparando θ vertical ideal, 10°, 30° e 40° em `L`, `F_g`, `F_rol` e `E_rol`.
2. Uma tabela separada de E3 para os mesmos ângulos, mantendo explícito o torque constante.
3. Uma comparação E4 apenas para cenários que compartilhem a mesma `base`, carga e parâmetros elétricos.
4. Um quadro de nomenclatura distinguindo `s`, velocidade no trilho, velocidade vertical, velocidade da corda e rotação.
5. Conferência integral de REF-001 e REF-002 antes de afirmações bibliográficas específicas.

Essas análises não foram executadas nesta etapa, conforme a restrição de não criar novos experimentos.

## Organização sugerida no TCC II

1. **Referência energética:** E1 e modelo vertical ideal.
2. **Pergunta principal:** E2 como comparação geométrica e mecânica da inclinação.
3. **Consequências dinâmicas:** E3, com torque constante e limites claramente delimitados.
4. **Conversão:** E4, como modelo eletromecânico separado e condicionado.
5. **Escala e aplicação:** E5, como ordem de grandeza hipotética.
6. **Discussão integrada:** o que permanece igual (`mgH`), o que muda (`L`, forças, perdas, torque, velocidade) e o que não foi demonstrado (viabilidade física, econômica ou experimental).

## Referências prioritárias confrontadas

- [REF-001 — Qin et al.](https://doi.org/10.19799/j.cnki.2095-4239.2022.0634): metadados oficiais; texto integral pendente.
- [REF-002 — Zhang et al.](https://doi.org/10.19799/j.cnki.2095-4239.2023.0667): metadados oficiais; texto integral pendente.
- [REF-004 — Liu et al.](https://esst.cip.com.cn/CN/10.19799/j.cnki.2095-4239.2024.0243): HTML oficial consultado, com resumo, parâmetros e figuras.
- [REF-003 — Morstyn et al.](https://ora.ox.ac.uk/objects/uuid%3A0482b2fa-f51b-4276-a369-8892cb5095c4): metadados e resumo; manuscrito aceito listado no repositório.

**Conclusão:** E2–E4 são cientificamente suficientes para sustentar uma análise comparativa paramétrica, mas ainda não demonstram uma comparação completa entre equipamentos vertical e inclinado. A principal lacuna é de integração metodológica e referência vertical física, não uma falha evidente nas equações implementadas.
