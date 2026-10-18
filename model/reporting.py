"""Relatórios reproduzíveis de cenário para o dashboard."""
from datetime import datetime, timezone
import json
import csv
import io


def relatorio_cenario(entradas, resultados, hipoteses, limitacoes, versao="V0.9"):
    """Monta um registro serializável, sem converter hipóteses em medições."""
    return {
        "versao_modelo": versao,
        "instante_utc": datetime.now(timezone.utc).isoformat(),
        "classificacao": {
            "entradas": "HIPÓTESE / CONFIGURÁVEL",
            "resultados": "CALCULADO ou SIMULADO",
            "validacao": "NÃO EXPERIMENTAL",
        },
        "entradas": entradas,
        "resultados": resultados,
        "hipoteses": list(hipoteses),
        "limitacoes": list(limitacoes),
    }


def serializar_relatorio(relatorio):
    return json.dumps(relatorio, ensure_ascii=False, indent=2, sort_keys=False)


def serializar_tabela_relatorio(relatorio):
    """Exporta uma tabela plana para planilhas e anexos do TCC."""
    linhas = []
    for grupo in ("entradas", "resultados"):
        valores = relatorio.get(grupo, {})
        for chave, valor in valores.items():
            if isinstance(valor, (dict, list)):
                valor = json.dumps(valor, ensure_ascii=False)
            linhas.append({"grupo": grupo, "parametro": chave, "valor": valor,
                           "classificacao": relatorio["classificacao"].get("entradas" if grupo == "entradas" else "resultados", "")})
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["grupo", "parametro", "valor", "classificacao"])
    writer.writeheader()
    writer.writerows(linhas)
    return out.getvalue()


def serializar_trajetoria(estados):
    """Exporta a trajetória dinâmica em CSV com unidades indicadas no cabeçalho."""
    campos = [
        ("tempo_s", "tempo (s)"),
        ("posicao_m", "posição (m)"),
        ("velocidade_m_s", "velocidade (m/s)"),
        ("aceleracao_m_s2", "aceleração (m/s²)"),
        ("omega_saida_rad_s", "velocidade angular (rad/s)"),
        ("torque_eletromagnetico_Nm", "torque eletromagnético (N·m)"),
        ("potencia_ac_W", "potência AC (W)"),
        ("energia_acumulada_J", "energia AC acumulada (J)"),
        ("perda_cobre_acumulada_J", "perda de cobre acumulada (J)"),
    ]
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow([rotulo for _, rotulo in campos])
    for estado in estados:
        writer.writerow([estado.get(chave, "") for chave, _ in campos])
    return out.getvalue()


def serializar_transformacoes(etapas):
    """Exporta o balanço energético por transformação em CSV."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["etapa", "entrada (J)", "saída (J)", "perda (J)", "eficiência", "status"])
    for etapa in etapas:
        writer.writerow([etapa.nome, etapa.entrada_J, etapa.saida_J,
                         etapa.perda_J, etapa.eficiencia, etapa.status])
    return out.getvalue()
