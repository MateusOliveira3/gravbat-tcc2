# Balanço energético por transformações

## Correção de escopo

O TCC-1 descreve uma arquitetura com módulo mecânico, gerador de baixa rotação, retificação Schottky, barramento CC, estágio buck/boost, controle e carga. O modelo atual ainda não representava todas essas etapas separadamente. Esta documentação corrige essa pendência e impede que uma eficiência global esconda perdas distintas.

## Cadeia de energia

`E_potencial → E_mecânica → E_eixo → E_AC → E_CC → E_carga`

Para um ciclo, a forma geral será:

`E_carga = m g h · η_mecânica · η_transmissão · η_gerador · η_retificador · η_conversor · η_carga`

Cada fator deve ser independente e receber classificação própria. A eficiência global será calculada pelo produto apenas quando todas as etapas estiverem definidas.

## Estado atual

| Transformação | Estado atual | Classificação |
|---|---|---|
| Potencial → mecânica | energia potencial, cinética, rolamento | TEÓRICO/ANALÍTICO e CALCULADO |
| Mecânica → transmissão | perdas e eficiência `η_t` | HIPÓTESE configurável |
| Eixo → AC | FEM, resistência e potência equivalente | HIPÓTESE/CALCULADO |
| AC → CC | eficiência genérica do retificador | HIPÓTESE |
| CC → conversor/carga | ainda não separado | A DEFINIR |
| Recarga do ciclo | potência e eficiência prescritas | HIPÓTESE/CALCULADO |

## Auditoria do TCC-1

O TCC-1 registra cenários qualitativos otimista, realista e conservador e menciona perdas mecânicas, retificação, controle, aquecimento e desalinhamento. A faixa de 70–80% localizada no texto está associada a sistemas hidrelétricos de bombeamento, não ao motor de passo do GravBat. Não foi localizada uma fonte que permita atribuir diretamente `η_gerador = 70%` ou `η_eletrônica = 90%` ao protótipo.

Consequentemente, esses números não serão incorporados como fatos. Poderão ser usados somente como hipóteses de cenário, com rótulo explícito e análise de sensibilidade, até que datasheets ou medições forneçam valores específicos.

## Relação com o benchmark do TCC-1

O TCC-1 apresenta como resultado esperado que massas de aproximadamente 5–6 kg, alturas úteis de 1–1,2 m e potência de cerca de 0,5 W por aproximadamente 50 s seriam adequadas para uma validação didática. O trecho consultado apresenta esses números como cenário/resultado esperado, associado a cenários de eficiência, e não como medição experimental do GravBat. A derivação detalhada de cada eficiência parcial não está explicitada no trecho extraído.

Por isso, o benchmark será preservado como **REFERÊNCIA HISTÓRICA DO TCC-1**, mas sua reconstrução no TCC-2 deverá mostrar separadamente quais valores vêm de `mgh`, duração, potência requerida e eficiências assumidas. Ele não será usado como prova de desempenho do sistema real.

## Fontes de fundamentação

Chapman, Fitzgerald e Krause fundamentam a separação de perdas em máquinas elétricas: cobre, núcleo, mecânicas, dispersas e perdas no circuito. A documentação do fabricante deve fornecer os parâmetros do componente. Para retificador e conversor, serão usados datasheets do circuito selecionado; queda de diodo e perdas dependentes da corrente serão modeladas quando houver componente definido.

## Próxima implementação

Criar uma estrutura de balanço que receba eficiências por etapa e mostre, para cada cenário:

- energia de entrada;
- perda em cada transformação;
- energia de saída de cada etapa;
- eficiência parcial;
- eficiência global;
- origem/status do parâmetro.

Até essa implementação, qualquer eficiência global exibida deve ser entendida como hipótese de cenário e não como medição do GravBat.

O balanço por transformação pode ser exportado em CSV com entrada, saída, perda, eficiência e status de cada etapa. Esse arquivo é a tabela de auditoria energética do cenário e pode ser usado diretamente como base para tabelas do TCC.
