# Verificação dinâmica eletromecânica

## Objetivo

Verificar como a velocidade altera a FEM, a corrente, a potência e o torque resistente durante a descida.

## Saídas observadas

O dashboard apresenta, na área de verificação, as séries temporais de velocidade, torque eletromagnético, potência AC e energia acumulada. Também informa a perda de cobre acumulada. Essas grandezas são **SIMULADAS** pelo integrador explícito e utilizam parâmetros classificados como **HIPÓTESE**, **DATASHEET** ou **MEDIDO** conforme o motor selecionado.

## Interpretação

Com a aproximação atual, o torque e a potência variam com a velocidade. A curva não constitui validação experimental. Ela permite verificar tendências, detectar bloqueio, comparar passo temporal e identificar se o acoplamento está produzindo sentido físico coerente.

## Próxima verificação

Comparar a energia elétrica integrada numericamente com o trabalho mecânico extraído e com a solução analítica em casos simplificados.

A trajetória eletromecânica também pode ser exportada em CSV. O arquivo contém tempo, posição, velocidade, aceleração, velocidade angular, torque, potência AC, energia acumulada e perda de cobre, com unidades no cabeçalho. Isso permite reconstruir figuras técnicas fora da interface sem alterar os dados da simulação.
