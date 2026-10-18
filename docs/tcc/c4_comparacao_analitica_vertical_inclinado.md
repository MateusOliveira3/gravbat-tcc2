# C4 — Comparação analítica entre arquiteturas vertical e inclinada

## Escopo

A comparação abaixo usa somente deduções analíticas e resultados já registrados em E1–E5. Ela não representa uma simulação adicional nem assume que perdas verticais e inclinadas sejam iguais.

| Condição de referência | Vertical idealizado | Plano inclinado | Conclusão permitida |
|---|---|---|---|
| Mesma massa e mesmo desnível $H$ | $E_g=m g H$ | $E_g=m g H$ | O potencial gravitacional ideal é igual. Eficiências podem diferir. |
| Mesma massa e mesma velocidade linear | $P_g=m g v$ em descida vertical ideal | $P_g=m g v\sin\theta$ na direção do movimento | Para a mesma velocidade ao longo do movimento, a componente motriz depende de $\theta$. Não se compara potência elétrica sem o mesmo controle e perdas. |
| Mesma massa, desnível e duração | Percurso vertical próximo de $H$ | $L=H/\sin\theta$ e velocidade média no trilho $L/t$ | A rampa exige maior deslocamento quando $\theta$ diminui; a energia potencial continua igual. |
| Perdas por rolamento | Não aplicadas automaticamente ao modelo vertical | $E_{rol}=c_r m g H\cot\theta$ para $H$ fixo | Sob a hipótese de E2, rampas rasas acumulam mais trabalho de rolamento. O valor de $c_r$ é uma hipótese do modelo. |
| Força motriz | Aproximadamente $m g$ no eixo vertical ideal | $F_g=m g\sin\theta$ e $F_{rol}=c_r m g\cos\theta$ | O movimento inclinado requer $\tan\theta>c_r$ para força líquida positiva no modelo. |
| Transmissão e torque | Dependem do tambor, cabo e relação | Dependem adicionalmente da força ao longo do trilho e do raio efetivo | Não há equivalência automática entre torque, velocidade ou potência. |

### Interpretação quantitativa

E2 documenta, para $H=1$ m, que $E_g$ permanece 58,86 J enquanto o comprimento cresce de 2,00 m a 30° para 28,65 m a 2°. Com $c_r=0,02$, o limiar analítico é $\theta>\arctan(0,02)\approx1,146°$. Esses números são calculados para os parâmetros de E2 e não constituem projeto estrutural.

No caso A, com $L$ fixo, $H=L\sin\theta$ e a energia varia com o ângulo. No caso B, com $H$ fixo, a energia é constante e a perda de rolamento aumenta conforme $\cot\theta$. Portanto, aumentar a inclinação pode reduzir comprimento e perdas de rolamento sob a hipótese adotada, mas altera força, torque, segurança, ocupação e requisitos estruturais.

A condição de mesma duração não permite concluir qual arquitetura fornece maior energia elétrica: a potência depende de controle, transmissão, velocidade, carga e conversão. O E3 usa torque constante e o E4 usa um acoplamento eletromecânico dependente da velocidade; suas trajetórias não devem ser comparadas como se fossem um único experimento.

### Lacunas

Não há dados suficientes para comparar massas estruturais, inércia rotacional, frenagem de emergência, fundações, ocupação territorial, custo ou disponibilidade de locais. Também não há base para atribuir ao sistema vertical a mesma resistência de rolamento do plano inclinado.
