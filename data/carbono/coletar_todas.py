"""
Arquivo 11 - coleta todas as regiões e imprime no terminal.

Rodar: python3 coletar_todas.py
"""

import regiao_01_br_cs
import regiao_02_us_cal_ciso
import regiao_03_fr
import regiao_04_de
import regiao_05_gb
import regiao_06_nz
import regiao_07_pl
import regiao_08_es
import regiao_09_it
import regiao_10_se
from comum import imprimir

REGIOES = [
    regiao_01_br_cs,
    regiao_02_us_cal_ciso,
    regiao_03_fr,
    regiao_04_de,
    regiao_05_gb,
    regiao_06_nz,
    regiao_07_pl,
    regiao_08_es,
    regiao_09_it,
    regiao_10_se,
]

if __name__ == "__main__":
    for modulo in REGIOES:
        try:
            for nome, horario, r in modulo.coletar():
                # regiao, horario, r
                imprimir(nome, horario, r)
        except Exception as e:  # uma região com erro não derruba as outras
            print(f"{modulo.__name__:22} FALHOU -> {type(e).__name__}: {e}")
