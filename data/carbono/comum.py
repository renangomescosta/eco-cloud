"""Cálculo compartilhado entre as regiões. Só biblioteca padrão."""

import json
import urllib.request

# Fatores de emissão de ciclo de vida (gCO2eq/kWh), iguais para todas as regiões.
# Base: medianas do IPCC AR5 (2014), Anexo III.
# Os marcados com "suposição" NÃO vêm do IPCC: revise antes de usar no trabalho.
FATORES_EMISSAO = {
    "carvao": 820,
    "gas": 490,
    "oleo": 650,             # suposição
    "biomassa": 230,
    "solar": 48,
    "geotermica": 38,
    "hidraulica": 24,
    "nuclear": 12,
    "eolica": 11,
    "termica_agregada": 490, # suposição: térmica sem separação (ex.: ONS); usei o fator do gás
    "outros": 700,           # suposição: "Other/Others/Waste" sem detalhamento
}

RENOVAVEIS = {"hidraulica", "eolica", "solar", "biomassa", "geotermica"}
LIVRE_CARBONO = RENOVAVEIS | {"nuclear"}


def baixar_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def calcular(mix_mw):
    """mix_mw: {fonte: MW}. Negativos viram 0."""
    mix = {k: max(v or 0, 0) for k, v in mix_mw.items()}
    total = sum(mix.values())
    if total <= 0:
        raise ValueError("geração total zero")
    emissoes = sum(v * FATORES_EMISSAO[k] for k, v in mix.items())
    return {
        "total_mw": round(total, 2),
        "pct_renovavel": round(100 * sum(v for k, v in mix.items() if k in RENOVAVEIS) / total, 2),
        "pct_livre_carbono": round(100 * sum(v for k, v in mix.items() if k in LIVRE_CARBONO) / total, 2),
        "intensidade_gco2_kwh": round(emissoes / total, 1),
        "mix_mw": {k: round(v, 2) for k, v in mix.items() if v > 0},
    }


def imprimir(regiao, horario, r):
    print(f"{regiao:22} {horario}  "
          f"{r['intensidade_gco2_kwh']:>6} gCO2eq/kWh  "
          f"renovável {r['pct_renovavel']:6.2f}%  "
          f"livre de carbono {r['pct_livre_carbono']:6.2f}%")

