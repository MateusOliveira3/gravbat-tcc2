# Auditoria de coerência física do dashboard

**Data:** 19/10/2026  
**Escopo:** inspeção matemática e de rastreabilidade, sem alteração de código, modelos ou parâmetros.

## 1. Cenário auditado

Foram considerados os valores observados: `m=6 kg`, `theta=10°`, `H=2 m`, `c_r=0,02`, `v=0,02 m/s`, `eta=0,55` e `N=10` módulos.

Para uma velocidade informada ao longo do trilho:

- `L = H/sen(theta) = 11,5175 m`;
- `v_vertical = v_trilho sen(theta) = 0,003473 m/s`;
- `t_controlado = L/v_trilho = 575,877 s`.

A convenção usada por `dimensionar_configuracao` é explícita: com `theta_graus`, `velocidade_descida_m_s` é velocidade no trilho e a função calcula a componente vertical (`model/inverse_design.py`, linhas 20–35). A velocidade dinâmica de `simulation.simulator` é também velocidade ao longo da rampa (`Estado.velocidade_m_s`). A transmissão usa essa velocidade linear do trilho para obter rotação (`app.py`, linhas 256–272). Não foi encontrada duplicação de seno na dinâmica mecânica.

## 2. Energia e potência do banco

### Energia exibida

`app.py`, linha 155:

```python
energia_banco_Wh = massa_banco * g * altura_pergunta * eficiencia_global / 3600
```

Com `massa_banco=60 kg`:

`E_banco = 60·9,81·2·0,55/3600 = 0,17985 Wh`.

Esse valor está correto como energia útil hipotética baseada no desnível vertical e em `eta=0,55`.

### Potência exibida

`app.py`, linha 156:

```python
potencia_banco_W = massa_banco * g * velocidade_pergunta * eficiencia_global
```

O resultado é:

`60·9,81·0,02·0,55 = 6,4746 W`.

A fórmula trata a velocidade ao longo do trilho como se fosse velocidade vertical. Para a convenção declarada no restante do sistema, a potência gravitacional vertical seria:

`P = N·m·g·v_trilho·sen(theta)·eta = 1,1243 W`.

Também é necessário distinguir potência média da energia dividida pelo tempo controlado. Com `t=L/v=575,877 s`:

`E_banco/t = 0,17985 Wh·3600/575,877 = 1,1243 W`.

**Classificação:** inconsistente na fórmula de `potencia_banco_W`. A energia e o tempo usam o desnível vertical; a potência omite `sen(theta)`.

## 3. Energia cinética de aproximadamente 104 J

O gráfico geral de energia usa `estados = r.amostras(...)` e `charts.energia_posicao(estados)` (`app.py`, linhas 549–554). Esse `r` é produzido por `simular(massa, theta, cr, modo, **dimensao)` (`app.py`, linhas 95–96), com partida do repouso e aceleração livre:

`a = g(sen(theta)-c_r cos(theta)) = 1,51027 m/s²`.

Para `L=11,5175 m`:

- `t_livre = sqrt(2L/a) = 3,9054 s`;
- `v_final = sqrt(2aL) = 5,8982 m/s`;
- `K_final = 0,5·6·v² = 104,37 J`.

O valor observado é, portanto, coerente com a **descida livre do cenário mecânico de 6 kg**, com rolamento equivalente, sem torque de carga e sem velocidade controlada de `0,02 m/s`.

A animação controlada usa outra trajetória: `tempo_controlado = posição/velocidade_pergunta` (`app.py`, linhas 204–205 e 228), mas o gráfico de energia continua usando `r`. **Classificação:** valor matematicamente correto para a descida livre, porém apresentado junto de parâmetros da trajetória controlada. Há mistura de cenários na apresentação.

## 4. Potência instantânea de 14.400 W

`app.py`, linhas 203–205 e 219–229:

```python
massa_aplicacao = resultado_inverso["massa_requerida_kg"]
potencia_visual = massa_aplicacao * g * velocidade_pergunta * eficiencia_global
```

Para uma demanda de `400 Wh`, `H=2 m`, `eta=0,55`:

`massa_aplicacao = 400·3600/(0,55·9,81·2) = 133.444,5 kg`.

Logo:

`P_visual = 133.444,5·9,81·0,02·0,55 = 14.400 W`.

Esse valor pertence à **massa dimensionada pela aplicação**, não ao banco de dez módulos de 6 kg e não à potência instantânea calculada pela dinâmica. Ele é uma potência de referência associada à velocidade-alvo, mantida constante durante a visualização. O rótulo `Potência instantânea` pode induzir a interpretação de geração efetiva, embora a grandeza seja uma estimativa de demanda/aplicação.

Além disso, pela convenção de velocidade no trilho, a versão projetada verticalmente seria `2.502 W` para esse mesmo cálculo (`14.400·sen(10°)`).

**Classificação:** origem rastreável, mas nomenclatura e projeção cinemática são inconsistentes com a convenção declarada.

## 5. Dimensionamento e módulos

Para `E=400 Wh`, `H=2 m`, `eta=0,55`:

- massa pela energia: `133.444,5 kg`, produzida por `massa_energia = energia_J/(eta·g·H)` em `model/inverse_design.py`;
- duração padrão da aplicação: `14.400 s` (4 h), portanto potência média: `100 W`;
- massa pela potência média, usando `v_vertical=v_trilho·sen(theta)`: `5.336,6 kg`;
- módulos para a massa de energia: `ceil(133.444,5/6)=22.241` (`app.py`, linha 157);
- energia útil por módulo: `0,017985 Wh`;
- excedente de `1.000 W` por `1 h`: `1.000 Wh`;
- módulos para absorver esse excedente: `ceil(1.000/0,017985)=55.602` (`app.py`, linha 159).

A massa de 5.337 kg e os 22.241/55.602 módulos são coerentes entre si sob as entradas acima, mas a potência do banco de 6,475 W não usa a mesma convenção energética. A massa pela potência média usa a componente vertical; `potencia_banco_W` não.

**Classificação:** dimensionamento inverso coerente em sua própria função; apresentação do banco inconsistente por usar fórmula de potência diferente.

## 6. Convenções identificadas

| Grandeza | Convenção rastreada |
|---|---|
| `velocidade_pergunta` | Velocidade-alvo ao longo do trilho quando `theta_graus` é informado |
| `Estado.velocidade_m_s` | Velocidade ao longo da rampa, calculada pela dinâmica |
| `velocidade_vertical_m_s` | Componente vertical calculada em `inverse_design.py` |
| Velocidade da corda | Não há variável separada no trecho auditado |
| Velocidade no eixo | Obtida por `cinematica` como rotação/RPM, não em m/s |
| `potencia_visual` | Potência de referência da massa de aplicação na velocidade-alvo |
| Potência dinâmica E4 | `potencia_ac_W` do modelo eletromecânico dependente da velocidade |

## 7. Proposta mínima de correção, sem implementar

1. Definir e exibir explicitamente se cada velocidade é no trilho, vertical ou no eixo.
2. Corrigir conceitualmente `potencia_banco_W` para usar a mesma convenção da energia e do dimensionamento: `m·g·v_trilho·sen(theta)·eta`, ou renomear a variável caso a intenção seja potência ao longo do trilho.
3. Renomear `Potência instantânea` da animação para algo como `Potência de referência da aplicação` e separar essa métrica da potência dinâmica.
4. Separar visualmente a trajetória livre `r` da animação controlada por velocidade-alvo.
5. Mostrar `E_banco/t_controlado` ao lado da potência baseada em força e velocidade para tornar a consistência verificável.
6. Não misturar a energia cinética da massa de 6 kg com a massa dimensionada pela aplicação.

## 8. Testes recomendados

- Para uma rampa inclinada, verificar `E_banco/t_controlado == N·m·g·v_trilho·sen(theta)·eta`.
- Verificar que ao mudar `theta`, mantendo `H`, `m`, `N`, `v_trilho` e `eta`, a potência vertical muda por `sen(theta)`.
- Verificar que `potencia_visual` é identificada como aplicação e não como potência dinâmica.
- Verificar que a curva cinética da trajetória livre não é exibida como se fosse a trajetória controlada.
- Verificar que `energia_banco_Wh` e `potencia_banco_W` usam a mesma massa, eficiência e convenção cinemática.
- Verificar que os módulos para energia e excedente usam a energia por módulo, enquanto a potência de atendimento usa potência compatível com a mesma velocidade.

## Conclusão da auditoria

A divergência principal é real e localizada em `app.py`: a potência do banco e a potência visual usam a velocidade ao longo do trilho sem a projeção vertical, embora a energia, o tempo controlado e o dimensionamento inverso tratem o desnível vertical. Os 104 J de energia cinética são corretos para a descida livre do cenário mecânico de 6 kg, mas aparecem junto da visualização controlada. Nenhuma alteração foi implementada nesta auditoria.
