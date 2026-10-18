# Interface de resultados e visão futura do produto

## Objetivo

O dashboard deve responder a uma pergunta de dimensionamento preliminar, como:

- “Que configuração poderia atender uma casa com esta demanda?”
- “Que ordem de grandeza seria necessária para uma comunidade?”
- “Que configuração seria possível neste terreno?”

A resposta deve ser uma **estimativa calculada e simulada**, com hipóteses e parâmetros visíveis. Não deve ser apresentada como projeto executivo.

## Motivação do estudo

O projeto nasceu da necessidade de investigar alternativas de flexibilidade para sistemas elétricos com maior participação de fontes renováveis variáveis. Nesse contexto, restrições de rede, limitações operacionais e desequilíbrios temporais entre geração e demanda podem produzir situações de energia disponível que não é aproveitada. O dashboard permite estudar, sob cenários documentados, se uma bateria gravitacional poderia absorver parte dessa energia e devolvê-la posteriormente.

Essa motivação é contextual, não uma conclusão antecipada. O modelo não presume que o armazenamento elimine curtailment e deve distinguir causas energéticas, limitações de transmissão/rede e requisitos de confiabilidade.

## O que a resposta principal deve mostrar

1. **Pergunta e cenário interpretado** — demanda de energia, potência, duração, altura, inclinação e terreno.
2. **Configuração estimada** — massa, desnível, comprimento, número de módulos, velocidade e relação de transmissão.
3. **Desempenho do ciclo** — energia gerada, energia de recarga, saldo líquido, potência média, potência máxima e tempo de ciclo.
4. **Trajetória do carrinho** — posição, velocidade e potência ao longo da descida e subida.
5. **Conclusão condicionada** — o que o modelo permite afirmar e quais dados ainda faltam.

## O que deve ficar em verificação técnica

- comparação sem carga versus carga;
- comparação V0.4 versus V0.5;
- varredura de torque;
- varredura de inclinação;
- relação `G` versus RPM;
- resíduos energéticos;
- convergência do integrador;
- tabelas completas de estados;
- parâmetros não arredondados.

Esses gráficos são importantes para o professor e para a auditoria, mas não precisam ocupar a resposta principal do usuário.

## Gráficos prioritários

### Resultado principal

- posição e velocidade no tempo;
- potência elétrica e energia acumulada;
- energia gerada, energia consumida na subida e saldo líquido;
- comparação entre demanda e capacidade estimada.

### Verificação

- forças no plano;
- energia potencial, cinética e perdas;
- torque e velocidade;
- comparação analítico versus numérico;
- sensibilidade à altura, massa e eficiência.

## Arredondamento

A interface usa valores compactos para facilitar leitura. Tabelas técnicas, exportações e relatórios devem preservar precisão suficiente para reprodução. O arredondamento visual não altera os cálculos internos.

## Evolução prevista

O produto futuro poderá receber uma pergunta em linguagem natural, transformar a pergunta em entradas explícitas, executar cenários e apresentar uma configuração possível. O TCC demonstrará o núcleo científico que torna essa evolução possível; não precisa implementar uma inteligência artificial completa nem um projeto executivo automático.
### Resposta operacional do ciclo

A interface apresenta, quando a integração dinâmica é válida, energia elétrica
na descida, potência média, potência de pico, energia requerida na subida,
saldo líquido e eficiência do ciclo. Esses valores são classificados como
**CALCULADO** ou **SIMULADO** conforme sua origem e permanecem acompanhados de
hipóteses de carga, eficiência e potência de subida. A interface não os chama
de validação nem de projeto executivo.


### Exportação reproduzível

Cada cenário pode ser exportado em JSON, preservando a estrutura completa, ou em CSV, com uma linha por parâmetro e sua classificação. Os arquivos são artefatos **CALCULADOS/SIMULADOS** da execução e registram as hipóteses usadas no momento da análise.

Os relatórios exportados registram o identificador, nome, status, origem e observação do motor selecionado. Dessa forma, a rastreabilidade do resultado permanece preservada mesmo fora da interface.

### Visualização operacional compacta

O modo compacto apresenta um esquema didático da rampa, da massa e da carga elétrica. Um controle de posição percorre a trajetória amostrada e atualiza a posição do bloco, a energia potencial restante e a potência mecânica instantânea. A lâmpada representa qualitativamente a intensidade da potência; ela não é um modelo elétrico adicional nem uma validação experimental.

O modo compacto inclui o botão `Executar descida`. Ele percorre os estados calculados e atualiza o esquema da rampa, posição, energia restante e potência instantânea. A animação é uma reprodução visual da trajetória simulada, não um novo integrador nem uma validação experimental.
