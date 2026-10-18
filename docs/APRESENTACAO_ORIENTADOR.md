# GravBat TCC-2 — Apresentação ao orientador

## 1. Ponto de partida

O TCC-1 estabeleceu a ideia de armazenamento gravitacional com massa móvel e a necessidade de relacionar geometria, energia, transmissão e conversão. O TCC-2 transforma essa ideia em um núcleo computacional auditável. A continuidade preserva as hipóteses úteis do trabalho anterior, mas separa resultados analíticos, simulações, hipóteses e questões ainda não verificadas.

## 2. O que foi desenvolvido

O repositório contém modelos de geometria e mecânica, transmissão, dimensionamento, balanço de energia, dinâmica eletromecânica equivalente e ciclo de carga/descarga. O dashboard Streamlit permite alterar massa, inclinação, desnível, resistência ao rolamento, torque e parâmetros de carga dentro do escopo documentado.

A investigação foi organizada em cinco experimentos:

- **E1 — energia potencial:** cálculo de $E_g=m g H$ para estabelecer a escala ideal.
- **E2 — geometria e perdas:** influência do ângulo, do comprimento e do rolamento, especialmente com desnível fixo.
- **E3 — torque e potência:** compromisso entre torque resistente, aceleração, tempo e potência média no modelo V0.4.
- **E4 — conversão eletromecânica:** modelo equivalente com carga resistiva, FEM e perdas de cobre/retificação.
- **E5 — escalabilidade e ciclo:** soma ideal de módulos, recarga, descarga e série sintética de excedente.

## 3. Perguntas da comparação vertical × inclinada

A comparação busca responder quatro condições diferentes:

1. Com a mesma massa e o mesmo desnível, o potencial $m g H$ é igual, embora percurso e perdas possam mudar.
2. Com a mesma massa e velocidade linear, a componente motriz no trilho depende de $\sin\theta$.
3. Com o mesmo desnível e duração, uma rampa mais rasa exige maior comprimento e velocidade média no percurso.
4. Com rolamento modelado, $E_{rol}=c_r m g H\cot\theta$ para desnível fixo; isso é uma hipótese do modelo inclinado, não uma perda atribuída automaticamente a uma arquitetura vertical.

Essa comparação é analítica e usa resultados já existentes. Ela não cria uma equivalência completa de estrutura, segurança ou eficiência entre arquiteturas.

## 4. Resultados existentes

| Resultado | Valor documentado | Status |
|---|---:|---|
| 1.000 kg, 2 m | 19.620 J = 5,450 Wh | CALCULADO |
| 1.000 kg, 800 m | 2,180 kWh ideais | CALCULADO; cenário hipotético |
| E2, H=1 m, 2° | L=28,65 m | CALCULADO |
| E2, H=1 m, 30° | L=2,00 m | CALCULADO |
| Limiar com $c_r=0,02$ | $\theta>1,146°$ | DEDUÇÃO ANALÍTICA |
| E3, torque ótimo | $\tau/\tau_{lim}=2/3$; eixo ≈2,9881 W | CALCULADO |
| E4, carga 8 Ω | 0,4766 J na carga AC; 0,1192 J em cobre | SIMULADO/CALCULADO |
| E5, 10×1.000 kg a 800 m | 21,8 kWh ideais; 11,99 kWh a 55% assumidos | CALCULADO/HIPÓTESE |

## 5. O que os resultados permitem concluir

Os resultados permitem afirmar que massa e desnível determinam linearmente o potencial gravitacional. Também mostram que, em uma rampa com desnível fixo, reduzir a inclinação aumenta o percurso e o trabalho de rolamento segundo as hipóteses adotadas. No modelo de torque constante, existe um compromisso entre potência média e duração, e o ponto de $2/3$ do torque-limite é uma propriedade desse modelo específico.

E5 permite comparar ordens de grandeza de módulos e ciclos de forma idealizada. A série de excedente é sintética e serve para ilustrar absorção temporal, não para medir curtailment.

## 6. O que não pode ser concluído

Os resultados não demonstram que o GravBat possa alimentar uma cidade, substituir uma usina, reduzir curtailment real no SIN ou ser instalado na Serra do Mar. Também não demonstram viabilidade econômica, estrutural, ambiental, segurança operacional, eficiência industrial ou autonomia residencial.

A eficiência de E4 não deve ser extrapolada para o cenário de 800 m. E3 e E4 representam modelos diferentes. Uma simulação computacional não substitui ensaio físico de motor, transmissão, trilho, cabo, freio ou estrutura.

## 7. Limitações atuais

- ausência de bancada física e de componente gerador identificado;
- inércia rotacional, estrutura, frenagem de emergência e segurança fora do núcleo;
- parâmetros de rolamento, transmissão e conversão tratados como hipóteses documentadas;
- ausência de fluxo de potência, despacho ou modelo do SIN;
- figura temporal de E4 ainda pendente;
- suíte com 73 testes aprovados em 74, devido a erro ambiental de limpeza temporária no Windows.

## 8. Decisões para discutir

1. Confirmar o enquadramento formal como investigação computacional.
2. Definir quais referências do TCC-1 serão mantidas após conferência bibliográfica.
3. Decidir se o cenário Serra do Mar permanece apenas como hipótese conceitual.
4. Definir o nível de detalhamento da futura arquitetura com motor de passo, encoder, PWM e frenagem.
5. Decidir quais resultados entram na versão final da monografia e quais ficam como material suplementar.

## 9. Como reproduzir

Na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -B verificar_dashboard.py
.\.venv\Scripts\python.exe -B -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Os relatórios E1–E5, a matriz de evidências e as figuras estão em `docs/tcc/`.
