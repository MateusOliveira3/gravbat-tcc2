# Implementação do balanço energético por transformações

O módulo `model/energy_chain.py` implementa seis etapas explícitas: mecânica, transmissão, gerador, retificador, conversor e carga. Para cada etapa são armazenadas energia de entrada, energia de saída, perda, eficiência e status.

O cálculo é sequencial:

`E_saida,k = η_k E_entrada,k`

`E_perda,k = E_entrada,k − E_saida,k`

A eficiência global é o produto das eficiências parciais, mas a tabela preserva a perda de cada transformação. Os valores atuais são parâmetros de cenário e estão classificados como **HIPÓTESE** até que datasheets ou medições estejam disponíveis.
### Correção da origem da energia no ciclo V0.6

Quando a integração eletromecânica dinâmica está disponível, a energia usada
no ciclo descida–subida passa a ser a energia AC acumulada pela simulação
(`energia_acumulada_J`). Isso evita tratar a energia mecânica da carga genérica
V0.4 como se fosse energia elétrica gerada. A referência V0.4 permanece
disponível apenas quando não há trajetória eletromecânica válida, identificada
explicitamente como `CALCULADO_V04_MECANICO`.

Classificação: a energia integrada é **SIMULADO**; a referência V0.4 é
**CALCULADO**. Nenhuma das duas constitui validação experimental.
