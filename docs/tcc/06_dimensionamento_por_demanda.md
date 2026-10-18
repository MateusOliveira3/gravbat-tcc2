# V0.7 — Dimensionamento preliminar por demanda

## Objetivo

Relacionar uma demanda de energia e potência a uma estimativa de massa gravitacional, altura e eficiência global.

## Modelo

`E_util = η m g h`

`m = E_util/(η g h)`

`P_media = E_util/t_descarga`

As entradas são energia útil [kWh], potência máxima [kW], altura [m], eficiência [adimensional] e duração [h]. A massa é calculada em kg. A potência média é uma verificação da duração solicitada; potência máxima ainda precisa ser atendida pelo número de módulos e pela dinâmica eletromecânica.

## Limitações

Esta versão é um dimensionamento de ordem de grandeza. Não calcula área, estrutura, custo, disponibilidade de terreno, curva de carga, rampas de potência ou projeto executivo. Os resultados são **CALCULADOS** sob parâmetros de **HIPÓTESE** ou **LITERATURA** quando fornecidos pelo usuário.
### Acoplamento ao ciclo simulado

Quando existe um ciclo descida–subida completo, a interface calcula uma
estimativa adicional por módulo: energia elétrica produzida por ciclo,
quantidade equivalente por energia, quantidade equivalente por potência e o
maior desses valores arredondado para cima. A classificação é **CALCULADO** a
partir de uma trajetória **SIMULADA**. O resultado não inclui redundância,
disponibilidade, despacho, limites térmicos, perdas civis ou dimensionamento
executivo.


### Comparação paramétrica V0.8

A comparação de cenários apresenta a mesma demanda sob três alturas e duas variações de eficiência. A massa calculada segue `m = E/(η g h)`, enquanto a potência média segue `P = E/t`. As variações são **CALCULADAS** para análise de sensibilidade; não representam levantamento topográfico, catálogo ou medição.
