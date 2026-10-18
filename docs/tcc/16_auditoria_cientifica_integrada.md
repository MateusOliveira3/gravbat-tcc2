# Auditoria científica integrada — GravBat TCC-2

**Passagem:** A — diagnóstico, sem correção da física nesta etapa  
**Data:** 12/10/2026  
**Status:** diagnóstico inicial; a Passagem B depende de aprovação da IA coordenadora científica.

## Escopo e preservação

A diretriz recebida determina preservar V0.1–V0.4, não reescrever o projeto e suspender novas funcionalidades até concluir os itens P0. O estado atual foi inspecionado e a suíte existente foi executada:

```text
Ran 68 tests in 0.17s
OK
```

O diretório de trabalho não expõe um repositório Git no caminho atual, portanto não foi possível registrar `git status` ou criar ponto de recuperação por Git nesta execução. Os arquivos e a documentação histórica foram preservados; nenhuma alteração de física foi realizada nesta Passagem A.

## P0-01 — dimensionamento inverso e semântica da potência

**Arquivos:** `model/inverse_design.py`, `model/dimensioning.py`, `app.py`  
**Status:** confirmado; requer correção na Passagem B.

`dimensionar_configuracao` calcula:

```text
massa_energia = energia_Wh · 3600 / (η · g · H)
massa_potencia_pico = P_solicitada / (η · g · v)
massa_potencia_media = P_media / (η · g · v)
massa_requerida = max(massa_energia, massa_potencia_media)
```

A função preserva a massa associada ao pico como diagnóstico, mas não a utiliza na restrição principal. Isso só é válido se `P_solicitada` for explicitamente um pico atendido por inversor/barramento e não uma potência mecânica contínua exigida da massa.

### Reprodução obrigatória da diretriz

Entradas: `1 Wh`, `1000 W`, `3600 s`, `10 m`, `η=0,50`, `v=0,02 m/s`.

- Energia: `3600 J`.
- Massa pela energia: `3600/(0,5·9,81·10) = 73,39 kg`.
- Potência média: `1 W`.
- Massa pela potência média: `1/(0,5·9,81·0,02) = 10,19 kg`.
- Massa pela potência contínua de 1000 W: `1000/(0,5·9,81·0,02) = 10.193,68 kg`.
- Massa principal atual: `73,39 kg`.

**Impacto:** a interface pode sugerir atendimento de 1000 W por uma massa de 73,39 kg, embora essa massa não sustente 1000 W mecanicamente a 0,02 m/s. O resultado só é defensável se existir explicitamente um buffer que forneça o pico e se a duração/energia do pico forem modeladas.

**Correção recomendada:** separar formalmente `potência média`, `potência contínua da massa`, `potência de pico`, `duração do pico`, `potência do inversor` e `potência do banco. O critério de atendimento deve verificar energia, potência contínua, pico, duração e buffer separadamente.

## P0-02 — consistência geométrica e temporal

**Arquivos:** `model/inverse_design.py`, `model/dimensioning.py`, `model/geometry.py`, `simulation/simulator.py`, `app.py`  
**Status:** confirmado como risco semântico.

O modelo mecânico do plano inclinado usa comprimento `L`, ângulo `θ` e altura `H=L·sen(θ)`. Já o dimensionamento inverso recebe `altura_m` e `velocidade_descida_m_s`, mas não recebe `θ` nem informa se a velocidade é ao longo do trilho ou vertical.

A expressão atual de potência mecânica implícita é `P=m·g·v`. Ela só é consistente se `v` for velocidade vertical. Se `v` for velocidade ao longo do trilho, a expressão deve usar `v·sen(θ)`.

**Impacto:** a mesma velocidade numérica pode produzir resultados diferentes conforme a interpretação. O tempo de descarga também deve satisfazer `t=L/v_trilho` ou `t=H/v_vertical`.

**Correção recomendada:** renomear as grandezas (`v_trilho`, `v_vertical`), incluir a relação geométrica na API, verificar `H`, `L`, `θ`, `v` e duração conjuntamente, e emitir aviso quando a duração prescrita não coincidir com a trajetória.

## P0-03 — torque eletromagnético e perdas

**Arquivos:** `model/electromechanics.py`, `model/electromechanical_coupling.py`  
**Status:** confirmado como lacuna física.

`previa_carga_resistiva` calcula a potência da carga externa:

```text
P_carga = fases · 0,5 · I_pico² · R_carga
P_cc = η_retificador · P_carga
τ = P_carga / |ω|
```

A resistência de fase entra no denominador da corrente, mas a dissipação de cobre não é adicionada ao torque eletromagnético. O torque calculado representa somente a potência na carga externa, enquanto a potência eletromagnética retirada do eixo deveria, quando aplicável, incluir:

```text
P_em = P_carga + P_cobre
τ_em = P_em / |ω|
```

Também é necessário confirmar se a ponte de diodos, a queda direta, o número de fases e o deslocamento angular estão representados pela aproximação usada. O código declara que a forma de onda e o retificador são hipóteses reduzidas.

**Impacto:** potência e torque podem estar subestimados e o acoplamento mecânico pode não fechar o balanço.

**Correção recomendada:** registrar separadamente FEM, cobre, carga, retificador e potência eletromagnética; só aplicar cada eficiência uma vez; documentar a convenção de fases para motor de passo bipolar.

## P0-04 — integrador dinâmico

**Arquivo:** `simulation/electromechanical_dynamic.py`  
**Status:** confirmado.

A aceleração é calculada por:

```python
a = max(0.0, (forca_disponivel - forca_carga) / massa)
```

Quando o torque elétrico supera a força disponível, a aceleração é artificialmente zerada. Isso impede desaceleração física, embora a trajetória possa continuar avançando com velocidade existente.

**Impacto:** o modelo não representa corretamente frenagem, parada ou equilíbrio dinâmico. A ponte de diodos não pode ser avaliada como freio se o integrador elimina aceleração negativa.

**Correção recomendada:** integrar aceleração assinada, impor `v >= 0`, tratar o evento de parada, torque estático/retenção e limite da rampa, e testar convergência ao reduzir `passo_s`.

## P1-01 — ciclo completo

**Arquivos:** `simulation/cycle.py`, `model/energy_chain.py`, `app.py`  
**Status:** parcialmente implementado; requer auditoria.

`balanço_transformacoes` fornece um produto de eficiências por etapas, mas isso não substitui o ciclo completo. A documentação deve separar:

- energia elétrica consumida na subida;
- energia potencial armazenada;
- energia elétrica recuperada na descida;
- perdas por etapa;
- eficiência de ida e volta;
- potência e duração de subida e descida.

Não se deve chamar a energia mecânica de V0.4 de energia elétrica nem somar uma eficiência que já foi aplicada dinamicamente.

## P1-02 — modularidade

**Arquivos:** `model/dimensioning.py`, `model/inverse_design.py`, `app.py`  
**Status:** parcialmente implementado.

O dashboard já mostra módulos em paralelo, mas a soma linear ainda é idealizada. Faltam estados explícitos para módulos disponíveis, simultâneos, sequenciais, limites de recarga, limites de descarga, resposta e energia disponível após cada evento.

**Correção recomendada:** validar o banco contra potência e energia em cada evento e impedir declaração de atendimento se um requisito obrigatório não for satisfeito.

## P1-03 — curtailment e serviços

**Arquivos:** `app.py`, `docs/tcc/14_explorador_de_aplicacoes.md`, documentação nova do dashboard  
**Status:** parcialmente implementado.

O dashboard já possui entrada de excedente e duração. Deve distinguir:

1. excedente identificado;
2. energia absorvível pelo banco;
3. energia recuperável depois das perdas;
4. curtailment efetivamente mitigado.

O quarto item só pode ser calculado com modelo operacional e dados de rede. Inicialmente, os eventos devem ser sintéticos e rotulados como hipóteses.

## P1-04 — bibliografia e evidências

**Arquivos:** `docs/tcc/bibliografia.md`, `docs/tcc/fontes_por_secao.md`, `docs/tcc/04_modelo_eletromecanico.md`  
**Status:** precisa auditoria documental.

A existência de uma referência no arquivo não prova que ela foi lida ou sustenta a afirmação usada. A matriz de evidências deve relacionar cada afirmação a fonte, código, teste, cenário, figura e limitação.

## Lacunas de testes

A suíte cobre entradas, mecânica, dimensionamento, relatórios e interface básica, mas ainda faltam testes independentes para:

- incompatibilidade entre potência média, pico e duração;
- velocidade no trilho versus velocidade vertical;
- conservação de energia com torque eletromagnético;
- cobre + carga + retificador;
- desaceleração e parada;
- convergência do integrador;
- subida e descida em ciclo completo;
- módulos disponíveis versus módulos exigidos;
- absorção de excedente versus curtailment mitigado;
- cenários de eficiência parcial.

## Arquivos que deverão ser modificados na Passagem B

- `model/inverse_design.py`;
- `model/dimensioning.py`;
- `model/electromechanics.py`;
- `model/electromechanical_coupling.py`;
- `simulation/electromechanical_dynamic.py`;
- `simulation/cycle.py`;
- `model/energy_chain.py`;
- `app.py`;
- testes correspondentes;
- documentação técnica e matriz de evidências.

## Plano ordenado de correção

1. Fixar semântica de velocidade, altura, comprimento e duração.
2. Separar potência média, contínua, pico, inversor e buffer.
3. Corrigir e testar torque eletromagnético incluindo perdas de cobre.
4. Corrigir integrador para aceleração assinada, frenagem e parada.
5. Fechar ciclo de recarga e descarga com balanço de ida e volta.
6. Validar modularidade contra energia, potência e tempo de resposta.
7. Reorganizar serviços de curtailment com cenários sintéticos rotulados.
8. Auditar fontes e completar matriz de evidências.
9. Só então revisar a interface e criar novos cenários.

## Critério de parada da Passagem A

Nenhuma correção física foi aplicada nesta auditoria. A próxima etapa deve aguardar aprovação da IA coordenadora científica e então executar a Passagem B com testes antes/depois.

## Resultado da Passagem B autorizada

A IA coordenadora autorizou a correção P0. Foram alterados `model/inverse_design.py`, `model/electromechanics.py`, `simulation/electromechanical_dynamic.py`, a chamada correspondente em `app.py` e adicionados testes independentes em `tests/test_correcoes_p0.py`. O relatório detalhado antes/depois está em `17_correcoes_p0_e_verificacao.md`.

A suíte passou de 68 para 71 testes. As prioridades P1 continuam pendentes e não foram implementadas nesta passagem.
