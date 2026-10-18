# GravBat | Armazenamento gravitacional em plano inclinado

**Trabalho de Conclusão de Curso II | Engenharia de Energia | Universidade Federal de Santa Catarina (UFSC)**

O GravBat é um projeto de pesquisa sobre armazenamento de energia por meio do deslocamento de massas em planos inclinados. A proposta surgiu durante o TCC I, a partir do interesse em investigar alternativas de armazenamento para sistemas elétricos com participação crescente de fontes renováveis, especialmente solar e eólica.

Nesta segunda etapa, o trabalho passou a se concentrar na modelagem matemática e na simulação do sistema. O objetivo é compreender como a inclinação do percurso, as resistências mecânicas, o torque aplicado à transmissão e as características da conversão eletromecânica afetam a energia que pode ser recuperada durante a descida de uma massa.

O estudo não parte da hipótese de que o plano inclinado seja necessariamente mais eficiente que um sistema vertical. Para uma mesma massa e um mesmo desnível, ambos possuem a mesma energia potencial gravitacional ideal. A diferença está nas condições necessárias para realizar o deslocamento e recuperar essa energia.

## 1. O que estamos investigando?

A energia potencial gravitacional de uma massa elevada a determinada altura pode ser calculada por:

\[
E_g = m \cdot g \cdot H
\]

Em que:

- \(E_g\) é a energia potencial gravitacional, em joules;
- \(m\) é a massa, em quilogramas;
- \(g\) é a aceleração da gravidade, em metros por segundo ao quadrado;
- \(H\) é o desnível vertical, em metros.

Essa expressão estabelece a energia ideal disponível, mas não determina quanto será efetivamente convertido em eletricidade.

No plano inclinado, a força responsável pelo movimento depende da inclinação do trilho. Além disso, a massa percorre uma distância maior que o desnível vertical, ficando sujeita às resistências mecânicas ao longo do trajeto.

A pesquisa procura responder como esses fatores interferem no movimento, na potência mecânica e na energia entregue a uma carga elétrica.

## 2. Modelos e simulações desenvolvidos

O trabalho foi organizado em cinco experimentos computacionais, construídos para analisar aspectos diferentes do funcionamento do sistema.

| Experimento | Análise realizada | Resultado de referência |
|---|---|---|
| **E1** | Energia potencial em função da massa e da altura | Uma massa de 1.000 kg elevada a 2 m armazena idealmente 19.620 J, ou 5,45 Wh. |
| **E2** | Geometria do plano inclinado e perdas por rolamento | Para vencer 1 m de desnível, o percurso é de aproximadamente 28,65 m a 2° e 2 m a 30°. |
| **E3** | Influência do torque resistente sobre a descida | No modelo de torque constante, a potência mecânica média máxima ocorre em 2/3 do torque-limite, resultando em aproximadamente 2,99 W no caso estudado. |
| **E4** | Conversão eletromecânica com carga resistiva | No cenário com carga de 8 Ω, foram calculados 0,4766 J entregues à carga AC e 0,1192 J de perdas no cobre. |
| **E5** | Dimensionamento hipotético de módulos e ciclos de armazenamento | Dez módulos de 1.000 kg, com 800 m de desnível, possuem 21,8 kWh de energia potencial ideal. Com rendimento hipotético de descarga de 55%, a saída estimada é de 11,99 kWh. |

Os experimentos não representam necessariamente uma única configuração física. Em particular, o E3 considera torque resistente constante, enquanto o E4 utiliza um modelo eletromecânico equivalente cuja resposta depende da velocidade e da carga elétrica.

### E1. Energia potencial

O primeiro experimento estabelece a relação entre massa, altura e capacidade energética. Seu propósito é verificar as ordens de grandeza envolvidas antes de considerar as perdas do sistema.

![Energia potencial gravitacional](docs/tcc/figuras_consolidadas/figura_01_e1_energia.svg)

### E2. Inclinação e resistência ao movimento

No segundo experimento, a geometria passa a fazer parte da análise. Para um desnível fixo, diminuir o ângulo aumenta o comprimento do percurso e, no modelo adotado, o trabalho dissipado pela resistência ao rolamento.

A condição angular de aproximadamente 1,146°, obtida para coeficiente de rolamento igual a 0,02, corresponde ao equilíbrio entre a componente gravitacional tangencial e a resistência modelada. Não deve ser interpretada como um limite universal para qualquer sistema sobre trilhos.

![Geometria e perdas no plano inclinado](docs/tcc/figuras_consolidadas/figura_02_e2_geometria.svg)

### E3. Torque resistente e potência

O terceiro experimento investiga a influência do torque resistente sobre a aceleração e o tempo de descida.

Um torque elevado reduz a aceleração e pode impedir o movimento. Por outro lado, uma resistência pequena permite maior aceleração, mas não necessariamente proporciona a maior potência transferida ao eixo.

O ponto de máxima potência mecânica média identificado é uma consequência das hipóteses desse modelo. Ele não representa, por si só, a condição de máxima eficiência elétrica.

![Torque resistente e potência mecânica](docs/tcc/figuras_consolidadas/figura_03_e3_potencia.svg)

### E4. Conversão eletromecânica

O quarto experimento acrescenta um modelo equivalente de conversão eletromecânica, considerando força eletromotriz, resistência elétrica, carga e perdas associadas.

Essa etapa permite examinar a distribuição da energia durante a descida, incluindo a parcela entregue à carga, as perdas e a energia cinética que permanece na massa ao final do percurso.

O modelo utiliza parâmetros hipotéticos e carga resistiva passiva. Ainda não representa um gerador físico caracterizado nem um sistema de controle com encoder e PWM.

A figura temporal consolidada desse experimento permanece pendente.

### E5. Escalabilidade e deslocamento temporal de energia

O quinto experimento amplia a discussão para cenários hipotéticos com múltiplos módulos e diferentes desníveis.

Também foi utilizada uma série sintética de excedente energético para estudar a lógica de carregamento e descarregamento ao longo do tempo.

![Ciclo de armazenamento com excedente sintético](docs/tcc/figuras_consolidadas/figura_04_e5_excedente.svg)

Os rendimentos utilizados nessa etapa são hipóteses de cálculo. Eles não foram obtidos pela extrapolação do modelo eletromecânico do E4. O exercício também não demonstra redução efetiva de restrições de geração no Sistema Interligado Nacional.

## 3. Organização do projeto

O código foi separado conforme a função de cada componente:

- `model/`: equações de geometria, mecânica, transmissão, energia e conversão eletromecânica.
- `simulation/`: rotinas de simulação dos modelos mecânico, eletromecânico e de ciclos de armazenamento.
- `dashboard/`: componentes de visualização e exploração dos cenários.
- `tests/`: testes automatizados.
- `docs/tcc/`: relatórios dos experimentos, figuras e documentos de apoio à monografia.
- `outputs/`: resultados e registros de execução.
- `app.py`: aplicação interativa desenvolvida com Streamlit.

Para uma visão resumida do andamento da pesquisa, consulte [Apresentação ao orientador](docs/APRESENTACAO_ORIENTADOR.md).

## 4. Como executar

O projeto utiliza Python 3.12 ou versão compatível, além das bibliotecas indicadas no arquivo `requirements.txt`.

No Windows, abra o PowerShell na pasta principal do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Para executar os testes:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

Para iniciar a interface:

```powershell
.\.venv\Scripts\python.exe -B -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Depois, acesse `http://127.0.0.1:8501` no navegador.

Também existe uma rotina de verificação do dashboard:

```powershell
.\.venv\Scripts\python.exe -B verificar_dashboard.py
```

Na auditoria de 18 de outubro de 2026, essa rotina foi iniciada, mas não terminou dentro do tempo disponível. Portanto, sua execução completa ainda precisa ser confirmada.

## 5. Estado atual e limitações

Na auditoria realizada em 18 de outubro de 2026, foram executados 74 testes automatizados. Destes, 73 foram aprovados e um apresentou erro de permissão durante a limpeza de um diretório temporário no Windows (`WinError 5`).

A falha registrada não correspondeu a uma divergência identificada nas equações físicas, mas sua causa e a possibilidade de reprodução em outros ambientes ainda precisam ser verificadas.

Até o momento, a pesquisa foi desenvolvida computacionalmente. Não foram realizados ensaios físicos de bancada nem a caracterização experimental de um conjunto gerador, transmissão e frenagem.

Também permanecem fora do escopo atual o dimensionamento estrutural, a análise de custos, a avaliação de segurança operacional e a integração elétrica efetiva com o SIN.

O cenário de grande desnível considerado no E5 é uma hipótese para comparação de ordens de grandeza. Não representa um projeto de implantação em local específico.

## 6. Continuidade da pesquisa

Os próximos passos serão definidos em conjunto com o orientador, especialmente quanto à suficiência da abordagem computacional para o TCC-2 e à necessidade de aprofundamento de determinados modelos.

Entre os pontos que ainda precisam ser discutidos estão a comparação com sistemas verticais, a seleção dos resultados que integrarão a monografia, a consolidação das referências e a possibilidade de uma futura etapa experimental.

O propósito do GravBat, nesta fase, é estabelecer uma base de análise física e computacional que permita compreender o potencial energético do plano inclinado sem desconsiderar suas perdas e limitações.