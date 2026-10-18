# Explorador de aplicações V0.9

## Objetivo científico

Investigar como a estimativa de massa gravitacional varia quando a pergunta é
formulada em termos de demanda de energia, potência, altura e duração de
descarga.

## Modelo

`m = E_util/(η g h)` e `P_media = E_util/t_descarga`.

As entradas de energia e potência dos cenários pré-cadastrados são **HIPÓTESE**
de exploração. O desnível, a eficiência e a duração também são entradas de
cenário. O resultado de massa é **CALCULADO**.

## Implementação

`model/application_scenarios.py` mantém presets identificados como hipótese.
`model/dimensioning.py` executa as equações e o dashboard permite substituir
qualquer valor antes do cálculo.

## Interpretação e limitações

O explorador serve para comparar ordens de grandeza e formular perguntas de
projeto. Não representa curva de carga real, estudo de transmissão, despacho,
disponibilidade, licenciamento, custos, segurança ou validação de curtailment.
O cenário urbano não representa a demanda de uma cidade específica.

## Próxima etapa

Substituir presets por dados documentados de demanda e terreno, mantendo a
origem de cada parâmetro e separando energia, potência, disponibilidade e
restrições de rede.

O comprimento do percurso pode ser informado como verificação geométrica. A interface calcula `sin(θ) = H/L` e exibe a inclinação equivalente. Essa inclinação não substitui levantamento topográfico nem altera automaticamente o cálculo energético, que usa o desnível vertical `H`.

## Dimensionamento inverso

A V1.0 inclui uma função de dimensionamento inverso. Dada energia útil, potência máxima, duração, altura, eficiência e velocidade de descida, calcula-se a massa pela restrição energética e pela restrição de potência. A massa recomendada é o maior desses valores:

`m = max(E/(ηgh), P/(ηgv))`

O resultado é **CALCULADO**. A velocidade é uma condição de operação que exige freio eletromagnético ou conversor controlado; a ponte de diodos sozinha não garante regulação de velocidade.

A referência de 50 s permanece restrita ao cenário didático de bancada. Para o explorador residencial, o preset inicial foi alterado para uma hora de operação (`3600 s`) e 100 W, correspondendo a 100 Wh por evento. Esses valores continuam sendo hipóteses configuráveis, não curva de consumo medida.

No modo compacto, o dimensionamento inverso usa a geometria principal do cenário, evitando que uma altura independente contradiga a rampa visual. Alturas alternativas permanecem disponíveis apenas na auditoria técnica como análise paramétrica.
