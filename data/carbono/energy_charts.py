"""
Leitura da API pública do Energy-Charts (Fraunhofer ISE).
Usada pelas regiões europeias: DE, PL, ES, IT, SE.

Observações:
  - O mapeamento das fontes é feito por palavra-chave no nome.
    Nomes não reconhecidos são listados no terminal para você conferir.
  - Ficam de fora: consumo de bombeamento, comércio internacional,
    carga (load) e indicadores de participação (share).
"""

from datetime import datetime, timezone

from comum import baixar_json, calcular

URL = "https://api.energy-charts.info/public_power?country={pais}"

IGNORAR = ("consumption", "cross border", "load", "share", "battery")

# ordem importa: a primeira palavra-chave encontrada vence
PALAVRAS = [
    ("nuclear", "nuclear"),
    ("lignite", "carvao"),
    ("hard coal", "carvao"),
    ("oil", "oleo"),
    ("gas", "gas"),
    ("biomass", "biomassa"),
    ("geothermal", "geotermica"),
    ("hydro", "hidraulica"),
    ("wind", "eolica"),
    ("solar", "solar"),
    ("waste", "outros"),
    ("other", "outros"),
]


def classificar(nome):
    n = nome.lower()
    if any(p in n for p in IGNORAR):
        return None
    for palavra, fonte in PALAVRAS:
        if palavra in n:
            return fonte
    return "?"


def coletar_pais(pais, nome_regiao):
    dados = baixar_json(URL.format(pais=pais))
    tempos = dados["unix_seconds"]
    tipos = dados["production_types"]

    # instante mais recente com o maior número de séries preenchidas
    # (algumas séries podem vir sempre vazias, então não exige todas)
    relevantes = [t for t in tipos if classificar(t["name"])]
    preenchidas = [sum(t["data"][j] is not None for t in relevantes) for j in range(len(tempos))]
    if not preenchidas or max(preenchidas) == 0:
        raise ValueError("nenhum instante com dados")
    melhor = max(preenchidas)
    i = max(j for j, n in enumerate(preenchidas) if n == melhor)

    mix, nao_mapeados = {}, []
    for t in tipos:
        fonte = classificar(t["name"])
        if fonte is None:
            continue
        if fonte == "?":
            nao_mapeados.append(t["name"])
            continue
        mix[fonte] = mix.get(fonte, 0) + (t["data"][i] or 0)

    if nao_mapeados:
        print(f"[{pais.upper()}] fontes não reconhecidas (ignoradas): {nao_mapeados}")

    horario = datetime.fromtimestamp(tempos[i], tz=timezone.utc).isoformat()
    return [(nome_regiao, horario, calcular(mix))]
