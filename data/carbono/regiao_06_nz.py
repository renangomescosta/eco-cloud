"""
Região 06 - Nova Zelândia
Fonte: Transpower "Power system live data" (dados do em6, JSON embutido no HTML)

Rodar: python3 regiao_06_nz.py

Observações:
  - A página traz objetos do tipo {"Coal":{"generation":..,"capacity":..}, ...}.
    Pode haver mais de um (país e ilhas): o script usa o de MAIOR geração
    total, que deve ser o nacional.
  - Battery fica de fora (armazenamento).
  - Co-Gen entra como "outros" (mistura de combustíveis; fator é suposição).
  - Fontes não reconhecidas são listadas no terminal.
"""

import json
import re
import urllib.request

from comum import calcular, imprimir

URL = "https://www.transpower.co.nz/power-system-live-data"

FONTES = {
    "coal": "carvao",
    "gas": "gas",
    "geothermal": "geotermica",
    "hydro": "hidraulica",
    "wind": "eolica",
    "solar": "solar",
    "co-gen": "outros",
    "cogen": "outros",
    "liquid": "oleo",
    "diesel": "oleo",
    "diesel/oil": "oleo",
}
IGNORAR = {"battery"}


def _objeto_em_volta(texto, pos):
    """Retorna o objeto JSON {...} que contém a posição pos."""
    nivel, ini = 0, pos
    while ini >= 0:
        if texto[ini] == "}":
            nivel += 1
        elif texto[ini] == "{":
            if nivel == 0:
                break
            nivel -= 1
        ini -= 1
    nivel = 0
    for fim in range(ini, len(texto)):
        if texto[fim] == "{":
            nivel += 1
        elif texto[fim] == "}":
            nivel -= 1
            if nivel == 0:
                return json.loads(texto[ini:fim + 1])
    raise ValueError("objeto JSON não fechado")


def coletar():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8")

    candidatos = []
    for m in re.finditer(r'"Coal"\s*:\s*\{\s*"generation"', html):
        try:
            candidatos.append(_objeto_em_volta(html, m.start()))
        except (ValueError, json.JSONDecodeError):
            continue
    if not candidatos:
        raise ValueError("não achei o JSON de geração na página")

    def total(obj):
        return sum(max(v.get("generation") or 0, 0)
                   for v in obj.values() if isinstance(v, dict))

    nacional = max(candidatos, key=total)

    mix, nao_mapeados = {}, []
    for nome, v in nacional.items():
        if not isinstance(v, dict) or "generation" not in v:
            continue
        chave = nome.lower()
        if chave in IGNORAR:
            continue
        fonte = FONTES.get(chave)
        if not fonte:
            nao_mapeados.append(nome)
            continue
        mix[fonte] = mix.get(fonte, 0) + (v["generation"] or 0)

    if nao_mapeados:
        print(f"[NZ] fontes não reconhecidas (ignoradas): {nao_mapeados}")

    m = re.search(r"as at.{0,120}?(\d{1,2} \w{3} \d{4} \d{1,2}:\d{2})", html, re.S | re.I)
    horario = m.group(1) + " (horário NZ)" if m else "horário não encontrado na página"
    return [("Nova Zelândia", horario, calcular(mix))]


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
