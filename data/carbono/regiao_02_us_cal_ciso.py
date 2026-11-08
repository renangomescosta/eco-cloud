"""
Região 02 - EUA (Califórnia, CAISO)
Fonte: CAISO Today's Outlook - fuel source (CSV, MW, a cada 5 min)

Rodar: python3 regiao_02_us_cal_ciso.py

Premissas:
  - Batteries e Imports ficam de fora (não são geração local)
  - Biogas conta como biomassa; Small hydro e Large Hydro como hidráulica
  - Other entra como "outros" (fator de emissão é suposição, ver comum.py)
  - O horário do CSV é local da Califórnia (Pacífico) e vem sem data
"""

import csv
import io
import urllib.request

from comum import calcular, imprimir

URL = "https://www.caiso.com/outlook/current/fuelsource.csv"

COLUNAS = {
    "Solar": "solar",
    "Wind": "eolica",
    "Geothermal": "geotermica",
    "Biomass": "biomassa",
    "Biogas": "biomassa",
    "Small hydro": "hidraulica",
    "Large Hydro": "hidraulica",
    "Coal": "carvao",
    "Nuclear": "nuclear",
    "Natural Gas": "gas",
    "Other": "outros",
}


def coletar():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        texto = resp.read().decode("utf-8")

    linhas = list(csv.DictReader(io.StringIO(texto)))
    # última linha com todas as colunas preenchidas
    completas = [l for l in linhas if all((l.get(c) or "").strip() for c in COLUNAS)]
    if not completas:
        raise ValueError("CSV sem linhas completas")
    ultima = completas[-1]

    mix = {}
    for coluna, fonte in COLUNAS.items():
        mix[fonte] = mix.get(fonte, 0) + float(ultima[coluna])
    return [("EUA Califórnia", f"hoje {ultima['Time']} (horário do Pacífico)", calcular(mix))]


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
