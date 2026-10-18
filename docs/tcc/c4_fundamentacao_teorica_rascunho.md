# C4 — Fundamentação teórica (rascunho)

## 2 Integração de fontes renováveis variáveis

Fontes solar e eólica dependem de condições meteorológicas e apresentam produção variável. A integração requer coordenação entre geração, rede, demanda e recursos de flexibilidade. A IEA identifica a expansão renovável e a necessidade de flexibilidade como questões sistêmicas, sem que suas projeções globais possam ser transferidas diretamente ao SIN [1]. No Brasil, EPE e ONS fornecem o contexto institucional específico [2,3].

## 3 Flexibilidade, armazenamento e curtailment

Armazenamento desloca energia entre momentos de carga e disponibilidade, podendo fornecer potência, reserva ou suavização. Curtailment é uma redução operativa da geração disponível. No SIN, o ONS distingue razão energética, confiabilidade e indisponibilidade externa [3]. Logo, uma bateria gravitacional pode ser estudada como recurso potencial de flexibilidade, mas o presente trabalho não calcula despacho, fluxo de potência ou redução real de cortes.

## 4 Princípios do armazenamento gravitacional

A energia potencial gravitacional é $E_g=m g H$. Para uma massa de 1.000 kg e $H=800$ m, E1 calcula aproximadamente 2,180 kWh ideais. Esse valor é um limite energético mecânico antes de perdas e conversão. A energia útil condicionada a uma eficiência $\eta$ seria $E_u=\eta E_g$, mas $\eta$ precisa ser explicitamente assumida e não é uma propriedade universal do sistema.

## 5 Arquiteturas gravitacionais

Sistemas verticais podem usar torres, poços ou massas suspensas; sistemas inclinados podem usar trilhos, cabos ou veículos sobre encostas. Zhang et al. [4] discutem arquiteturas de encosta e montanha, enquanto Qin et al. [5] analisam fatores de eficiência em armazenamento ferroviário. As arquiteturas compartilham a relação $m g H$, mas diferem em percurso, forças, transmissão, ocupação espacial, segurança e perdas. Não se presume que perdas de uma arquitetura sejam iguais às de outra.

## 6 Mecânica do plano inclinado

Para uma massa em uma rampa de comprimento $L$ e ângulo $\theta$:

$$H=L\sin\theta,$$
$$F_g=m g\sin\theta,$$
$$F_{rol}=c_r m g\cos\theta.$$

Com desnível fixo, $L=H/\sin\theta$. O trabalho de rolamento no modelo E2 é $E_{rol}=F_{rol}L=c_r m g H\cot\theta$. A força motriz líquida é positiva somente quando $\tan\theta>c_r$. Essas relações são deduções analíticas sob o coeficiente de rolamento assumido; não representam automaticamente atrito estático, deformação, curva ou irregularidade de uma instalação real.

## 7 Trabalho, potência e dinâmica

Trabalho mecânico é força aplicada ao longo do deslocamento. Potência média é $P=E/t$, enquanto potência instantânea depende do estado dinâmico. No E3, o modelo V0.4 usa torque resistente constante e

$$F_{carga}=\frac{G\tau}{\eta_t r_d},\qquad a=\frac{F_0-F_{carga}}{m}.$$

O torque limite é $\tau_{lim}=\eta_t r_d F_0/G$. O ponto $\tau=(2/3)\tau_{lim}$ maximiza a potência média somente sob as hipóteses do modelo: percurso fixo, partida do repouso, torque constante e parâmetros invariantes. Não é uma regra geral para máquinas reais ou controle variável.

## 8 Perdas e transmissão

As perdas são separadas por mecanismo. No E3, $E_{rol}$ representa o trabalho de rolamento; $E_{carga}=F_{carga}L$ é o trabalho absorvido na entrada da transmissão; a energia no eixo é $E_{eixo}=\eta_t E_{carga}$ e a perda de transmissão é $(1-\eta_t)E_{carga}$. No E4, perdas de cobre, carga e retificação pertencem ao modelo eletromecânico equivalente. Esses termos não devem ser somados como se fossem medições de uma máquina real.

## 9 Conversão eletromecânica

Uma máquina elétrica converte potência mecânica em elétrica por meio de torque, velocidade, fluxo e resistência. O E4 reduz essa cadeia a parâmetros equivalentes, incluindo constante de FEM, resistência de fase, carga e retificação. O modelo é calculado/simulado sob hipóteses documentadas e não caracteriza um gerador físico. Motor de passo, encoder, PWM e frenagem controlável constituem arquitetura conceitual futura; não foram demonstrados como sistema implementado nesta fase.

## 10 Escala e aplicações conceituais

A capacidade de módulos independentes soma-se idealmente como $E_{tot}=N m g H$. E5 mostra que a soma de módulos não garante potência, disponibilidade, recarga, estrutura ou rendimento de ciclo. O cenário sintético de excedente solar/eólico ilustra uma possível aplicação de absorção temporal, mas não mede curtailment nem comprova benefício no SIN.

## Referências citadas

[1] IEA. *Renewables 2025 — Renewable electricity*.

[2] EPE. *Anuário Estatístico de Energia Elétrica 2026*.

[3] ONS. *Diagnóstico e perspectiva da evolução dos cortes de geração no Brasil*. RT DGL-ONS 0189/2025.

[4] ZHANG, J. et al. 2024. DOI: 10.19799/j.cnki.2095-4239.2023.0667.

[5] QIN, T. et al. 2023. DOI: 10.19799/j.cnki.2095-4239.2022.0634.
