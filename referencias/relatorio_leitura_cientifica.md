# Relatório de leitura científica — referências prioritárias

## Estado da aquisição

A consulta foi feita em DOI, páginas oficiais da revista e repositório institucional. Nenhum PDF foi copiado para `referencias/pdfs_locais/` nesta etapa: os links localizados não permitiram confirmar simultaneamente download legal, termos de uso e autorização de redistribuição local.

- **REF-001:** metadados oficiais confirmados no resolvedor DOI; página de acesso direciona ao CNKI. Texto integral não consultado.
- **REF-002:** metadados oficiais confirmados no resolvedor DOI; página de acesso direciona ao CNKI. Texto integral não consultado.
- **REF-003:** registro ORA confirmado, com manuscrito aceito disponível sob termos de uso; o acesso automático retornou bloqueio 403 nesta sessão. Abstract e metadados foram consultados por páginas institucionais/editoriais.
- **REF-004:** página integral em HTML da revista consultada, incluindo resumo, parâmetros da tabela e lista de figuras; PDF não arquivado.

## REF-001 — Qin et al. (2023)

A fonte oficial confirma o artigo **Study on factors influencing rail gravity energy storage system efficiency**, publicado em *Energy Storage Science and Technology*, 12(3), 835–845, DOI `10.19799/j.cnki.2095-4239.2022.0634`. O texto integral não foi obtido; portanto não são extraídas equações, páginas, parâmetros ou resultados numéricos.

**Uso possível:** fundamentar a necessidade de estudar fatores de eficiência em sistemas ferroviários. **Não permitido nesta etapa:** transferir tendências quantitativas para E2 ou E4.

## REF-002 — Zhang et al. (2024)

A fonte oficial confirma **Gravity energy storage technology based on slopes and mountains**, *Energy Storage Science and Technology*, 13(3), 924–933, DOI `10.19799/j.cnki.2095-4239.2023.0667`. O texto integral não foi obtido.

**Uso possível:** contextualizar arquiteturas inclinadas e de montanha. **Lacuna:** ainda não há leitura de equações, hipóteses ou resultados do artigo.

## REF-003 — Morstyn et al. (2019)

A editora e o repositório Oxford confirmam **Gravity energy storage with suspended weights for abandoned mine shafts**, *Applied Energy*, 239, 201–206. O resumo informa uma arquitetura vertical com massas suspensas em poços de minas, análise de dimensionamento e separação entre capacidade de energia e potência; também menciona estudo de caso em minas do Midlands.

Essas informações sustentam a função de REF-003 como **referência vertical**, não como validação do GravBat. A arquitetura possui perdas e condicionantes próprias de suspensão e poço, portanto não deve ser comparada diretamente ao rolamento de E2 sem um modelo comum.

## REF-004 — Liu et al. (2024)

A página oficial da revista confirma **Multi-software collaborative modeling method for mechanical and electrical co-simulation of slope gravity energy storage systems**, *Energy Storage Science and Technology*, 13(9), 3266–3276, DOI `10.19799/j.cnki.2095-4239.2024.0243`.

O resumo descreve um modelo de rampa, trilhos, carro e bloco de massa construído em SolidWorks, acoplado a Adams e Simulink. A página informa uma tabela com: inclinação de 22°, massa de 3 t, velocidade de 0,5 m/s, coeficiente de rolamento 0,05, raio de pinhão 1,21394 m e motor de 16 kVA. Esses valores pertencem ao artigo e não devem ser usados como parâmetros do GravBat.

A fonte lista resultados de força na corrente, velocidade do carro, torque e velocidade angular, além de potência mecânica e elétrica em condições normais e de queda de tensão. Isso é diretamente útil para definir quais grandezas E3/E4 devem ser comparadas, mas não prova equivalência entre os modelos.

## Comparação com E1–E5

1. `E_g = m g H` é mecânica clássica e aparece como referência energética; não depende da arquitetura quando massa e desnível são iguais.
2. `L = H/sin(theta)`, `F_g = m g sin(theta)` e `F_rol = c_r m g cos(theta)` são deduções do modelo do GravBat; REF-001 e REF-004 motivam a comparação, mas não foram usados para validar esses parâmetros.
3. E3 é um modelo de torque constante; REF-004 indica modelos com carro, corrente e co-simulação, portanto a comparação é conceitual, não numérica.
4. E4 usa equivalente eletromecânico simplificado; REF-004 mostra a necessidade de acoplamento mecânico-elétrico mais detalhado em trabalhos futuros.
5. E5 permanece análise de escala hipotética; nenhuma das quatro referências autoriza afirmar viabilidade estrutural ou econômica.

## Lacunas que permanecem

- leitura integral de REF-001 e REF-002;
- acesso ao manuscrito aceito de REF-003 e conferência de páginas;
- extração integral das equações e método de validação de REF-004;
- referência específica para motor operando como gerador, retificação e torque de frenagem;
- comparação vertical × inclinada com critérios e hipóteses comuns.

## Decisão de uso

As quatro referências são suficientes para orientar a fundamentação e a matriz de rastreabilidade, mas ainda não para afirmar que a literatura valida as equações ou os resultados do GravBat. E2 continua sendo o experimento central da comparação; E3 e E4 devem ser apresentados como aprofundamentos condicionados aos seus próprios modelos.
