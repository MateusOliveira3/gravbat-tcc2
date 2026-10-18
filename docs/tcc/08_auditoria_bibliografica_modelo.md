# Auditoria bibliográfica das hipóteses do modelo

## Objetivo

Verificar se as simplificações utilizadas no GravBat são compatíveis com modelos e revisões técnicas publicados, sem transformar revisão bibliográfica em validação experimental.

## Armazenamento gravitacional

Cai et al. (2024, DOI `10.1002/wene.543`) revisam arquiteturas, avaliação técnico-econômica e integração de sistemas gravitacionais. A fonte é adequada para justificar o uso de `mgh` como princípio energético e para contextualizar que sistemas de massa sólida ainda têm maturidade e avaliação econômica limitadas. Ela não fornece parâmetros do GravBat nem demonstra viabilidade de um terreno específico.

Wang et al. (2025, DOI `10.3390/en18071812`) revisam sistemas líquidos e sólidos, incluindo arquiteturas em trilhos e montanhas. A fonte sustenta a comparação de arquiteturas e a necessidade de considerar eficiência, infraestrutura, investimento e uso do terreno. Não sustenta a afirmação de que armazenamento gravitacional elimina curtailment.

## Máquinas elétricas

A revisão de modelos analíticos de máquinas de ímã permanente (Electric Power Systems Research, 2013) sustenta a escolha de níveis de modelagem com diferentes compromissos entre complexidade e precisão. Isso apoia o uso inicial de um modelo equivalente por fase, enquanto dados do motor e a pergunta científica não exigirem um modelo eletromagnético mais detalhado.

O manual técnico da Oriental Motor permanece a fonte primária para estrutura, fases, FEM e torque de motores de passo. O manual e a revisão não identificam o motor físico do GravBat; seus parâmetros continuam **A DEFINIR** até datasheet ou medição.

## Consequência para o modelo atual

As hipóteses `E = mgh`, FEM proporcional à velocidade em circuito aberto, resistência de fase, potência `τ·ω` e perdas separadas são adequadas como modelo inicial de ordem reduzida, desde que sejam classificadas como **TEÓRICO/ANALÍTICO**, **HIPÓTESE** ou **CALCULADO** quando não houver dado do componente. A literatura sustenta o princípio e o nível de modelagem; a validade quantitativa do protótipo ainda depende de parâmetros rastreáveis e futura validação experimental.
