# Síntese científica dos experimentos E1–E5

## E1 — Energia potencial gravitacional

**Pergunta:** como massa e desnível determinam a energia disponível?

**Método e classificação:** cálculo direto de E_g = m g H, com g=9,81 m/s². A hipótese é um campo gravitacional uniforme e a grandeza principal não inclui eficiência.

**Resultados:** 1.000 kg a 2 m fornecem 19.620 J (5,450 Wh); 1.000 kg a 800 m fornecem 2,180 kWh. A energia cresce linearmente com massa e altura.

**Interpretação:** E1 define a escala ideal de armazenamento. Energia potencial não é energia elétrica entregue.

**Conclusões permitidas:** massa e desnível são determinantes da capacidade ideal. **Não sustenta:** potência, autonomia, eficiência real, viabilidade comercial ou desempenho de rede.

## E2 — Geometria e perdas

**Pergunta:** como a inclinação altera comprimento, forças e rolamento?

**Método e classificação:** cálculo paramétrico com m=6 kg, c_r=0,02, L=1,20 m ou H=1,00 m. Foram usadas H=L sen(theta), força gravitacional e trabalho de rolamento. CALCULADO.

**Resultados:** com H fixo, E_g=58,86 J em todos os ângulos; a 2° o comprimento é 28,65 m e a 30° é 2,00 m. O limiar de força líquida é theta>1,146°.

**Interpretação:** inclinação é compromisso geométrico e de perdas, não fonte adicional de energia.

**Não sustenta:** dimensionamento estrutural, segurança ou eficiência elétrica.

## E3 — Torque, potência e dinâmica

**Pergunta:** como torque constante afeta descarga mecânica?

**Método e classificação:** modelo V0.4, partida do repouso, torque constante, percurso fixo. m=6 kg, L=1,20 m, theta=10°, eta_t=0,90. CALCULADO.

**Resultados:** torque limite 0,40777 N m; 2/3 do limite maximiza potência média no modelo. No ponto ótimo, energia na entrada da transmissão é 7,2493 J, energia no eixo 6,5244 J e potência média no eixo 2,9881 W.

**Interpretação:** potência média ótima não é energia total máxima; perto do bloqueio o tempo cresce fortemente.

**Não sustenta:** comportamento de motor real, controle ou operação contínua.

## E4 — Conversão eletromecânica

**Pergunta:** como carga elétrica e parâmetros equivalentes influenciam extração?

**Método e classificação:** integração do modelo equivalente com K_e=0,1, R_fase=2 ohm, duas fases e retificador eta=0,90, todos hipotéticos. SIMULADO/CALCULADO.

**Resultados:** no caso de 8 ohm, E_em=0,5958 J, E_carga AC=0,4766 J, perda de cobre=0,1192 J e energia CC estimada=0,4290 J. A convergência temporal foi registrada para 0,001, 0,0005 e 0,00025 s. A varredura de 100 ohm foi corrigida para E_em=0,05965896 J = E_carga 0,05848918 J + E_cobre 0,00116978 J.

**Interpretação:** carga, velocidade e perdas estão acopladas. Energia cinética final não é energia recuperada.

**Não sustenta:** eficiência universal, caracterização de gerador ou validação experimental.

## E5 — Escala e ciclo

**Pergunta:** como módulos, altura e eficiências condicionam o ciclo?

**Método e classificação:** cálculos de E=m g H, eficiências paramétricas, soma ideal de módulos e série sintética de excedente. CALCULADO/SIMULADO/HIPÓTESE.

**Resultados:** dez módulos de 1.000 kg a 800 m têm 21,8 kWh ideais; a 80% de recarga exigem 27,25 kWh e, a 55% de descarga, disponibilizam 11,99 kWh. Na série sintética, 1,25 kWh de excedente foram absorvidos para armazenar 1,00 kWh.

**Interpretação:** modularidade amplia capacidade ideal sob independência, mas não prova escala estrutural, potência ou disponibilidade.

**Não sustenta:** redução efetiva de curtailment, viabilidade da Serra do Mar ou eficiência medida.

## Discussão integrada

E1 fornece o teto energético gravitacional. E2 mostra que o mesmo desnível pode exigir comprimentos muito diferentes e que o rolamento cresce em rampas rasas. E3 mostra o compromisso entre força resistente, potência e tempo. E4 reduz a energia mecânica à energia elétrica de uma máquina equivalente hipotética. E5 mostra que recarga, descarga e escala precisam ser contabilizadas separadamente.

O cenário de 800 m e 8 km é hipotético e não deve ser tratado como infraestrutura disponível. Os resultados não representam uma única trajetória contínua: E3 usa torque constante e E4 usa torque dependente da velocidade.

## Limitações gerais

Não há validação experimental, inércia rotacional detalhada, máquina real caracterizada, retificador detalhado, recarga modelada eletromecanicamente, estrutura, segurança, economia ou modelo do SIN. A suíte permanece em 73 testes aprovados de 74, com erro ambiental de limpeza temporária no Windows.

