# C4 — Introdução (rascunho)

## 1 Introdução

A expansão de fontes renováveis variáveis altera a relação entre capacidade instalada, geração efetiva e operação do sistema elétrico. No Brasil, os dados recentes da EPE registram crescimento expressivo da capacidade instalada e da participação solar e eólica, ao mesmo tempo em que a transmissão e os requisitos operativos continuam condicionando o aproveitamento espacial e temporal da geração [1]. O PDE 2035 trata esse crescimento em um horizonte de planejamento que exige compatibilizar oferta, rede, carga e flexibilidade [2]. Esses dados descrevem o contexto do sistema; não significam, por si só, que toda capacidade instalada esteja disponível em qualquer instante.

A geração variável introduz diferenças entre o recurso disponível, a produção efetivamente despachada e a energia que pode ser escoada pela rede. Quando a produção precisa ser reduzida, o termo curtailment deve ser usado com precisão. O ONS classifica os cortes em razão energética, confiabilidade e indisponibilidade externa, além de relacioná-los às condições de rede e de operação [3]. Assim, armazenamento pode ser investigado como recurso de flexibilidade temporal, mas não deve ser apresentado como solução automática para todos os cortes nem como demonstração de mitigação no SIN.

Neste trabalho, o armazenamento gravitacional é estudado como uma forma de converter energia elétrica em energia potencial de uma massa e recuperar parte dessa energia por uma cadeia mecânica e eletromecânica. A relação ideal de primeira ordem é

$$E_g=m g H,$$

em que $m$ é a massa, $g$ a aceleração gravitacional e $H$ o desnível vertical. A equação mostra que a capacidade potencial depende da massa e da altura, enquanto não determina sozinha potência, duração, perdas ou energia elétrica entregue.

O GravBat investiga particularmente uma massa deslocada em plano inclinado. Essa escolha permite examinar como inclinação, comprimento, componente tangencial do peso, resistência ao rolamento, transmissão e carga resistente se relacionam. Arquiteturas inclinadas, ferroviárias, de encosta e montanha já são discutidas na literatura de armazenamento gravitacional [4,5]; portanto, o plano inclinado é uma configuração investigada, não uma tecnologia declarada como inédita.

A pergunta central é: **como massa, desnível, inclinação, perdas mecânicas, torque resistente e conversão eletromecânica condicionam a energia e a potência estimadas de um sistema gravitacional modular?** O objetivo geral é analisar essas relações por meio de modelos e cálculos reproduzíveis, preservando a distinção entre potencial gravitacional, energia mecânica extraída e energia elétrica estimada.

Os objetivos específicos são: (a) calcular a energia potencial para diferentes massas e alturas; (b) quantificar o efeito da inclinação sobre comprimento, forças e perdas por rolamento; (c) investigar o compromisso entre torque, aceleração, potência média e duração; (d) avaliar uma conversão eletromecânica equivalente sob hipóteses explícitas; e (e) explorar a escala modular, a recarga e um cenário sintético de excedente renovável.

O trabalho é uma investigação computacional. Os resultados E1–E5 são classificados conforme sua origem como calculados, simulados ou hipotéticos. Não há, nesta etapa, validação experimental do conjunto, caracterização de uma máquina física, projeto estrutural ou modelo de fluxo de potência do SIN. O cenário de 800 m de desnível e 8 km de percurso é mantido como hipótese conceitual, sem afirmar viabilidade ferroviária, ambiental, econômica ou operacional.

O triângulo geração–transmissão–armazenamento é usado apenas como representação conceitual da flexibilidade. Ele não substitui a topologia geração–transmissão–distribuição do sistema elétrico. A contribuição pretendida é organizar uma análise quantitativa das relações físicas e explicitar quais conclusões podem ser sustentadas pelo modelo.

## Referências citadas nesta seção

[1] EPE. *Anuário Estatístico de Energia Elétrica 2026*. Dados de destaques de 2025. 

[2] EPE. *Plano Decenal de Expansão de Energia — PDE 2035*.

[3] ONS. *Diagnóstico e perspectiva da evolução dos cortes de geração no Brasil*. RT DGL-ONS 0189/2025.

[4] ZHANG, J. et al. Gravity energy storage technology based on slopes and mountains. *Energy Storage Science and Technology*, v.13, n.3, p.924–933, 2024. DOI: 10.19799/j.cnki.2095-4239.2023.0667.

[5] QIN, T. et al. Study on factors influencing rail gravity energy storage system efficiency. *Energy Storage Science and Technology*, v.12, n.3, p.835–845, 2023. DOI: 10.19799/j.cnki.2095-4239.2022.0634.
