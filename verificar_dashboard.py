"""Smoke test de execução Streamlit; não substitui inspeção do navegador.

Uso: .venv/Scripts/python.exe -B verificar_dashboard.py
"""
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest


def main(saida=None):
    raiz = Path(__file__).resolve().parent
    saida = Path(saida) if saida is not None else raiz / "outputs" / "v02"
    saida.mkdir(parents=True, exist_ok=True)
    app = AppTest.from_file(str(raiz / "app.py"), default_timeout=30).run()
    registros = []

    def conferir(nome, esperado, tempo_aplicavel=True):
        assert not app.exception, [e.message for e in app.exception]
        metricas = {m.label: m.value for m in app.metric}
        assert len(app.get("plotly_chart")) == 11
        for chave, valor in esperado.items():
            assert metricas[chave] == valor, (nome, chave, metricas[chave], valor)
        if tempo_aplicavel:
            assert metricas["Tempo de descida"] != "Não aplicável"
        registros.append({"cenario": nome, "metricas": metricas, "graficos": 11,
                          "avisos": [w.value for w in app.warning], "excecoes": 0})

    conferir("laboratorio", {"Comprimento L": "1,2 m", "Desnível H": "0,208378 m"})
    app.radio(key="modo").set_value("Terreno · H fixo").run()
    conferir("terreno", {"Desnível H": "1 m", "Energia potencial inicial": "58,86 J"})
    app.number_input(key="cr").set_value(1.0).run()
    conferir("NAO_DESCE", {"Tempo de descida": "Não aplicável", "Velocidade · repouso": "0 m/s",
                           "Perda por rolamento": "0 J", "Energia dissipada por rolamento": "0 %"}, False)
    assert any("NAO_DESCE" in w.value for w in app.warning)
    app.number_input(key="massa").set_value(0.0).run()
    assert not app.exception and len(app.error) == 1
    assert "massa_kg" in app.error[0].value and not app.metric
    registros.append({"cenario": "massa invalida", "erro_explicito": app.error[0].value, "excecoes": 0})
    (saida / "smoke_streamlit.json").write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK: laboratorio, terreno, NAO_DESCE e massa invalida. AppTest automatizado; sem inspecao visual.")


if __name__ == "__main__":
    main()
