# Cenário demonstrativo baseado no benchmark do TCC-1

## Objetivo

Executar o conjunto do dashboard com um cenário histórico do TCC-1, verificando a continuidade entre o trabalho anterior e o núcleo V1.0.

## Entradas históricas

- massa de referência: 5–6 kg;
- altura útil: 1–1,2 m;
- potência de referência: aproximadamente 0,5 W;
- duração histórica: aproximadamente 50 s.

Esses valores aparecem no TCC-1 como cenário/resultado esperado para validação didática. Não são medições confirmadas do protótipo e não definem um motor real.

## Procedimento de reprodução

1. Selecionar Laboratório e `L = 1,20 m`.
2. Usar massa de referência entre 5 e 6 kg.
3. Definir a inclinação do cenário.
4. Selecionar o modelo hipotético V0.5.
5. Observar a trajetória mecânica e a FEM calculada.
6. Definir a carga resistiva como hipótese de bancada.
7. Consultar a integração dinâmica na área de verificação.
8. Preencher as eficiências parciais somente quando a origem estiver definida.
9. Comparar a energia útil e o tempo com a referência histórica de 0,5 W por aproximadamente 50 s.

## Interpretação permitida

O cenário verifica a continuidade computacional entre TCC-1 e TCC-2 e mostra como as hipóteses afetam a ordem de grandeza. Ele não comprova que o sistema físico entrega 0,5 W e não valida o motor, o cabo ou o circuito eletrônico.
