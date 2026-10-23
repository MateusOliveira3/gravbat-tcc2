# E6 — Diagnóstico de descarga controlada e otimização paramétrica

**Status:** primeira rodada de diagnóstico; nenhum modelo E1–E5 foi alterado.  
**Data:** 23/10/2026  
**Branch:** `fix/coerencia-fisica-dashboard`  
**Commit de referência:** `868fe53`

## 1. Escopo executado

A diretriz do E6 solicitou, nesta primeira rodada, diagnóstico quantitativo, avaliação preliminar da meta de 60 s/0,5 W e proposta de arquitetura. Não foram implementados controladores, novas equações, varreduras extensas ou otimização.

A suíte existente foi executada com:

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -q
```

Resultado: 88 testes, 87 aprovados e 1 erro ambiental conhecido de limpeza temporária no Windows (`PermissionError: [WinError 5]`). Não houve alteração de código científico.

## 2. Por que o E4 desce em poucos segundos

No cenário de diagnóstico (`m=6 kg`, `H=1 m`, `theta=10°`, `c_r=0,02`), a geometria de desnível fixo produz `L=5,75877 m`. O modelo mecânico calcula aceleração inicial de aproximadamente `1,51027 m/s²` e uma descida livre de `2,76155 s`.

No integrador eletromecânico atual, a força resistente é calculada a partir do torque equivalente do gerador:

`F_carga = G * tau_em / (eta_t * r_d)`

O torque eletromagnético depende da velocidade e da FEM equivalente. Com os parâmetros hipotéticos documentados (`K_e=0,1`, `R_fase=2 ohm`, duas fases, `r_d=0,05 m`, `G=1`, `eta_t=0,90`, carga de 8 ohm), a carga retarda apenas parcialmente o movimento. A execução forneceu:

| R_carga (ohm) | duração (s) | velocidade final (m/s) | energia eletromagnética integrada (J) | cobre (J) |
|---:|---:|---:|---:|---:|
| 1 | 3,114 | 3,282 | 17,886 | 11,924 |
| 2 | 3,018 | 3,492 | 14,036 | 7,018 |
| 4 | 2,928 | 3,711 | 9,789 | 3,263 |
| 8 | 2,859 | 3,891 | 6,082 | 1,216 |
| 100 | 2,771 | 4,143 | 0,625 | 0,012 |

A energia na carga AC é aproximadamente `E_em - E_cobre`; para 8 ohm, cerca de `4,866 J`. A resistência de carga altera sobretudo a potência e a parcela dissipada, mas não cria por si só uma descarga de 60 s. O modelo atual não representa inércia rotacional detalhada nem um controlador de velocidade.

A inclinação também influencia o tempo: com desnível fixo, ângulos menores aumentam o comprimento, mas reduzem a força tangencial; isso não garante uma descarga longa quando a aceleração líquida continua positiva. O raio, a transmissão e o torque resistente são os parâmetros que podem alterar diretamente a força refletida; devem ser limitados por uma especificação mecânica, e não ajustados para produzir um tempo desejado.

## 3. Viabilidade preliminar da meta de 0,5 W por 60 s

A demanda exige:

`E_demanda = 0,5 W * 60 s = 30 J`.

A energia potencial ideal do cenário é:

`E_g = 6 kg * 9,81 m/s² * 1 m = 58,86 J`.

Portanto, 30 J correspondem a aproximadamente 50,96% da energia potencial ideal. Energeticamente, a meta não é proibida pelo limite superior ideal. Porém, a execução passiva atual com carga de 8 ohm entrega aproximadamente 4,866 J na carga AC, muito abaixo de 30 J, e termina em cerca de 2,859 s. Assim, **a meta não é atendida pelo E4 passivo atual**.

Também não é correto concluir ainda que a meta é impossível. Uma descarga controlada poderia prolongar o tempo, mas a potência elétrica depende da velocidade e da carga; reduzir a velocidade pode reduzir a FEM e a potência instantânea. Será necessário modelar explicitamente torque de frenagem, limites de velocidade, eficiência e perdas, além de definir se os 30 J são medidos na carga AC ou após retificação.

## 4. Arquitetura recomendada para E6

A investigação deve ser separada em camadas:

1. **Caso passivo de referência:** reutilizar `simulation/electromechanical_dynamic.py` sem mudanças, registrando duração, estado final, energia AC, cobre e resíduo.
2. **Modelo de torque prescrito:** adicionar, em módulo separado, uma lei de torque limitada por `tau_max`, com estados explícitos de movimento, bloqueio e parada. Não substituir o V0.4 nem o E4.
3. **Modelo de velocidade limitada:** definir uma referência de velocidade e um controlador idealizado apenas depois de aprovar torque máximo, saturação e critério de estabilidade. O controlador não deve ser apresentado como hardware validado.
4. **Frenagem terminal:** tratar a desaceleração final como parcela de energia separada; não contabilizar toda frenagem como energia elétrica recuperada.
5. **Varredura/otimização:** somente após validar balanço energético e convergência temporal. Objetivos devem ser executados separadamente: energia, potência média, duração e compromisso multicritério.

## 5. Módulos reutilizáveis

- `model/geometry.py`: comprimento, desnível e ângulo.
- `model/mechanics.py`: força gravitacional, rolamento e força disponível.
- `model/coupling.py`: referência V0.4 de torque constante e limite analítico.
- `model/electromechanics.py`: equivalente de FEM, carga, cobre e retificação.
- `simulation/electromechanical_dynamic.py`: integrador passivo dependente da velocidade.
- `simulation/simulator.py`: trajetória mecânica analítica de referência.
- Testes existentes em `tests/` para balanço, parada, convergência e unidades.

## 6. Hipóteses que exigem aprovação antes da implementação

- ponto físico de aplicação do torque e limites de torque;
- inclusão ou não de inércia rotacional equivalente;
- definição de potência principal: carga AC ou energia CC estimada;
- eficiência de transmissão e retificação, sem dupla contagem;
- modelo de controle e sua saturação;
- critério de parada e tratamento de frenagem terminal;
- passo temporal e tolerâncias de convergência;
- restrições máximas de velocidade, comprimento e potência;
- se a meta de 60 s deve ser tratada como requisito de projeto ou apenas cenário de sensibilidade.

## 7. Conclusão da primeira rodada

O diagnóstico confirma que os tempos curtos são consequência do regime acelerado e da carga eletromecânica equivalente insuficiente para equilibrar a força motriz, não de uma simples falha de conversão de unidades. A meta de `0,5 W por 60 s` é inferior à energia potencial ideal disponível, mas não é alcançada pelo caso passivo atual. A próxima etapa segura é especificar e testar um modelo de torque/velocidade controlados em experimento E6 separado, com balanço energético e limites explícitos.

Nenhum resultado novo foi incorporado a E1–E5, nenhum commit ou push foi executado.
