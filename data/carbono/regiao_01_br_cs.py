"""
Região 01 - Brasil (todos os subsistemas do SIN)
Fonte: ONS - balanço energético em tempo real

Rodar: python3 regiao_01_br_cs.py

Premissas:
  - Itaipu (50Hz Brasil + 60Hz) conta como hidráulica
  - mmgd (micro/minigeração distribuída) conta como solar
  - termica é agregada pelo ONS (gás, carvão, óleo, biomassa juntos)
"""

from comum import baixar_json, calcular, imprimir

URL = "https://tr.ons.org.br/Content/GetBalancoEnergetico/null"

SUBSISTEMAS = {
    "sudesteECentroOeste": "Brasil SE/CO",
    "sul": "Brasil S",
    "nordeste": "Brasil NE",
    "norte": "Brasil N",
}

CAMPOS = {
    "hidraulica": "hidraulica",
    "itaipu50HzBrasil": "hidraulica",
    "itaipu60Hz": "hidraulica",
    "termica": "termica_agregada",
    "eolica": "eolica",
    "nuclear": "nuclear",
    "solar": "solar",
    "mmgd": "solar",
}


def coletar():
    dados = baixar_json(URL)
    resultados = []
    for chave, nome in SUBSISTEMAS.items():
        mix = {}
        for campo, valor in dados[chave]["geracao"].items():
            fonte = CAMPOS.get(campo)
            if fonte:
                mix[fonte] = mix.get(fonte, 0) + max(valor or 0, 0)
        resultados.append((nome, dados["Data"], calcular(mix)))
    return resultados


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
