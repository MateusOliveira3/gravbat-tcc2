# V0.1/V0.2 — modelo mecânico

## Objetivo científico

Investigar como massa, inclinação, geometria e resistência ao rolamento determinam força, aceleração, tempo, velocidade e balanço de energia numa massa em plano inclinado.

## Modelo matemático

Laboratório: `H=L sen(theta)`. Terreno: `L=H/sen(theta)`. Forças: `N=mg cos(theta)`, `Fg=mg sen(theta)`, `Fr=c_r N`, `Fdisp=Fg-Fr`. Se `Fdisp>0`, `a=Fdisp/m`, `t=sqrt(2L/a)`, `s=at²/2`, `v=at`. Energias: `Ei=mgH`, `Ep=mg(H-s sen(theta))`, `K=mv²/2`, `Erol=Fr s`, e `residuo=Ei-(Ep+K+Erol)`.

Variáveis: `m` kg, `g` m/s², `theta` graus/rad, `L,H,s` m, forças N, `a` m/s², `t` s, `v` m/s e energias J.

## Hipóteses e implementação

Massa pontual, repouso inicial, rampa retilínea, grandezas constantes; sem arrasto, rotação, transmissão, gerador ou frenagem. A partida usa a aproximação `Fg-Fr>0`; isso não caracteriza atrito estático. `model/geometry.py`, `model/mechanics.py`, `model/energy.py` e `simulation/simulator.py` implementam a solução analítica em biblioteca padrão.

## Verificação e resultados

Os testes de geometria, forças, casos ideais, balanço durante/final, bloqueio, entradas inválidas e extremos passaram. Nos 12 cenários padrão, o maior resíduo foi da ordem de `2,13e-14 J` durante amostragem e `7,11e-15 J` ao final. São resultados CALCULADOS/SIMULADOS; não são validação EXPERIMENTAL.

## Limitações e próxima etapa

Faltam medições de massa/geometria/c_r, validação experimental e modelagem de transmissão, carga e gerador. A V0.2 é somente a interface do mesmo motor.
