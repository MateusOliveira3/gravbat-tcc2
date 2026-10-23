# Guia de reprodução para o orientador

## Requisitos

Windows com Python 3.11 ou compatível, Git opcional e acesso à pasta do projeto. As versões declaradas estão em `requirements.txt` (`streamlit==1.64.0`, `plotly==6.9.0`).

## Instalação limpa

Na raiz do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Testes

```powershell
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
```

O resultado esperado no ambiente auditado foi 88 testes, 87 aprovações e um erro ambiental de limpeza temporária do Windows. Uma falha diferente deve ser investigada.

## Executar o dashboard

```powershell
.\.venv\Scripts\python.exe -B -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Abra `http://127.0.0.1:8501/`. Na demonstração, conferir parâmetros, modo de descida livre, velocidade-alvo, Executar/Pausar/Reiniciar, barra de progresso, gráfico e menu de auditoria.

## Reproduzir as conclusões principais

- E1: conferir `E_g=m g H` nos relatórios e em `model/energy.py`.
- E2: conferir `H=L sen(theta)`, `L=H/sen(theta)`, forças e rolamento em `model/geometry.py` e `model/mechanics.py`.
- E3: conferir o acoplamento V0.4 em `model/coupling.py`, incluindo limite de torque e balanço energético.
- E4: conferir a integração em `simulation/electromechanical_dynamic.py` e o equivalente de gerador em `model/electromechanics.py`.
- E5: conferir a conversão de joules para kWh no relatório `docs/tcc/resultado_e5_escalabilidade_ciclo.md` e a série sintética documentada.

## Interpretação recomendada

Apresentar E1–E5 como resultados calculados ou simulados sob hipóteses declaradas. A comparação vertical de 90° é limite geométrico/energético ideal, não um equipamento vertical completo. Nenhum resultado deve ser descrito como validação experimental ou como demonstração de viabilidade estrutural/econômica.
