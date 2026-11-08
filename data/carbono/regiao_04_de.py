"""
Região 04 - Alemanha
Fonte: Energy-Charts (Fraunhofer ISE), API pública (JSON, MW)

Rodar: python3 regiao_04_de.py
"""

from comum import imprimir
from energy_charts import coletar_pais


def coletar():
    return coletar_pais("de", "Alemanha")


if __name__ == "__main__":
    for nome, horario, r in coletar():
        imprimir(nome, horario, r)
