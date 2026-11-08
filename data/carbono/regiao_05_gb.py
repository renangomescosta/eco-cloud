"""
Região 05 - Reino Unido (Grã-Bretanha)
Fonte: NESO Carbon Intensity API (JSON, % por fonte, a cada 30 min)

Rodar: python3 regiao_05_gb.py

Observações:
  - A API entrega percentuais, não MW. O cálculo usa as proporções
    (o total impresso pelo comum.py não é MW, é a soma dos percentuais).
  - imports fica de fora (não é geração local); os demais são renormalizados.
"""

from comum import baixar_json, calcular, imprimir

URL = "https://api.carbonintensity.org.uk/generation"

COMBUSTIVEIS = {
    "biomass": "biomassa",
    "coal": "carvao",
    "gas": "gas",
    "nuclear": "nuclear",
    "other": "outros",
    "hydro": "hidraulica",
    "solar": "solar",
    "wind": "eolica",
}


def coletar():
    dados = baixar_json(URL)["data"]
    mix = {}
    for item in dados["generationmix"]:
        fonte = COMBUSTIVEIS.get(item["fuel"])
        if fonte:  # imports e desconhecidos ficam de fora
            mix[fonte] = mix.get(fonte, 0) + item["perc"]
    return [("Reino Unido", dados["from"], calcular(mix))]


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
