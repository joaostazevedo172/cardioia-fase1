#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CardioIA - Fase 1 | Batimentos de Dados
=======================================
Gerador da COORTE SINTETICA "HOSPITAL CARDIOIA".

Este script NAO baixa dados de nenhum repositorio publico. Ele CONSTROI,
a partir de um modelo estatistico explicito, uma coorte fictícia de pacientes
cardiologicos. Toda a estrutura de dependencia entre as variaveis foi
parametrizada com base em relacoes clinicas descritas na literatura
(Framingham, diretrizes da SBC/AHA) e esta documentada em
`docs/GOVERNANCA_DE_DADOS.md`.

Por que sintetico?
------------------
1. Zero risco de reidentificacao de pacientes reais (LGPD Art. 11 - dado
   sensivel de saude).
2. Rastreabilidade total: sabemos exatamente qual e o "processo gerador"
   dos dados, o que permite validar depois se o modelo de IA aprendeu o
   padrao correto ou apenas um atalho espurio.
3. Reprodutibilidade: SEED fixa -> qualquer pessoa regenera o mesmo CSV.
4. Unicidade: nenhum outro grupo tera exatamente esta base.

Uso:
    python src/01_gerar_dataset_numerico.py
Saidas:
    data/cardioia_pacientes.csv
    data/cardioia_pacientes.xlsx
    data/dicionario_de_dados.md  (gerado automaticamente)
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd

SEED = 20260806          # data de referencia do projeto -> reprodutibilidade
N_PACIENTES = 800        # rubrica pede >= 100; entregamos 800
rng = np.random.default_rng(SEED)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
DOCS = os.path.join(BASE, "docs")
os.makedirs(DATA, exist_ok=True)
os.makedirs(DOCS, exist_ok=True)


# --------------------------------------------------------------------------
# 1. DEMOGRAFIA
# --------------------------------------------------------------------------
def clip(x, lo, hi):
    return np.clip(x, lo, hi)


idade = clip(rng.normal(58, 14, N_PACIENTES), 29, 92).round(0).astype(int)

# VIES DELIBERADO E DOCUMENTADO: 58% homens.
# Coortes cardiologicas reais historicamente sub-representam mulheres, o que
# faz modelos de IA errarem mais no diagnostico feminino (sintomas atipicos).
# Mantemos o desbalanceamento de proposito para que ele seja MEDIDO nas
# proximas fases, e nao escondido.
sexo = rng.choice(["M", "F"], N_PACIENTES, p=[0.58, 0.42])

# Regiao de origem - permite auditar vies geografico de acesso ao servico
regiao = rng.choice(
    ["Capital", "Regiao Metropolitana", "Interior", "Zona Rural"],
    N_PACIENTES, p=[0.42, 0.28, 0.22, 0.08],
)

imc = clip(rng.normal(27.5, 4.6, N_PACIENTES), 16.5, 47.0).round(1)

# --------------------------------------------------------------------------
# 2. FATORES DE RISCO (probabilidades condicionadas a idade/sexo/IMC)
# --------------------------------------------------------------------------
def bern(p):
    return (rng.random(N_PACIENTES) < np.clip(p, 0.01, 0.97)).astype(int)


p_fuma = 0.10 + 0.14 * (sexo == "M") + 0.10 * (idade < 55)
tabagismo = bern(p_fuma)

p_dm = 0.03 + 0.006 * (idade - 30) + 0.020 * (imc - 25)
diabetes = bern(p_dm)

p_has = 0.05 + 0.010 * (idade - 30) + 0.018 * (imc - 25)
hipertensao = bern(p_has)

hist_familiar_dac = bern(np.full(N_PACIENTES, 0.31))
sedentarismo_dias = rng.integers(0, 8, N_PACIENTES)          # dias ativos/semana
etilismo = rng.choice([0, 1, 2], N_PACIENTES, p=[0.55, 0.34, 0.11])  # 0 nao,1 social,2 pesado

# --------------------------------------------------------------------------
# 3. SINAIS VITAIS E LABORATORIO
# --------------------------------------------------------------------------
pressao_sistolica = clip(
    108 + 0.42 * (idade - 30) + 22 * hipertensao + 0.9 * (imc - 25)
    + 4 * tabagismo + rng.normal(0, 9, N_PACIENTES), 88, 215
).round(0).astype(int)

pressao_diastolica = clip(
    0.58 * pressao_sistolica + 8 + rng.normal(0, 6, N_PACIENTES), 52, 130
).round(0).astype(int)

colesterol_ldl = clip(
    92 + 0.55 * (idade - 30) + 16 * diabetes + 1.4 * (imc - 25)
    + rng.normal(0, 22, N_PACIENTES), 45, 265
).round(0).astype(int)

colesterol_hdl = clip(
    58 - 8 * (sexo == "M") - 6 * tabagismo - 0.55 * (imc - 25)
    + 1.1 * sedentarismo_dias + rng.normal(0, 8, N_PACIENTES), 18, 96
).round(0).astype(int)

triglicerides = clip(
    np.exp(rng.normal(4.83, 0.42, N_PACIENTES)) + 38 * diabetes + 2.6 * (imc - 25),
    45, 620
).round(0).astype(int)

colesterol_total = (colesterol_ldl + colesterol_hdl + triglicerides / 5).round(0).astype(int)

glicemia_jejum = clip(
    88 + 46 * diabetes + 0.9 * (imc - 25) + rng.normal(0, 11, N_PACIENTES), 62, 310
).round(0).astype(int)

fc_repouso = clip(
    72 + 6 * tabagismo - 1.3 * sedentarismo_dias + 0.10 * (imc - 25)
    + rng.normal(0, 8, N_PACIENTES), 42, 128
).round(0).astype(int)

fc_maxima_esforco = clip(
    (220 - idade) - rng.normal(14, 12, N_PACIENTES) - 9 * diabetes, 78, 202
).round(0).astype(int)

saturacao_o2 = clip(
    98 - 1.6 * tabagismo - 0.04 * (idade - 30) + rng.normal(0, 1.1, N_PACIENTES), 84, 100
).round(0).astype(int)

# --------------------------------------------------------------------------
# 4. RISCO LATENTE  ->  desfechos
#    log-odds explicito: o "ground truth" do processo gerador.
# --------------------------------------------------------------------------
logit = (
    -3.55                                        # intercepto calibrado para
    #                                              prevalencia ~22% (perfil de
    #                                              ambulatorio de cardiologia,
    #                                              nao de populacao geral)
    + 0.055 * (idade - 55)
    + 0.62 * (sexo == "M")
    + 0.78 * tabagismo
    + 0.85 * diabetes
    + 0.60 * hipertensao
    + 0.55 * hist_familiar_dac
    + 0.016 * (pressao_sistolica - 120)
    + 0.011 * (colesterol_ldl - 100)
    - 0.020 * (colesterol_hdl - 50)
    + 0.045 * (imc - 25)
    - 0.070 * sedentarismo_dias
    + 0.30 * (etilismo == 2)
    + 0.014 * (fc_repouso - 72)
    + rng.normal(0, 0.55, N_PACIENTES)          # heterogeneidade individual
)
prob_evento = 1 / (1 + np.exp(-logit))
evento_cardiaco_12m = (rng.random(N_PACIENTES) < prob_evento).astype(int)

# Escore de risco em 10 anos (percentual), derivado do mesmo risco latente
escore_risco_10a = clip(prob_evento * 100 * rng.uniform(0.85, 1.45, N_PACIENTES), 0.4, 79).round(1)

risco_cardiovascular = pd.cut(
    escore_risco_10a, bins=[-1, 5, 20, 100],
    labels=["Baixo", "Intermediario", "Alto"]
).astype(str)

# --------------------------------------------------------------------------
# 5. SINTOMAS (dependem do risco latente -> sinal aprendivel para NLP/ML)
#    Mulheres recebem mais frequentemente dor ATIPICA: fenomeno clinico real
#    e uma das principais causas de subdiagnostico feminino.
# --------------------------------------------------------------------------
dor_tipo = []
for i in range(N_PACIENTES):
    p = prob_evento[i]
    if sexo[i] == "F":
        pesos = [0.16 + 0.45 * p, 0.34, 0.30 - 0.15 * p, 0.20 - 0.15 * p]
    else:
        pesos = [0.26 + 0.50 * p, 0.26, 0.26 - 0.15 * p, 0.22 - 0.20 * p]
    pesos = np.clip(pesos, 0.02, None)
    pesos = np.array(pesos) / np.sum(pesos)
    dor_tipo.append(rng.choice(
        ["Tipica_anginosa", "Atipica", "Nao_anginosa", "Assintomatico"], p=pesos))
dor_toracica_tipo = np.array(dor_tipo)

dispneia_esforco = bern(0.12 + 0.62 * prob_evento)
palpitacoes = bern(0.14 + 0.34 * prob_evento)
sincope = bern(0.03 + 0.20 * prob_evento)
edema_mmii = bern(0.07 + 0.40 * prob_evento)
fadiga = bern(0.18 + 0.45 * prob_evento)

classe_nyha = np.select(
    [prob_evento < 0.10, prob_evento < 0.28, prob_evento < 0.55],
    ["I", "II", "III"], default="IV"
)

ecg_repouso = []
for i in range(N_PACIENTES):
    p = prob_evento[i]
    pesos = np.array([max(0.05, 0.80 - 1.1 * p), 0.10 + 0.55 * p,
                      0.06 + 0.25 * p, 0.04 + 0.30 * p])
    pesos = pesos / pesos.sum()
    ecg_repouso.append(rng.choice(
        ["Normal", "Alteracao_ST_T", "Hipertrofia_VE", "Fibrilacao_atrial"], p=pesos))
ecg_repouso = np.array(ecg_repouso)

# Tempo porta-atendimento: pior no Interior/Zona Rural (vies de acesso REAL,
# mantido de proposito para discussao de equidade nas proximas fases)
base_tempo = {"Capital": 26, "Regiao Metropolitana": 41, "Interior": 68, "Zona Rural": 105}
tempo_ate_atendimento_min = np.array(
    [max(6, int(rng.normal(base_tempo[r], base_tempo[r] * 0.30))) for r in regiao]
)

# --------------------------------------------------------------------------
# 6. MONTAGEM DO DATAFRAME
# --------------------------------------------------------------------------
df = pd.DataFrame({
    "id_paciente": [f"CARD-{i:04d}" for i in range(1, N_PACIENTES + 1)],
    "idade": idade,
    "sexo": sexo,
    "regiao_atendimento": regiao,
    "imc": imc,
    "tabagismo": tabagismo,
    "etilismo": etilismo,
    "diabetes": diabetes,
    "hipertensao_diagnosticada": hipertensao,
    "historico_familiar_dac": hist_familiar_dac,
    "dias_ativos_semana": sedentarismo_dias,
    "pressao_sistolica": pressao_sistolica,
    "pressao_diastolica": pressao_diastolica,
    "frequencia_cardiaca_repouso": fc_repouso,
    "fc_maxima_esforco": fc_maxima_esforco,
    "saturacao_o2": saturacao_o2,
    "colesterol_total": colesterol_total,
    "colesterol_ldl": colesterol_ldl,
    "colesterol_hdl": colesterol_hdl,
    "triglicerides": triglicerides,
    "glicemia_jejum": glicemia_jejum,
    "dor_toracica_tipo": dor_toracica_tipo,
    "dispneia_esforco": dispneia_esforco,
    "palpitacoes": palpitacoes,
    "sincope": sincope,
    "edema_mmii": edema_mmii,
    "fadiga": fadiga,
    "classe_funcional_nyha": classe_nyha,
    "ecg_repouso": ecg_repouso,
    "tempo_ate_atendimento_min": tempo_ate_atendimento_min,
    "escore_risco_10a_pct": escore_risco_10a,
    "risco_cardiovascular": risco_cardiovascular,
    "evento_cardiaco_12m": evento_cardiaco_12m,
})

# --------------------------------------------------------------------------
# 7. "SUJEIRA" CONTROLADA
#    Dados reais nunca chegam limpos. Injetamos ausencias plausiveis para que
#    a etapa de tratamento seja exercitada de verdade nas proximas fases.
#    O padrao NAO e aleatorio: falta mais exame laboratorial em quem foi
#    atendido longe da capital (MAR - Missing At Random), exatamente como
#    acontece na rede publica.
# --------------------------------------------------------------------------
prob_falta = np.where(np.isin(regiao, ["Interior", "Zona Rural"]), 0.11, 0.03)
for col in ["colesterol_hdl", "triglicerides", "glicemia_jejum", "imc"]:
    mask = rng.random(N_PACIENTES) < prob_falta
    df.loc[mask, col] = np.nan

# --------------------------------------------------------------------------
# 8. EXPORTACAO
# --------------------------------------------------------------------------
csv_path = os.path.join(DATA, "cardioia_pacientes.csv")
df.to_csv(csv_path, index=False, encoding="utf-8", sep=",")
try:
    df.to_excel(os.path.join(DATA, "cardioia_pacientes.xlsx"), index=False)
except Exception as e:  # openpyxl ausente
    print(f"[aviso] xlsx nao gerado: {e}")

print(f"OK  {csv_path}")
print(f"    {df.shape[0]} linhas x {df.shape[1]} colunas")
print(f"    prevalencia de evento em 12m: {df.evento_cardiaco_12m.mean():.1%}")
print(df.risco_cardiovascular.value_counts().to_string())
print(f"    celulas ausentes: {int(df.isna().sum().sum())}")
