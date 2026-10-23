# Plano de correção visual do GravBat

Este plano orienta correções pequenas após a auditoria de 20/10/2026. Não autoriza alteração de modelos físicos, equações, parâmetros ou resultados E1–E5.

## Etapa 1 — acesso e smoke test da tela

**Ação:** iniciar o Streamlit no `.venv` e confirmar abertura em navegador real.  
**Aceitação:** a página inicial abre sem exceção; o modo padrão não renderiza a auditoria técnica; o menu secundário fica acessível.

## Etapa 2 — estabilização da integração da animação

**Ação:** revisar o teste de integração e a serialização da transformação do carro, sem mudar a geometria física.  
**Aceitação:** a suíte não apresenta falha funcional no teste da animação; a transformação gerada e a expectativa do teste usam a mesma convenção.

## Etapa 3 — verificação geométrica estática

**Ação:** inspecionar os quadros `s=0`, `s=L/2` e `s=L` para 10°, 30° e 40°, em comprimento fixo e desnível fixo.  
**Aceitação:** centro do carro está no segmento entre topo e base; as duas rodas coincidem com os dois perfis; nenhuma parte do carro fica acima ou afastada do trilho; o cabo permanece contínuo.

## Etapa 4 — teste interativo dos controles

**Ação:** executar, pausar, retomar, reiniciar e arrastar a barra. Repetir para descida livre e velocidade-alvo.  
**Aceitação:** massa, cabo, tambor, indicadores e marcador do gráfico usam o mesmo instante; pausar congela todos; reiniciar retorna ao início; fim da trajetória não ultrapassa `s=L`.

## Etapa 5 — revisão de apresentação

**Ação:** conferir desktop e tela estreita.  
**Aceitação:** seis indicadores legíveis, duas colunas sem cortes, unidades visíveis, contraste adequado e aviso de autonomia compreensível.

## Etapa 6 — revisão científica para a demonstração

**Ação:** ensaiar a explicação com o orientador.  
**Aceitação:** fica explícito que o dashboard é um instrumento computacional; potência útil é estimada; E4 é um modelo eletromecânico equivalente; a transmissão é esquemática; E5 é hipotético; não há validação experimental do protótipo.

## Checklist final

- [ ] Página abre no navegador real.
- [ ] Parâmetros preservam estado.
- [ ] Geometria passa nos três pontos e nos ângulos de aceitação.
- [ ] Cabo, tambor e engrenagens acompanham o movimento.
- [ ] Gráfico e indicadores sincronizam.
- [ ] Controles funcionam nos dois modos.
- [ ] Auditoria técnica permanece secundária.
- [ ] Testes funcionais passam; erros ambientais estão separados.
- [ ] Nenhum resultado E1–E5 foi alterado.

