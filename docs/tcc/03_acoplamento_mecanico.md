# V0.4 — acoplamento com carga mecânica genérica

## Objetivo científico

Quantificar como um torque constante resistente no eixo de saída altera aceleração, tempo, velocidade, RPM e energia durante a descida.

## Modelo matemático

Para `tau_carga >= 0`, `0<eta_t<=1`, `r_d>0`, `G>0`: `tau_tambor=G tau_carga/eta_t`; `F_carga=G tau_carga/(eta_t r_d)`; `Fliquida=Fg-Fr-Fcarga`; `a=Fliquida/m`. Se `Fliquida<=0`, status `NAO_DESCE_COM_CARGA`, sem percurso, tempo ou dissipação fictícia.

O limite teórico é `tau_limite=(eta_t r_d/G) (Fg-Fr)` quando `Fg-Fr>0`. Para movimento constante: `s=at²/2`, `v=at`; `theta_saida=G s/r_d`; `Ecarga=tau_carga theta_saida`; `Eentrada=Ecarga/eta_t`; `Eperda_trans=Eentrada-Ecarga`. O balanço é `Ei=Ep+K+Erol+Eentrada`; o termo de entrada contém carga e perda. Potências: `Pcarga=tau_carga omega_saida` e `Pentrada=Pcarga/eta_t`.

## Implementação

`model/coupling.py` reutiliza a geometria e forças do núcleo, mantendo aceleração analítica constante. O módulo retorna estados com energias, potências, resíduos e RPM. `app.py` apresenta cards, comparação sem/com carga, potência mecânica, balanço final e controles de ativação, torque e eficiência.

## Verificação

Os 29 testes anteriores foram preservados e 5 novos testes foram adicionados, totalizando 34. Eles verificam torque zero, força/torque refletidos, redução de aceleração, bloqueio, entradas inválidas, conservação para `eta=1`, perda não negativa, `Ecarga`, `Eentrada=Fcarga s`, potência média, torque zero e resíduos.

## Resultados e interpretação

Com `tau=0`, a trajetória coincide com V0.3. Aumentar torque reduz aceleração; acima do limite resulta em `NAO_DESCE_COM_CARGA`. A potência mecânica na carga pode ter máximo intermediário na varredura, mas qualquer máximo é apenas RESULTADO SIMULADO do modelo V0.4, não ótimo do sistema real nem potência elétrica.

## Hipóteses e limitações

Torque constante, `G`, `r_d` e `eta_t` constantes, sem inércia rotacional, escorregamento, atrito estático caracterizado ou gerador. A carga é abstrata e não deve ser chamada de torque de gerador. O próximo passo pode substituir torque constante por uma carga dependente de velocidade, antes de qualquer modelo eletromagnético.

## Verificação analítica do ponto de máxima potência mecânica

Durante uma descida DESCE_COM_CARGA, defina `F0=Fg-Fr` e `tau_lim=(eta_t r_d/G)F0`. Então `a=(F0/m)(1-tau/tau_lim)` e `t_f=sqrt(2L/a)`. Como `E_carga=tau G L/r_d`, a potência média é proporcional a `tau sqrt(1-tau/tau_lim)`. Com `x=tau/tau_lim`, `f(x)=x sqrt(1-x)` e `f'(x)=sqrt(1-x)-x/[2 sqrt(1-x)]`. Igualando a zero: `2(1-x)-x=0`, logo `x=2/3`.

A auditoria reproduziu a divergência anterior. O relatório antigo usou `tau_lim=0,4530808 N·m`, calculado com `eta=1`, mas a potência foi calculada com `eta=0,9`; o limite efetivo na mesma simulação era `0,4077727 N·m`. Além disso, os cinco pontos testados eram `0`, `0,25`, `0,5`, `0,75` e `1,01` do limite incorreto, portanto não podiam localizar o máximo com precisão. O valor `0,22654 N·m` era exatamente `0,5` do limite com `eta=1`, não o ótimo analítico da configuração usada.

A implementação foi corrigida com `varrer_torque`, que calcula o limite usando o mesmo `eta_t` da simulação e usa 2.001 pontos uniformes até `1,01 tau_lim`. O código não impõe `2/3`; o teste independente compara o máximo encontrado com `2/3 tau_lim` dentro de 0,2%. Para `eta=0,9`, `tau_lim=0,4077727 N·m` e `tau_otimo=0,2718485 N·m`. A potência média simulada nesse ponto é aproximadamente `2,98813 W`.

Nos pontos de verificação, `P_media=E_carga/t_f` e `P_final=2 P_media` em toda descida constante a partir do repouso. Nos limites, `tau→0` implica energia e potência médias nulas; `tau→tau_lim` implica aceleração, velocidade final e potência média tendendo a zero. Esses resultados são TEÓRICO/ANALÍTICOS e CALCULADOS/SIMULADOS, não experimentais.
