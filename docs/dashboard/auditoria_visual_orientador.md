# Auditoria visual do GravBat para apresentação ao orientador

Data da auditoria: 20/10/2026  
Escopo: inspeção crítica da aplicação existente, sem alterações em código, modelos, equações, resultados ou testes.

## Método e limitações da inspeção

O projeto foi inspecionado na raiz do repositório. O ambiente virtual `.venv` está presente e o Streamlit está instalado (versão 1.64.0). A aplicação foi iniciada com:

```powershell
.\.venv\Scripts\python.exe -B -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

O processo iniciou o servidor, mas o navegador disponível no ambiente não conseguiu abrir `http://127.0.0.1:8501`, retornando `ERR_CONNECTION_REFUSED`. Portanto, não foi possível realizar inspeção visual interativa da página, dos controles ou da animação. As avaliações visuais abaixo são uma auditoria estática do código e dos contratos dos componentes, e não devem ser tratadas como aprovação visual.

Também foi executada a suíte existente com o ambiente virtual:

- 86 testes executados;
- 84 aprovados;
- 1 falha funcional no teste de integração da animação, relacionada à expectativa de nomenclatura da transformação;
- 1 erro ambiental conhecido de limpeza de diretório temporário do Windows (`WinError 5`).

## Estrutura observada

O modo padrão é controlado por `st.session_state` e renderiza a visão compacta. `Parâmetros` e o menu `⋯` são `st.popover`; a auditoria técnica é renderizada apenas quando o estado de auditoria está ativo. A tela compacta contém seis indicadores, seleção de trajetória, componente HTML/SVG com rampa e gráfico, controles locais de reprodução e aviso de autonomia.

## Problemas classificados

### P0 — impede demonstração ou apresenta comportamento incorreto

1. **Servidor não acessível pelo navegador de validação.** A aplicação iniciou o processo, mas a inspeção interativa não foi concluída. Para a apresentação, é indispensável confirmar a abertura em um navegador real.

2. **Falha no teste de integração da animação.** A suíte reportou uma falha em `test_componente_interativo_tem_relogio_e_controles`, que espera uma forma textual específica para a rotação. Mesmo que a transformação gerada seja matematicamente equivalente, a integração não está completamente estabilizada enquanto esse teste falhar.

3. **Geometria dinâmica ainda exige validação visual.** O código usa interpolação entre os pontos do trilho e rodas em perfis paralelos, mas não houve confirmação visual de que o carro permanece apoiado em `s=0`, `s=L/2` e `s=L`, especialmente no cenário de baixa inclinação `L=11,52 m`, `H=2 m`, `θ=10°`.

### P1 — prejudica significativamente a experiência

1. **A distinção entre descida livre e velocidade-alvo depende de controles textuais.** A interface rotula a trajetória, mas a demonstração precisa deixar evidente que a velocidade-alvo é hipótese cinemática e não controlador validado.

2. **A sincronização do gráfico não pode ser considerada comprovada visualmente.** O componente HTML atualiza massa, cabo, indicadores e marcador a partir de um relógio JavaScript, porém a sincronização precisa ser observada em início, meio, fim, pausa, retomada e arraste.

3. **A transmissão é esquemática.** O código mostra engrenagens e relação `G=5:1`, mas a apresentação deve manter explícito que não se trata de um dimensionamento construtivo nem de uma medição de gerador.

4. **A visão compacta ainda contém muitos significados no mesmo espaço.** Indicadores, trajetória, gráfico, controles e aviso competem pela atenção. Isso pode dificultar a explicação em 30 segundos, sobretudo em notebook.

### P2 — acabamento e melhorias secundárias

1. Padronizar unidades e casas decimais nos indicadores dinâmicos.
2. Garantir que cotas, rótulos do tambor e texto de transmissão não sejam cortados em ângulos extremos.
3. Confirmar contraste e tamanho dos controles em tema escuro em desktop e tela estreita.
4. Ajustar a escala vertical do gráfico para manter leitura clara em trajetórias muito curtas ou muito longas.

## Avaliação para o primeiro contato do orientador

1. **Entendimento em 30 segundos:** provavelmente sim pela presença do título, indicadores e desenho, mas isso depende da inspeção visual real e de uma legenda curta explicando potencial, potência estimada e trajetória.
2. **Alteração de parâmetro e consequência:** o código prevê essa interação, mas não foi possível confirmá-la no navegador.
3. **Distinção epistemológica:** está parcialmente explícita nos rótulos e captions; deve ser reforçada na demonstração para separar calculado, simulado e hipotético.
4. **Riscos à credibilidade:** afirmar sincronização ou funcionamento dos controles sem teste visual; apresentar a transmissão esquemática como equipamento dimensionado; confundir potência útil estimada com potência elétrica medida.
5. **Indispensável antes da apresentação:** abrir a aplicação em navegador real, validar os três pontos da trajetória, testar controles, confirmar o marcador do gráfico e resolver a falha do teste de integração.
6. **Pode ficar para depois:** refinamentos de tipografia, catálogo detalhado, animação de engrenagens mais sofisticada e melhorias de exportação, desde que não afetem a interpretação física.

## Proposta de layout final

Manter a arquitetura atual, sem novos modelos:

1. Cabeçalho compacto com GravBat, subtítulo, `Parâmetros` e menu `⋯`.
2. Duas linhas de três indicadores essenciais.
3. Duas colunas principais: representação mecânica à esquerda e gráfico sincronizado à direita.
4. Controles de reprodução imediatamente abaixo das duas visualizações.
5. Tempo, posição e velocidade atuais em uma única linha dinâmica.
6. Aviso de autonomia e limitações abaixo do componente.
7. Auditoria técnica somente pelo menu secundário.

## Critério de pronto para apresentação

O dashboard só deve ser declarado pronto quando:

- abrir sem erro em navegador real;
- parâmetros puderem ser abertos e fechados sem perda de estado;
- massa, inclinação e geometria recalcularem os indicadores;
- `s=0`, `s=L/2` e `s=L` mostrarem o carro apoiado nos trilhos;
- cabo e tambor permanecerem coerentes durante a reprodução;
- Executar, Pausar, Reiniciar e barra de progresso produzirem mudanças observáveis;
- o marcador do gráfico acompanhar o mesmo instante físico;
- descida livre e velocidade-alvo permanecerem claramente separadas;
- auditoria técnica abrir sem renderizar conteúdo pesado no modo padrão;
- testes da aplicação não apresentarem falhas funcionais conhecidas;
- limitações de eficiência, controle e validação experimental permanecerem explícitas.

