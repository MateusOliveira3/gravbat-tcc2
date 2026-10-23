GravBat | Plano operacional E6.3 e E6.4
Data: 23/10/2026
Origem: revisão do relatório e6_modelo_descarga_regulada.md, do CSV E6.2 e das referências do Google Docs TCC II v2.1.
Status: plano de execução e estimativas analíticas, não resultados de simulação E6.3/E6.4.
Instrução ao Codex
Trabalhe no repositório local C:\Users\Pichau\Documents\Codex\2026-09-29\gravbat-tcc2. Não modifique o comportamento, as saídas nem os testes históricos de E1–E5. Faça alterações isoladas para E6 e documentação bibliográfica. Não execute commit, push, merge ou deploy. Não apresente resultados de cálculos exploratórios como resultados simulados.
A. Sincronizar bibliografia antes das simulações
1. Localize os arquivos de referências, citações, documentação científica, README e relatórios do projeto. Faça um inventário dos DOI existentes e compare com o catálogo abaixo, que corresponde ao Google Docs v2.1.
2. Crie ou atualize um arquivo canônico versionado, preferencialmente docs/tcc/referencias_canonicas.md, com as referências [1]–[18], DOI, URL, papel científico, condição de comparação e status de verificação. Não renumere as referências já citadas no TCC.
3. Para os artigos [6], [7], [9], [17], [18], verifique o título, autor principal, periódico, ano, volume, páginas e DOI com o editor. Corrija inconsistências entre os documentos do repositório e o catálogo; se houver divergência relevante, registre-a, não a resolva silenciosamente.
4. Não trate coeficientes, rendimentos ou valores de potência de outros trabalhos como parâmetros calibrados do GravBat. Identifique cada dado como literatura, hipótese, derivação ou resultado_simulado.
5. Faça auditoria automatizada dos DOI duplicados, ausentes, malformados e das referências [n] sem entrada correspondente.
B. Corrigir o E6.2 (E6.3)
1. Regime B: a condição v=L/T é uma referência estacionária, não uma trajetória completa. Implementar estado dinâmico x(t), v(t) com partida, saturação, parada e chegada. Separar claramente a referência estacionária de uma trajetória fisicamente simulada.
2. Energia: contabilizar E_g = E_rol + E_transmissao + E_eixo/freio + E_cobre + E_carga + ΔE_cinetica + residuo, usando fronteiras coerentes e sem dupla contagem. Na referência estacionária a 10°, E_g=58,86 J, E_rol≈6,676 J, E_transmissao≈5,218 J e E_freio_eixo≈46,965 J, caso η_t=0,9 seja aplicado ao fluxo de potência restante. Documentar exatamente como η_t atua na dinâmica e no balanço.
3. Saturação: torque máximo de freio insuficiente para o equilíbrio implica aceleração, não BLOQUEADO. Bloqueio por torque excessivo, estol, falha de partida e chegada devem ser estados distintos e testados.
4. Energia cinética: nunca declarar v_final>0 e E_cinetica_final=0 no mesmo estado físico. Para v=0,09598 m/s, m=6 kg, E_k≈0,02764 J.
5. Integrador E4: investigar resíduo energético entre 0,208 e 0,672 J. Fazer estudo de convergência dt=1e-3, 5e-4, 1e-4 e documentar tratamento do evento de chegada. Não modificar o integrador histórico E4 para ocultar diferenças; criar correções isoladas ou novas versões se necessário.
6. Atualizar o relatório com a suíte efetivamente executada: 91 testes, 90 aprovados e 1 erro ambiental reportado pelo usuário, sujeitos a nova execução local. Não transformar o erro de Windows em aprovação.
C. Hipótese analítica prioritária: transmissão como alavanca do E6.4
Cenário de estudo, não resultado confirmado: m=6 kg, H=1 m, θ=10°, c_r=0,02, r_d=0,05 m, η_t=0,90, K_e=0,1 V·s/rad, duas fases, R_fase=2 Ω, R_carga=8 Ω, T=60 s.
- L = H/sinθ ≈ 5,75877 m.
- v_ref = L/T ≈ 0,0959795 m/s.
- F_0 = mg(sinθ-c_r cosθ) ≈ 9,06162 N.
- τ_req_gerador = η_t r_d F_0 / G ≈ 0,407773/G N·m.
- ω_gerador = G v_ref/r_d ≈ 1,91959 G rad/s.
- Hipótese elétrica explícita: duas fases independentes com FEM K_e ω, corrente I = K_e ω/(R_fase+R_carga) e torque total τ_em = 2 K_e I. Essa relação só é válida se a convenção de K_e e torque do código for consistente. Verificar unidade, fator de fase e constante de torque antes de usar.
- Nesse equivalente, τ_em ≈ 0,00383918 G N·m e a igualdade estacionária fornece G≈10,306.
- Para G≈10,306, estimam-se ω≈19,78 rad/s (189 rpm), E_fase≈1,978 V, I_fase≈0,198 A, P_AC≈0,626 W, E_AC≈37,57 J em 60 s de velocidade constante.
- Atenção: o resultado não inclui transientes, frenagem final, perdas variáveis, indutância, corrente/torque nominal, tensão mínima de retificação, limite térmico, conversor ou uma máquina real. A viabilidade não está demonstrada. É uma hipótese prioritária para verificação dinâmica.
- A mesma condição estacionária idealizada fornece a tabela exploratória abaixo. Não interpretar como simulação dinâmica, otimização ou resultado de desempenho validado.
Inclinação	Comprimento (m)	G de equilíbrio aproximado	Rotação (rpm)	P_AC (W)	E_AC em 60 s (J)
10°	5,7588	10,31	188,9	0,626	37,57
20°	2,9238	20,96	195,0	0,668	40,05
30°	2,0000	30,97	197,1	0,682	40,91
40°	1,5557	40,03	198,2	0,690	41,37


- O aumento de inclinação reduz o percurso e a perda por rolamento, mas, neste exercício, exige relações de transmissão progressivamente maiores para manter os mesmos 60 s. Esse compromisso entre ângulo, G e limites da máquina é uma pergunta central a ser verificada.
- Validar se a expressão F_carga = G τ/(η_t r_d) e a convenção de eficiência do E4 correspondem a essa derivação. Se não, corrigir a estimativa e explicar.
D. Implementar E6.4: gerador eletromagnético regulável
1. Criar regime C realmente distinto do E4 passivo, com dinâmica m dv/dt = F_0 - F_resistente_eletromagnetica(v,G,R_carga,...) e dx/dt=v, mais efeitos explicitamente escolhidos. Começar com carga resistiva ajustável; não usar torque ideal independente de corrente.
2. Tratar transmissão, corrente, FEM, torque, potência AC, cobre, rolamento e energia cinética como grandezas rastreáveis. Implementar limites de corrente, torque, velocidade, temperatura se houver parâmetros justificáveis; na ausência de dados, apresentar faixas paramétricas, não números comerciais inventados.
3. Testar G em torno de 1, 3, 5, 8, 10, 12, 15 e 20, refinando a região promissora. Testar θ=10°, 20°, 30°, 40° e posteriormente varredura 5°–60°. Investigar R_carga, K_e, r_d e c_r. Não combinar indiscriminadamente parâmetros de máquinas diferentes.
4. Resolver o problema de partida do repouso e de chegada com velocidade finita. Testar frenagem terminal: contabilizar separadamente energia recuperada, energia dissipada e energia cinética remanescente.
5. Verificar se há casos com tempo≥30 s, tempo≈60 s, E_AC≥30 J, P_AC_média≥0,5 W, sem impor resultados por construção. O critério de sucesso científico é identificar a região viável/inviável e as causas.
6. Após verificação, produzir gráficos temporais e mapas de calor de θ×G e θ×R_carga para tempo, energia AC, potência média, velocidade final, perdas e resíduo. Usar máscara visual para cenários inválidos, sem interpolá-los como se fossem válidos. Produzir Pareto energia × duração × percurso, indicando restrições.
7. Para comparação com a literatura, executar sensibilidade c_r=0,006, 0,020, 0,050 e identificar esses coeficientes como cenários inspirados em Qin et al. e Liu et al., não propriedades medidas do GravBat.
8. Exportar CSV, PNG/SVG, metadados completos de parâmetros, comandos de reprodução, testes e relatório docs/tcc/e6_3_4_resultados_e_validacao.md.
E. Critérios de aceite
- E1–E5 idênticos aos históricos e testes existentes preservados.
- Resíduo energético quantificado, convergência numérica documentada, tratamento consistente de estados e saturação.
- Regime C dinâmico genuíno, sem torque nem geração fictícios.
- Referências [1]–[18] sincronizadas e auditadas no repositório.
- Nenhum gráfico de otimização publicado antes de verificar física e balanço.
- Não fazer commit, push, merge ou deploy sem autorização.
Catálogo de DOI e links para sincronização
A numeração corresponde à versão atual do Google Docs. As referências [1]–[5] e [10]–[16] não apresentam DOI no documento de origem e devem permanecer assim até verificação, sem inventar identificadores.
Nº	Autor/ano	DOI	Fonte
[6]	Zhang et al. (2024)	10.19799/j.cnki.2095-4239.2023.0667	https://esst.cip.com.cn/EN/Y2024/V13/I3/924
[7]	Qin et al. (2023)	10.19799/j.cnki.2095-4239.2022.0634	https://esst.cip.com.cn/CN/10.19799/j.cnki.2095-4239.2022.0634
[8]	Morstyn et al. (2019)	10.1016/j.apenergy.2019.01.226	https://ora.ox.ac.uk/objects/uuid:0482b2fa-f51b-4276-a369-8892cb5095c4
[9]	Liu et al. (2024)	10.19799/j.cnki.2095-4239.2024.0243	https://esst.cip.com.cn/EN/abstract/abstract2758.shtml
[17]	Gao et al. (2025)	10.19799/j.cnki.2095-4239.2024.0652	https://esst.cip.com.cn/EN/10.19799/j.cnki.2095-4239.2024.0652
[18]	Wang et al. (2025)	10.19799/j.cnki.2095-4239.2024.0835	https://esst.cip.com.cn/EN/abstract/abstract3085.shtml


Dados bibliográficos do catálogo:
- [6] ZHANG, Jingye et al. Gravity energy storage technology based on slopes and mountains. Energy Storage Science and Technology, 13(3), 924–933, 2024.
- [7] QIN, Tingting et al. Study on factors influencing rail gravity energy storage system efficiency. Energy Storage Science and Technology, 12(3), 835–845, 2023.
- [8] MORSTYN, Thomas; CHILCOTT, Malcolm D.; MCCULLOCH, Martin. Gravity energy storage with suspended weights for abandoned mine shafts. Applied Energy, 239, 201–206, 2019.
- [9] LIU, Dameng et al. Multi-software collaborative modeling method for mechanical and electrical co-simulation of slope gravity energy storage systems. Energy Storage Science and Technology, 13(9), 3266–3276, 2024.
- [17] GAO, Tian et al. Energy efficiency analysis model and experimental verification of gravity energy storage system with gear box and chain transmission mechanisms. Energy Storage Science and Technology, 14(2), 688–698, 2025.
- [18] WANG, Qingshan et al. Energy efficiency analysis model and experimental verification of vertical gravity energy storage system based on belt drive. Energy Storage Science and Technology, 14(3), 1141–1149, 2025.
Padrão de autoria no corpo do TCC: Qin et al. (2023), Liu et al. (2024), Gao et al. (2025); manter [n] quando houver citação numérica. No catálogo bibliográfico, seguir ABNT com sobrenome e prenome do primeiro autor quando disponível.
Estado de acesso e sincronização
O Google Docs TCC II v2.1 foi atualizado com as 18 referências. A conexão GitHub consultada não lista um repositório GravBat entre os repositórios acessíveis. O diretório local do Cursor não pode ser lido ou editado por este ambiente. Logo, a presença dos novos DOI no Cursor ainda não foi confirmada e não deve ser declarada como concluída. Este arquivo serve como especificação explícita para sincronização local pelo Codex.