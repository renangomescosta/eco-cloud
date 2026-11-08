"""
Região 03 - França
Fonte: RTE éCO2mix tempo real, via portal ODRE (JSON, MW, a cada 15 min)

Rodar: python3 regiao_03_fr.py

Observações:
  - Os registros mais recentes vêm com geração null (o dataset já traz as
    linhas de previsão). O script pega o mais recente que tenha dado medido.
  - pompage (bombeamento, negativo) fica de fora.
  - Imprime também o taux_co2 calculado pela própria RTE, para comparação.
"""

from comum import baixar_json, calcular, imprimir

URL = ("https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
       "eco2mix-national-tr/records?order_by=date_heure%20desc&limit=100")

CAMPOS = {
    "fioul": "oleo",
    "charbon": "carvao",
    "gaz": "gas",
    "nucleaire": "nuclear",
    "eolien": "eolica",
    "solaire": "solar",
    "hydraulique": "hidraulica",
    "bioenergies": "biomassa",
}


def coletar():
    dados = baixar_json(URL)
    medidos = [r for r in dados["results"] if r.get("nucleaire") is not None]
    if not medidos:
        raise ValueError("nenhum registro com dado medido nos últimos 100")
    reg = medidos[0]  # já vem ordenado do mais recente para o mais antigo

    mix = {}
    for campo, fonte in CAMPOS.items():
        mix[fonte] = mix.get(fonte, 0) + (reg.get(campo) or 0)

    r = calcular(mix)
    r["taux_co2_rte"] = reg.get("taux_co2")
    return [("França", reg["date_heure"], r)]


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
        print(f"{'':22} (RTE informa {r['taux_co2_rte']} gCO2/kWh)")
