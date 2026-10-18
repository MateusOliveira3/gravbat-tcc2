# Correções P0 e verificação — Passagem B

**Data:** 12/10/2026  
**Escopo:** correções P0 autorizadas pela IA coordenadora. Novos serviços, otimização e funcionalidades de dashboard não foram implementados nesta passagem.

## 1. Proteção e estado anterior

Foi criado o backup local:

`outputs/backup_pre_p0_20261012_104624/`

Ele contém cópias dos arquivos físicos principais, `tests_before.txt` e hashes SHA-256. A suíte anterior registrou **68 testes passando**; após os testes P0 são 74 casos descobertos. O diretório não possui um repositório Git válido; nenhum remoto foi criado.

## 2. Dimensionamento inverso

A formulação anterior calculava massa por energia e potência média, mas deixava a potência de pico apenas como diagnóstico. A nova função mantém as grandezas separadas e retorna `DADOS_INSUFICIENTES` quando uma potência de pico maior que a média é informada sem duração de pico.

Caso obrigatório:

- 1 Wh, 1000 W, 3600 s, 10 m, η=0,5, velocidade vertical 0,02 m/s;
- massa pela energia: 73,39 kg;
- massa pela potência média: 10,19 kg;
- massa para sustentar 1000 W continuamente: 10.193,68 kg;
- status: `DADOS_INSUFICIENTES` para declarar atendimento do pico sem sua duração.

A regra agora impede que 1 Wh seja apresentado como 1000 W durante uma hora.

## 3. Velocidade e geometria

A API passou a retornar `velocidade_trilho_m_s` e `velocidade_vertical_m_s`. Quando o ângulo é informado, usa:

`v_vertical = v_trilho · sen(θ)`

O dashboard passa o ângulo do cenário ao dimensionamento inverso. A velocidade prescrita continua sendo hipótese de operação/controlabilidade, não medição nem garantia física.

## 4. Potência eletromecânica

`previa_carga_resistiva` agora separa:

- `potencia_carga_W`;
- `potencia_cobre_W`;
- `potencia_em_W`;
- `potencia_cc_W`;
- torque resistente.

A relação verificada é:

`P_em = P_cobre + P_carga`

O torque usa `P_em/|ω|`, enquanto a eficiência do retificador é aplicada à potência externa estimada. A topologia continua equivalente e hipotética; não representa automaticamente um motor de passo físico.

## 5. Integrador dinâmico

A aceleração não é mais truncada para zero. O integrador usa a força líquida assinada, impede velocidade negativa e retorna estado `PARA` se a velocidade atingir zero durante a desaceleração. A inércia rotacional e o atrito estático continuam explicitamente fora do modelo.

## 6. Testes adicionados

Foi criado `tests/test_correcoes_p0.py` com testes para:

- pico sem duração e status `DADOS_INSUFICIENTES`;
- componente vertical da velocidade em 30°;
- balanço de potência eletromagnética e torque incluindo cobre.

Resultado atual:

```text
Ran 74 tests; 73 passaram. Um teste existente falhou apenas na limpeza de diretório temporário por `PermissionError` do ambiente Windows, sem falha de asserção física.
```

Os testes anteriores foram preservados. O aumento de 68 para 74 corresponde aos novos testes independentes P0; a execução apresentou a limitação ambiental de limpeza temporária descrita acima.

## 7. Limitações ainda abertas

- A convergência temporal foi formalizada em teste reproduzível para três passos; permanece uma limitação de discretização, sem inferir ordem de convergência.
- Falta um caso integrado de ciclo completo de subida e descida.
- O modelo do retificador e das fases continua equivalente/hipotético.
- `model/dimensioning.py` agora retorna massas por energia, potência média e pico, velocidade vertical e status compatíveis com o dimensionamento inverso.
- A interface exibe aviso explícito para `DADOS_INSUFICIENTES`.
- Modularidade e curtailment continuam fora da correção física desta passagem.

## 8. Arquivos modificados nesta passagem

- `model/inverse_design.py`;
- `model/electromechanics.py`;
- `simulation/electromechanical_dynamic.py`;
- `app.py` (apenas chamada da semântica geométrica);
- `tests/test_correcoes_p0.py`;
- `model/dimensioning.py`.

## 9. Implicações para o TCC

Os resultados agora distinguem energia armazenada, potência média, pico não dimensionado e componente vertical da velocidade. Isso reduz o risco de declarar atendimento com base apenas em energia ou potência média. A correção não valida experimentalmente o sistema; ela melhora a consistência dimensional e a rastreabilidade do núcleo computacional.

**A Passagem B deve parar aqui para revisão da IA coordenadora.**

### Convergência temporal observada

No cenário eletromecânico de teste (`m=5 kg`, `θ=10°`, `L=1,2 m`, `R_carga=8 Ω`), a redução do passo produziu:

| passo (s) | posição final (m) | velocidade final (m/s) | energia eletromagnética acumulada (J) |
|---:|---:|---:|---:|
| 0,004 | 1,200 | 1,8432 | 0,5967 |
| 0,002 | 1,200 | 1,8403 | 0,5939 |
| 0,001 | 1,200 | 1,8403 | 0,5938 |

A posição converge exatamente no limite da rampa e velocidade/energia estabilizam entre 0,002 s e 0,001 s. O teste `test_desaceleracao_para_antes_do_final` usa velocidade inicial não nula, força resistente dominante e verifica parada sem posição negativa ou avanço após a parada.
