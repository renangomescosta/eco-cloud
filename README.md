# EcoCloud
Projeto de Mestrado
> Email: renancosta921@usp.br



# Regiões Utilizadas

## Objetivo

Esta amostragem define as regiões cuja intensidade de carbono da rede elétrica é usada no escalonamento do servidor. As regiões foram escolhidas para formar uma amostra **diversificada**, cobrindo diferentes continentes e perfis de matriz elétrica: hídrica, nuclear, solar, eólica, gás e carvão.

## Regiões
| # | Região | Arquivo | Matriz típica | Fonte | Atraso aprox. | Status |
|---|--------|---------|---------------|-------|---------------|--------|
| 1 | Brasil (SE/CO, S, NE, N) | `regiao_01_br_cs.py` | Hídrica | ONS | a verificar | Funcionando |
| 2 | EUA (Califórnia) | `regiao_02_us_cal_ciso.py` | Solar + gás | CAISO | a verificar | Funcionando |
| 3 | França | `regiao_03_fr.py` | Nuclear | RTE (éCO2mix, via ODRE) | ~30–45 min | Funcionando |
| 4 | Alemanha | `regiao_04_de.py` | Eólica + carvão + gás | Energy-Charts (Fraunhofer ISE) | ~1h45 | Funcionando |
| 5 | Reino Unido | `regiao_05_gb.py` | Eólica + gás | NESO (Carbon Intensity API) | ~30–45 min | Funcionando |
| 6 | Nova Zelândia | `regiao_06_nz.py` | Hídrica + geotérmica | Transpower (em6) | a verificar | Funcionando |
| 7 | Polônia | `regiao_07_pl.py` | Carvão | Energy-Charts (Fraunhofer ISE) | ~3h | Funcionando |
| 8 | Espanha | `regiao_08_es.py` | Solar + eólica | Energy-Charts (Fraunhofer ISE) | ~3h | Funcionando |
| 9 | Itália | `regiao_09_it.py` | Gás | Energy-Charts (Fraunhofer ISE) | ~3h | Funcionando |
| 10 | Suécia | `regiao_10_se.py` | Hídrica + nuclear | Energy-Charts (Fraunhofer ISE) | ~3h | Funcionando |

> **Status:** testado em 08/11/2026 com `python3 coletar_todas.py`.
> **Atraso aprox.:** diferença entre o horário da coleta e o horário do último dado publicado, observada em uma rodada.

> **Zona:** identificador da região no padrão do projeto [electricitymaps-contrib](https://github.com/electricitymaps/electricitymaps-contrib).
> **Confiança:** grau de segurança quanto à disponibilidade e à estabilidade da fonte de dados.

## Por que um modelo próprio

Antes de optar por um modelo próprio, avaliamos o uso de APIs prontas de intensidade de carbono. Dois problemas levaram a descartá-las:

1. **Custo:** as APIs com a cobertura e a granularidade necessárias são pagas.
2. **Precisão e transparência das fontes:** com um modelo próprio, temos controle total sobre a origem dos dados, que vêm diretamente dos operadores oficiais de cada rede, e sobre os critérios de cálculo aplicados.






> Para rodar:
`python3 coletar_todas.py`





## Artigos Base
1. [Strategies for operating and sizing low-carbon cloud data
centers](https://theses.hal.science/tel-04678116v1/document)

2. [Indirect Network Impact on the Energy Consumption in
Multi-clouds for Follow-the-renewables Approaches](https://hal.science/hal-03658289v1/document)

3. [The Difference Between Docker and VM](https://aws.amazon.com/pt/compare/the-difference-between-docker-vm/)

4. [Docker VS Podman](https://www.datacamp.com/blog/docker-vs-podman)

5. [DDNS](https://aws.amazon.com/pt/what-is/dynamic-dns/)

## Ferramentas
1. [Grid'5000](https://www.grid5000.fr/w/Grid5000:Home)

2. [Electricity Maps](https://app.electricitymaps.com/map/live/fifteen_minutes)
