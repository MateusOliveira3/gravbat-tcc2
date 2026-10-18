# Roadmap do GravBat — TCC-2

## Objetivo do trabalho

Desenvolver e verificar um modelo computacional escalável de armazenamento gravitacional por massa móvel, relacionando configuração mecânica, transmissão, conversão eletromecânica, ciclos de operação, energia, potência e perdas.

O produto do TCC é um **núcleo científico reproduzível com dashboard**, não um projeto executivo de uma instalação real. Aplicações a casas, cidades, ferrovias e curtailment serão cenários de investigação e não conclusões automáticas de viabilidade.

## Motivação contextual

O GravBat foi concebido para investigar uma alternativa de armazenamento e flexibilidade diante da expansão de fontes renováveis variáveis e de possíveis restrições futuras de aproveitamento da geração. A relação com curtailment será estudada por cenários e fontes institucionais, sem tratar sua ocorrência como certeza universal ou afirmar que o armazenamento resolve todas as suas causas.

## Fases concluídas

### V0.1 — Modelo mecânico

**Entregue:** equações de força, aceleração, trajetória e energia; distinção entre Laboratório `L` fixo e Terreno `H` fixo; testes e documentação.

**Critério de encerramento:** balanço energético e casos limite verificados.

### V0.2 — Dashboard mecânico

**Entregue:** interface Streamlit, gráficos Plotly, entradas configuráveis e interpretação do cenário.

**Critério de encerramento:** execução reproduzível e verificação automatizada do dashboard.

### V0.3 — Transmissão cinemática

**Entregue:** relação entre velocidade linear, tambor, relação `G` e velocidade angular de saída, sem carga.

**Decisão:** não extrair torque da trajetória V0.3 para evitar dupla contagem de energia.

### V0.4 — Acoplamento mecânico

**Entregue:** torque de carga genérico, torque refletido, força resistente, alteração da trajetória, perdas da transmissão e verificação analítico-numérica do ponto de máxima potência mecânica.

**Critério de encerramento:** auditoria aprovada; V0.4 não deve ser alterada sem motivo documentado.

### Fase 5A — Definição eletromecânica

**Entregue:** comparação entre gerador CC simplificado e motor de passo multifásico; separação entre gerador, retificador e eletrônica; tabela de parâmetros; auditoria do TCC-1 e da bibliografia.

**Decisão:** usar futuramente um modelo equivalente por fase, sem inventar parâmetros do motor físico.

## Fases de implementação do TCC-2

### V0.5 — Acoplamento eletromecânico mínimo

**Objetivo:** verificar a cadeia `ω_saida → FEM → corrente/carga → torque eletromagnético → torque refletido → dinâmica da massa`.

**Escopo:** modelo por fase de ordem reduzida, resistência, FEM parametrizada, carga elétrica prescrita e retificação ideal ou explicitamente simplificada.

**Não incluir:** controle PWM avançado, saturação, perdas térmicas detalhadas ou identificação automática.

**Critério de encerramento:** conservação de potência, sentido correto do torque resistente, comportamento limite sem carga e documentação completa.

**Primeira entrega:** integrador numérico com torque dependente da velocidade e teste de convergência aproximada contra a trajetória analítica sem carga elétrica.

**Ampliação:** o dashboard exibe velocidade, torque eletromagnético e potência AC ao longo do tempo na área de verificação.

### V0.6 — Ciclo de descida e subida

**Objetivo:** simular armazenamento como operação, e não somente como descida isolada.

**Escopo:** descida, energia elétrica gerada, subida com potência externa prescrita, energia consumida na recarga, perdas e saldo líquido por ciclo.

**Critério de encerramento:** tabela e gráficos temporais reproduzíveis; distinção entre descarga, recarga e ciclo completo.

**Primeira entrega:** balanço energético com potência de subida prescrita, eficiência de recarga, energia gerada na descida, energia consumida na subida, saldo líquido e tempo de ciclo. Controle detalhado da subida permanece fora desta entrega.

**Geometria complementar:** tipo e diâmetro do cabo, diâmetro do núcleo do tambor e voltas equivalentes na primeira camada são registrados como entradas preliminares. O raio efetivo continua separado até haver dados de enrolamento suficientes.

### V0.7 — Dimensionamento por cenário

**Objetivo:** responder a demandas genéricas de energia e potência.

**Escopo:** entrada de energia requerida, potência máxima, duração, altura, massa, eficiência e número de módulos.

**Critério de encerramento:** o sistema informa requisitos energéticos e de potência, além dos parâmetros ausentes e das limitações.

**Primeira entrega:** função de ordem de grandeza para massa total a partir de energia útil, altura e eficiência, com potência média e número estimado de módulos quando a massa modular é informada.

### V0.8 — Comparação de terrenos e escalabilidade

**Objetivo:** demonstrar que o modelo escala de forma flexível.

**Escopo:** comparação de alturas, comprimentos, inclinações, massas, velocidades e módulos em paralelo; cenários sintéticos e, se disponíveis, dados públicos documentados.

**Critério de encerramento:** tabelas e figuras exportáveis, com parâmetros do cenário e versão do modelo.

### V0.9 — Cenário energético contextualizado

**Objetivo:** investigar ordem de grandeza da aplicação a excedentes ou curtailment.

**Escopo:** usar dados institucionais rastreáveis como entrada de cenário, distinguindo causas energéticas, restrições de rede/transmissão e confiabilidade.

**Limite:** não afirmar que o armazenamento elimina curtailment nem transferir resultados simulados para uma instalação real.

### V1.0 — Consolidação do TCC

**Entregue:** versão congelada do código, documentação científica, bibliografia auditada, resultados principais, figuras reproduzíveis, limitações e discussão.

**Critério de encerramento:** outro usuário consegue instalar, executar, reproduzir os cenários principais e identificar a origem de cada parâmetro.

**Primeira consolidação:** o dashboard passou a reunir comparação de cenários, documentação de limites e preparação para verificação final do conjunto.

**Interface:** a resposta principal será organizada em torno do cenário, configuração estimada, desempenho do ciclo e limitações. Gráficos de diagnóstico permanecem na área de verificação.

## Evoluções posteriores ao TCC

Ficam como possibilidades futuras: interface em linguagem natural, mapas e perfis reais de terreno, otimização automática, controle avançado, modelo térmico, protótipo físico completo, integração com dados em tempo real e produto de dimensionamento comercial.

## Regra de documentação por fase

Antes de encerrar cada fase, atualizar a documentação correspondente com objetivo científico, modelo matemático, hipóteses, implementação, verificação, resultados, interpretação, limitações, decisões e próxima etapa. Toda saída deve ser classificada como **TEÓRICO/ANALÍTICO**, **CALCULADO**, **SIMULADO**, **EXPERIMENTAL**, **HIPÓTESE**, **LITERATURA** ou **DATASHEET**.
