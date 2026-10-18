# E3 — Torque, potência e dinâmica

**Classificação:** CALCULADO. **Data:** 12/10/2026. **Referência:** modelo mecânico V0.4; núcleo P0 congelado.

## Pergunta

Como o torque resistente constante modifica aceleração, velocidade, tempo de descarga, energia extraída e potência média em um percurso fixo?

## Hipóteses e parâmetros

- massa m = 6 kg;
- comprimento L = 1,20 m;
- inclinação θ = 10°;
- coeficiente de rolamento c_r = 0,02;
- raio efetivo r_d = 0,05 m;
- relação G = 1;
- rendimento da transmissão η_t = 0,90;
- gravidade g = 9,81 m/s²;
- partida do repouso e torque constante;
- sem inércia rotacional, controle ativo ou conversão elétrica detalhada.

## Equações

F_0 = m g [sen(θ) − c_r cos(θ)]

F_carga = G τ /(η_t r_d)

a = (F_0 − F_carga)/m

Para a > 0 e percurso L, t = raiz(2L/a), v_f = a t. A grandeza E_entrada_trans = F_carga L é o trabalho absorvido na entrada da transmissão. O trabalho mecânico entregue no eixo de saída é E_eixo = eta_t E_entrada_trans, a perda na transmissão é E_perda_trans = (1 − eta_t) E_entrada_trans e a potência média no eixo é P_eixo_media = E_eixo/t.

O torque limite é τ_lim = η_t r_d F_0/G. Para os parâmetros acima, F_0 = 9.06162 N e τ_lim = 0.40777 N m. A previsão do modelo para máxima potência média é τ_otimo = (2/3)τ_lim = 0.27185 N m.

## Varredura de torque

| carga | τ (N m) | F_carga (N) | a (m/s²) | tempo (s) | v_final (m/s) | E_entrada_trans (J) | P_entrada_media (W) | resíduo balanço (J) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.00 τ_lim | 0.00000 | 0.0000 | 1.51027 | 1.261 | 1.9039 | 0.0000 | 0.0000 | 0.00e+0 |
| 0.10 τ_lim | 0.04078 | 0.9062 | 1.35924 | 1.329 | 1.8062 | 1.0874 | 0.8183 | 0.00e+0 |
| 0.30 τ_lim | 0.12233 | 2.7185 | 1.05719 | 1.507 | 1.5929 | 3.2622 | 2.1651 | -8.88e-16 |
| 0.67 τ_lim | 0.27185 | 6.0411 | 0.50342 | 2.183 | 1.0992 | 7.2493 | 3.3201 | 4.44e-16 |
| 0.90 τ_lim | 0.36700 | 8.1555 | 0.15103 | 3.986 | 0.6021 | 9.7865 | 2.4550 | -6.66e-16 |
| 0.99 τ_lim | 0.40369 | 8.9710 | 0.01510 | 12.606 | 0.1904 | 10.7652 | 0.8540 | -1.08e-15 |
| 1.00 τ_lim | 0.40777 | 9.0616 | 0.00000 | bloqueado | — | — | — | — |
| 1.10 τ_lim | 0.44855 | 9.9678 | -0.15103 | bloqueado | — | — | — | — |

A linha em τ_lim representa a condição limite: a força líquida é nula e a partida do repouso não produz descarga espontânea. Acima desse valor, o movimento é bloqueado. A tabela usa o trabalho na entrada da transmissão; a energia e a potência no eixo são menores por eta_t.

## Verificações analíticas

- Torque nulo produz energia extraída nula pela carga.
- Aumentar torque reduz a aceleração.
- Torque igual ou superior ao limite não deve ser tratado como descida.
- O ponto τ = 2/3 τ_lim foi incluído na varredura. Neste modelo, ele maximiza a potência média no eixo (e na entrada, por fator constante eta_t) sob percurso, parâmetros e torque constantes.
- Esse ponto não maximiza a energia extraída em uma descarga. O trabalho absorvido na entrada cresce com o torque enquanto há movimento, enquanto o tempo cresce fortemente próximo do limite.
- A afirmação de máximo é específica do V0.4 e não é generalizada para geradores reais ou cargas variáveis.
- O resíduo foi calculado por F_0 L − E_entrada_trans − 0,5 m v_f² e permanece próximo de zero; o balanço completo com energia potencial e rolamento é apresentado abaixo.

## Trajetórias representativas

- 0.10 τ_lim: a=1.3592 m/s², t=1.329 s, posição s(t)=0,5·a·t², v(t)=a·t.
- 0.67 τ_lim: a=0.5034 m/s², t=2.183 s, posição s(t)=0,5·a·t², v(t)=a·t.
- 0.99 τ_lim: a=0.0151 m/s², t=12.606 s, posição s(t)=0,5·a·t², v(t)=a·t.

A posição e a velocidade seguem s(t)=0,5 a t² e v(t)=a t até L. Essas trajetórias são mecânicas idealizadas; não constituem conversão elétrica.

## Balanço energético no torque ótimo

No ponto τ = 2/3 τ_lim, os valores independentes são:

- energia potencial: 12,2651 J;
- perda por rolamento: 1,3912 J;
- trabalho na entrada da transmissão: 7,2493 J;
- energia no eixo de saída: 6,5244 J;
- perda na transmissão: 0,7249 J;
- energia cinética final: 3,6246 J;
- potência média na entrada: 3,3201 W;
- potência média no eixo: 2,9881 W.

O balanço completo é:

E_g = E_rol + E_perda_trans + E_eixo + E_cinetica_final.

Numericamente: 12,2651 = 1,3912 + 0,7249 + 6,5244 + 3,6246 J, com diferença apenas de arredondamento. A energia potencial bruta m g H não deve ser confundida com a energia no eixo.

## Figuras essenciais

1. Potência média versus τ/τ_lim, destacando 2/3 τ_lim e a região bloqueada.
2. Posição e velocidade versus tempo para 0,10, 2/3 e 0,99 τ_lim.
3. Balanço entre trabalho disponível, energia da carga e energia cinética.

Todas devem ser identificadas como CALCULADO, com unidades e hipóteses acima.

## Limitações

Torque resistente constante; rendimento de transmissão assumido; ausência de inércia rotacional detalhada; ausência de controle ativo; ausência de caracterização experimental do gerador; ausência de conversão elétrica detalhada. E3 trata extração mecânica e não substitui E4.

