# Registro de decisões de projeto — GravBat TCC-2

Registro cronológico objetivo. Resultados marcados como simulados não são experimentais.

1. O produto principal passou de protótipo físico para modelo computacional. O protótipo físico permanece como possível validação complementar.
2. Laboratório usa comprimento `L` fixo; Terreno usa desnível `H` fixo.
3. Foi abandonada a interpretação de escala global 1:10.000 como equivalência física automática.
4. `c_r` é hipótese configurável de resistência equivalente em movimento, não dado experimental.
5. `0,5 W` é referência histórica do TCC-1, não resultado do modelo; 50/60 s não é requisito fixo.
6. O motor físico foi separado da interface.
7. V0.1: modelo mecânico analítico com balanço energético e bloqueio explícito.
8. V0.2: dashboard mecânico com Plotly/Streamlit; sem gerador ou eletrônica.
9. V0.3: transmissão cinemática sem carga. Não se extrai torque da trajetória para evitar dupla contagem de energia.
10. V0.4: carga mecânica genérica de torque constante acoplada antes do gerador. O torque da carga modifica a trajetória.
11. A documentação científica passa a ser mantida em `docs/tcc/` a cada fase.
12. A V0.4 foi submetida a verificação analítica independente do ponto de máxima potência mecânica antes de qualquer introdução de gerador.
13. Fase 5A: a V0.4 foi encerrada sem alterações; foi definida uma investigação documental prévia ao gerador. A V0.5 não será implementada até identificar o motor físico ou obter parâmetros rastreáveis.
14. O modelo eletromecânico recomendado é equivalente por fase, com FEM dependente de velocidade e posição, resistência e indutância quando justificadas. Gerador, retificador e eletrônica permanecem subsistemas distintos.
15. Direcionamento científico do TCC-2: priorizar um núcleo computacional verificável e escalável. O simulador deverá permitir explorar diferentes massas, desníveis, inclinações, velocidades, eficiências, ciclos e demandas, preservando a rastreabilidade das hipóteses.
16. A aplicação futura a casas, cidades, terrenos reais e episódios de curtailment será tratada como camada de cenários e produto potencial. O TCC não afirmará que o armazenamento gravitacional elimina curtailment; investigará requisitos, potencial e limitações sob dados e hipóteses explícitos.
17. A maquete física passa a ser validação complementar possível, e não o eixo principal do trabalho. O foco permanece no modelo mecânico, eletromecânico, nos ciclos de operação e na análise de escalabilidade.
18. A redação do TCC-2 será construída junto com o desenvolvimento. Cada fase implementada deverá registrar objetivo científico, equações utilizadas, variáveis e unidades, hipóteses, origem dos parâmetros, implementação, verificação, resultados, interpretação, limitações e próxima etapa.
19. O TCC-1 permanece disponível em `work/tcc1_extraido.txt` como fonte histórica e base de continuidade. Referências reutilizadas serão auditadas e classificadas como mantidas, corrigidas, substituídas ou descartadas; nenhuma fonte será usada para sustentar afirmação que não demonstre.
20. A geometria preliminar do cabo passa a registrar tipo, diâmetro, núcleo do tambor e comprimento disponível. O enrolamento multicamada completo permanece fora do modelo até haver dados de largura, tensão e distribuição das camadas.
21. O cabo e o enrolamento ficam em segundo plano no núcleo científico. A próxima camada prioriza dimensionamento energético e de potência, mantendo a geometria do cabo como parâmetro preliminar configurável.
22. Motivação contextual do projeto: o GravBat investiga uma alternativa de flexibilidade e armazenamento para sistemas elétricos com expansão de fontes renováveis variáveis e possíveis episódios de curtailment. Essa motivação não constitui previsão determinística nem permite afirmar que a tecnologia eliminará curtailment; cenários futuros serão baseados em fontes institucionais e hipóteses explícitas.
23. O benchmark histórico de 5–6 kg, 1–1,2 m e aproximadamente 0,5 W por 50 s foi localizado no TCC-1 como resultado esperado/cenário didático. A derivação das eficiências parciais não está explicitada no trecho extraído; no TCC-2 ele será reconstruído com rastreabilidade e mantido como referência, não como medição.
24. Foi cadastrado o FAULHABER DM52100S como candidato real de datasheet, sem tratá-lo como componente do protótipo. A partir de 100 passos/revolução e 2,2 V/(1000 passos/s), foi derivado `K_e = 0,0350 V·s/rad`; o valor permanece sujeito a confirmação experimental.

## Classificação

Equações são TEÓRICO/ANALÍTICAS; saídas das funções são CALCULADAS; trajetórias amostradas e varreduras são SIMULADAS; não há resultado EXPERIMENTAL nesta entrega. `g`, `c_r`, geometrias padrão, raio do tambor e `G` são HIPÓTESES/entradas adotadas; nenhuma constante do gerador foi inventada.
25. A V0.9 foi consolidada como núcleo científico reproduzível, com explorador de aplicações, exportação JSON/CSV e auditoria de 65 testes. A V1.0 dependerá de parâmetros reais rastreáveis e revisão final das figuras.
26. A arquitetura eletromecânica adotada para o estudo de bancada usa o motor de passo como gerador, ponte de diodos para retificação e carga/barramento CC para produzir torque resistente. A ponte não injeta energia mecânica: o efeito de frenagem vem da corrente gerada. A referência de aproximadamente 2 cm/s é tratada como condição de operação do modelo de bancada, não como resultado experimental confirmado.
27. Caixa de engrenagens permanece como recurso cinemático para adequar velocidade e torque. Ela não cria energia nem substitui o balanço de perdas. O controle ativo posterior poderá regular a carga no barramento, mas o freio eletromagnético básico não requer servo motor dedicado.

## 12/10/2026 — Rodada de Polish científico

O núcleo computacional foi congelado após o fechamento P0. A rodada seguinte foi restrita a planejamento científico: pergunta, objetivos, matriz de experimentos, figuras, redação e simplificação de escopo. Nenhuma funcionalidade ou parâmetro foi alterado. A suíte registrou 74 testes encontrados, 73 aprovados e um erro ambiental de limpeza temporária no Windows; esse estado não é chamado de aprovação integral.
