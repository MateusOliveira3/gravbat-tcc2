# GravBat-L1: implementação fiel do protótipo de referência

## Artefato principal

`gravbat_l1_referencia.html` é um protótipo **funcional e autocontido** (HTML, CSS, SVG e JavaScript). Abrir no Chrome/Edge com duplo clique. Não depende de bibliotecas externas, Streamlit, Python ou internet.

**Foi testado em Chromium headless** quanto a abertura, execução, pausa, arraste, reinício, alteração de modo, alteração de inclinação e atualização de gráfico. A inspeção de imagens de início/meio/fim foi feita. Não é ensaio físico nem substitui testes no Windows do usuário.

## O que deve ser copiado fielmente

1. A composição: seis métricas superiores, vista mecânica à esquerda, gráfico à direita, controles no mesmo cartão, configuração abaixo, aviso científico discreto.
2. Tema escuro e hierarquia visual do HTML, com adaptação responsiva.
3. O **mesmo relógio de reprodução** atualiza posição do carro, ancoragem do cabo, rotação esquemática do tambor, gráfico, tempo, posição e velocidade. Um único `requestAnimationFrame` move todos os elementos, sem rerun do Streamlit a cada quadro.
4. `Executar`, `Pausar`, `Reiniciar`, barra de progresso e fatores de reprodução 1×/5×/20×/100× funcionam localmente.
5. Corpo e rodas ficam num único grupo SVG rígido, posicionado a partir de um ponto do trilho e rotacionado pelo ângulo do trilho. Os perfis paralelos têm deslocamento normal, não apenas vertical.
6. Cabo vai da âncora do carro ao ponto tangencial esquemático do tambor; o comprimento visível muda com a posição. A rotação do tambor depende do deslocamento de cabo dividido pelo raio nominal; a engrenagem de saída gira em sentido oposto com razão esquemática 5:1.
7. A vista da transmissão é identificada como esquemática, fora de escala. Geometria da rampa e cotas `L`, `H`, `θ` usam escala uniforme em X e Y. As extensões visuais dos trilhos permitem acomodar rodas nos extremos e **não** alteram `L` nem o percurso físico modelado.
8. Seleção de gráfico entre velocidade × tempo e energia × posição, com cursor e ponto sincronizados.

## O que NÃO copiar do protótipo como resultado científico

O HTML calcula uma trajetória livre **analítica demonstrativa** com `a = g(senθ - c_r cosθ)`, `s = a t²/2` e `v = a t`. A aplicação GravBat deve continuar usando a trajetória que **já é produzida pelo Python** (`simulation.simulator`) e as demais convenções de seus módulos. O HTML NÃO substitui E1–E5, modelo eletromecânico, limites de torque, inércias, resistência estática, freio, PWM ou validação experimental.

O modo `velocidade-alvo` do HTML é uma **hipótese cinemática** `s = v_alvo t`; não é controle físico nem demonstração de capacidade de frenagem. O protótipo calcula uma potência de referência `m g v_alvo senθ η`, independente da descida livre; mantenha esse rótulo epistemológico e o cálculo oficial do projeto. A animação não pode sugerir que energia elétrica foi gerada ou que a autonomia foi comprovada.

## Contrato de dados entre Python e componente visual

O Python deve entregar ao componente os parâmetros e uma sequência de amostras **pré-calculadas**. Use `contrato_trajetoria_exemplo.json` como esquema ilustrativo, não como resultado de E1–E5.

- `geometry`: `L_m`, `H_m`, `theta_deg`, `travel_start_m`, `travel_end_m`.
- `mechanical`: `mass_kg`, `rolling_coefficient`, `drum_radius_m`, `gear_ratio`, `efficiency_hypothesis`.
- `trajectory`: `mode` (`free` ou `target_hypothesis`), `samples` com `t_s`, `s_m`, `v_track_m_s` e opcionalmente energias.
- `metadata`: `model_classification`, `notes`, `source`.

O JavaScript deve interpolar linearmente as amostras entre tempos vizinhos, usar `s_m` para a posição no trilho e `v_track_m_s` para os indicadores. Para dados reais, **não reconstruir uma trajetória analítica diferente no JavaScript**.

Ao mudar parâmetros no Streamlit, gere novos dados no Python e remonte/reinicialize o componente. Durante reprodução, somente JavaScript atualiza os elementos, sem nova chamada Python por quadro.

## Critérios de aceitação (bloqueantes)

- `s=0`, `s=L/2`, `s=L`: rodas sobre os perfis, cabo ancorado, carro orientado, sem teleporte.
- `θ=10°`, `30°`, `40°`, geometria com H fixo e com L fixo.
- Executar move o carro de modo fluido; pausar congela **todos** os elementos; reiniciar zera; arrastar altera o quadro; fim não ultrapassa `s=L`.
- Gráfico e carro compartilham o mesmo `t_s`.
- Trocar trajetória não mistura descida livre com velocidade-alvo hipotética.
- Um valor de `a<=0` impede execução de descida livre, com aviso.
- Não usar `setInterval` com múltiplos relógios nem `st.rerun` a cada quadro.
- Não apresentar engrenagens/tambor como projeto construtivo validado.
- Preservar `model/`, `simulation/`, equações, E1–E5, valores padrão e auditoria técnica.
- Executar testes automatizados e inspeção real no navegador; não declarar aprovação visual sem evidência.

## Integração sugerida

1. Salvar o HTML como referência imutável em `docs/dashboard/referencia/gravbat_l1_referencia.html`.
2. Criar componente HTML/JS independente em `dashboard/components/` ou adaptar o existente, reutilizando layout e algoritmo de relógio do HTML.
3. Usar `streamlit.components.v1.html(...)` (ou componente customizado adequado), passando as amostras serializadas em JSON com escape seguro para contexto `<script>`.
4. Preservar a entrada dos parâmetros no Streamlit e o cálculo em Python. Somente a visualização deve usar o relógio do navegador.
5. Adicionar testes de contrato e Playwright, quando disponível, para controles, amostras e geometria.
6. Não executar commit, merge ou push sem autorização.

## Observação de engenharia

O conjunto ilustrado não representa um sistema fisicamente completo. O deslocamento do cabo, o contato com o tambor e a razão 5:1 são representações cinemáticas. Não há cálculo do enrolamento por camadas, raio variável, flexão do cabo, contato dos dentes, torque efetivo, frenagem nem sistema de segurança funcional. Esses elementos devem permanecer fora da demonstração científica de resultados.
