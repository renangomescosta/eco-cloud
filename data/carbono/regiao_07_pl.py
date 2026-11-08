"""
Região 07 - Polônia
Fonte: Energy-Charts (Fraunhofer ISE), API pública (JSON, MW)

Rodar: python3 regiao_07_pl.py
"""

from comum import imprimir
from energy_charts import coletar_pais


def coletar():
    return coletar_pais("pl", "Polônia")


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
