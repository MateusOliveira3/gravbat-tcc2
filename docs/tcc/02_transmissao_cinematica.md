# V0.3 — transmissão cinemática sem carga

## Objetivo científico

Determinar a rotação resultante no tambor e no eixo de saída a partir da trajetória mecânica, antes de acoplar carga eletromagnética ou mecânica.

## Equações

Com cabo sem escorregamento: `omega_d=v/r_d`, `RPM_d=omega_d 60/(2 pi)`. Pela convenção `G=omega_saida/omega_d`: `omega_saida=G omega_d`, `RPM_saida=G RPM_d`. `r_d` é m e `G` é adimensional; velocidades angulares são rad/s e rotações RPM.

Para potência prescrita externa: `P_in=tau_in omega_in`, `P_out=eta P_in`, `tau_out=eta tau_in/G` para `omega_in != 0`. A função isolada não injeta torque na massa.

## Hipóteses, implementação e verificação

`r_d` e `G` são HIPÓTESES configuráveis; não há inércia, escorregamento ou carga. `model/transmission.py` implementa as conversões. Os testes verificam `v=r omega`, rad/s-RPM, `G=1`, validações, independência da trajetória e conservação/redução de potência prescrita. V0.3 é CINEMÁTICA CALCULADA/SIMULADA, sem torque extraível.

## Interpretação e limitações

Alterar `r_d` ou `G` muda RPM, mas não aceleração, tempo ou velocidade enquanto não houver torque resistente. Não se pode chamar a RPM de ideal para um gerador não caracterizado. A etapa seguinte deve introduzir uma carga mecânica genérica.
