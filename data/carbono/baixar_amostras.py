"""
Testa as fontes candidatas e imprime o começo de cada resposta.
Também salva as respostas completas em amostras/.

Rodar: python3 baixar_amostras.py
Depois cole a saída do terminal na conversa.
"""

import os
import urllib.request

CANDIDATAS = {
    # já responderam na rodada anterior: preciso ver o conteúdo
    "02_us_cal_ciso": "https://www.caiso.com/outlook/current/fuelsource.csv",
    "03_fr": "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records?order_by=date_heure%20desc&limit=2",
    "04_de": "https://api.energy-charts.info/public_power?country=de",
    "05_gb": "https://api.carbonintensity.org.uk/generation",
    "08_jp_tk": "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv",
    # novas candidatas
    "06_nz": "https://www.transpower.co.nz/power-system-live-data",
    "06_au_reserva": "https://nemweb.com.au/Reports/Current/Dispatch_SCADA/",
    "07_tw": "https://dr.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json",
    "09_ca_on": "https://reports.ieso.ca/public/GenOutputbyFuelHourly/PUB_GenOutputbyFuelHourly.xml",
    "10_za": "https://www.eskom.co.za/dataportal/supply-side/",
}

PREVIA = 600  # caracteres impressos de cada resposta

os.makedirs("amostras", exist_ok=True)


def decodificar(corpo):
    for enc in ("utf-8", "shift_jis", "latin-1"):
        try:
            return corpo.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return corpo.decode("utf-8", errors="replace"), "utf-8?"


for nome, url in CANDIDATAS.items():
    print("=" * 70)
    print(f"{nome}  {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            corpo = resp.read()
            tipo = resp.headers.get("Content-Type", "")
        texto, enc = decodificar(corpo)
        with open(f"amostras/{nome}.txt", "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"OK  {len(corpo)} bytes  tipo={tipo}  encoding={enc}")
        print("-" * 70)
        print(texto[:PREVIA])
    except Exception as e:
        print(f"FALHOU  {type(e).__name__}: {e}")
