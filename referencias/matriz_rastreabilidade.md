# Matriz de rastreabilidade bibliográfica inicial

| Pergunta científica | Equação/modelo GravBat | Referência candidata | Hipótese a conferir | Evidência GravBat | Lacuna | Ação |
|---|---|---|---|---|---|---|
| Como a inclinação altera o percurso para o mesmo desnível? | `L = H/sen(theta)` | REF-001, REF-002 | Arquitetura inclinada e definição de percurso | E2 calculado | Conferir se a literatura usa o mesmo percurso útil | Ler texto integral e comparar variáveis |
| Como mudam força e rolamento? | `F_g`, `F_rol`, `E_rol` | REF-001 | Coeficiente equivalente e resistência | E2 calculado | Parâmetros não transferíveis automaticamente | Extrair hipóteses e unidades |
| Qual referência vertical é adequada? | `E_g = m g H` | REF-003, REF-005 | Massa suspensa, poço e perdas próprias | E1 calculado | Equipamentos verticais não têm as mesmas perdas de trilho | Comparar arquiteturas sem equiparar perdas artificialmente |
| Como torque e dinâmica afetam potência? | modelo V0.4 | REF-001, REF-007 | Transmissão, inércia e carga | E3 calculado | E3 é torque constante e não motor real | Identificar modelos de carga na literatura |
| Como ocorre a conversão elétrica? | modelo eletromecânico E4 | REF-006, REF-007 | FEM, resistência, retificação e controle | E4 simulado | Parâmetros elétricos hipotéticos | Buscar referências específicas de máquina e retificador |
| Como a escala modular deve ser interpretada? | `E = N m g H` | REF-004, REF-009 | Independência e ciclo | E5 calculado/sintético | Sem potência, estrutura ou economia | Usar apenas ordem de grandeza |
| Como conectar armazenamento a renováveis? | série sintética E5 | REF-008, REF-009 | Flexibilidade e despacho | E5 simulado | Não representa SIN nem curtailment real | Fundamentar contexto, não validar cenário |
