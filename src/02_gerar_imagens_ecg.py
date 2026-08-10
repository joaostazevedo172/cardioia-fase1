#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CardioIA - Fase 1 | Parte 3 - Dados Visuais (Visao Computacional)
=================================================================
Gerador do banco de imagens "ECG-CardioIA".

Cada imagem e um tracado eletrocardiografico renderizado sobre papel
milimetrado padrao (25 mm/s, 10 mm/mV), simulado a partir da soma de
componentes gaussianas que representam as ondas P, Q, R, S e T -
a mesma abordagem usada no gerador ECGSYN (McSharry et al., 2003),
aqui reimplementada de forma simplificada e autoral.

Classes geradas (rotulos ja prontos para treino supervisionado):
    0 normal                 ritmo sinusal 60-95 bpm
    1 taquicardia_sinusal    > 100 bpm
    2 bradicardia_sinusal    < 55 bpm
    3 fibrilacao_atrial      ausencia de onda P + intervalo RR irregular
    4 isquemia_infra_st      infradesnivelamento do segmento ST
    5 iam_supra_st           supradesnivelamento do segmento ST

Ruidos realistas injetados (para que a CNN nao aprenda um traco "limpo demais"):
    - deriva de linha de base (respiracao, 0.15-0.4 Hz)
    - interferencia de rede eletrica 60 Hz
    - ruido eletromiografico de alta frequencia
    - variabilidade de amplitude entre "pacientes"

Uso:
    python src/02_gerar_imagens_ecg.py [n_por_classe]
Saidas:
    assets/ecg/<classe>/ecg_<classe>_<id>.png   (default: 20 x 6 = 120 imagens)
    data/ecg_labels.csv                          (manifesto rotulado)
"""

from __future__ import annotations

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

SEED = 20260806
rng = np.random.default_rng(SEED)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets", "ecg")
DATA = os.path.join(BASE, "data")

FS = 500                     # Hz de amostragem
DUR = 5.0                    # segundos por tracado
N_POR_CLASSE = int(sys.argv[1]) if len(sys.argv) > 1 else 20

CLASSES = {
    "normal":              dict(fc=(60, 95),  rr_irreg=0.02, onda_p=1.00, st=0.00),
    "taquicardia_sinusal": dict(fc=(102, 155), rr_irreg=0.03, onda_p=0.85, st=0.00),
    "bradicardia_sinusal": dict(fc=(38, 54),  rr_irreg=0.03, onda_p=1.05, st=0.00),
    "fibrilacao_atrial":   dict(fc=(75, 150), rr_irreg=0.22, onda_p=0.00, st=0.00),
    "isquemia_infra_st":   dict(fc=(62, 100), rr_irreg=0.03, onda_p=0.95, st=-0.16),
    "iam_supra_st":        dict(fc=(70, 115), rr_irreg=0.04, onda_p=0.90, st=+0.32),
}


def gauss(t, centro, amp, larg):
    return amp * np.exp(-((t - centro) ** 2) / (2 * larg ** 2))


def batimento(t_rel, cfg, escala):
    """Um ciclo P-QRS-T em milivolts. t_rel em segundos a partir do inicio do RR."""
    p_amp = 0.15 * cfg["onda_p"] * escala
    y = np.zeros_like(t_rel)
    y += gauss(t_rel, 0.16, p_amp, 0.025)                    # onda P
    y += gauss(t_rel, 0.30, -0.10 * escala, 0.008)           # onda Q
    y += gauss(t_rel, 0.32, 1.25 * escala, 0.009)            # onda R
    y += gauss(t_rel, 0.35, -0.28 * escala, 0.010)           # onda S
    # segmento ST: platô deslocado entre S e T (marca isquemia/IAM)
    st_mask = (t_rel > 0.36) & (t_rel < 0.50)
    y += st_mask * cfg["st"] * escala
    # onda T (no IAM com supra, fica apiculada e mais alta)
    t_amp = (0.32 + 0.30 * max(cfg["st"], 0)) * escala
    y += gauss(t_rel, 0.55, t_amp, 0.042)
    return y


def gerar_sinal(cfg):
    n = int(FS * DUR)
    t = np.arange(n) / FS
    sinal = np.zeros(n)
    escala = rng.uniform(0.78, 1.22)                          # variabilidade entre pacientes

    fc = rng.uniform(*cfg["fc"])
    rr_medio = 60.0 / fc
    pos = rng.uniform(0, 0.4)
    while pos < DUR:
        rr = rr_medio * (1 + rng.normal(0, cfg["rr_irreg"]))
        rr = float(np.clip(rr, 0.30, 2.0))
        i0 = int(pos * FS)
        janela = np.arange(0, min(int(rr * FS), n - i0)) / FS
        if len(janela) > 10:
            sinal[i0:i0 + len(janela)] += batimento(janela, cfg, escala)
        pos += rr

    # Ondas "f" de fibrilacao atrial substituindo a onda P
    if cfg["onda_p"] == 0.0:
        sinal += 0.05 * escala * np.sin(2 * np.pi * rng.uniform(350, 550) / 60 * t
                                        + rng.uniform(0, 6.28))

    # --- ruidos ---
    sinal += 0.09 * np.sin(2 * np.pi * rng.uniform(0.15, 0.40) * t)   # deriva respiratoria
    sinal += rng.uniform(0.004, 0.020) * np.sin(2 * np.pi * 60 * t)   # rede eletrica 60 Hz
    sinal += rng.normal(0, rng.uniform(0.008, 0.028), n)              # ruido EMG
    return t, sinal


def salvar_png(t, sinal, caminho):
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=100)
    # papel de ECG: grade fina 0,04 s / 0,1 mV; grade grossa 0,2 s / 0,5 mV
    ax.set_facecolor("#fff5f4")
    ax.xaxis.set_minor_locator(MultipleLocator(0.04))
    ax.xaxis.set_major_locator(MultipleLocator(0.20))
    ax.yaxis.set_minor_locator(MultipleLocator(0.10))
    ax.yaxis.set_major_locator(MultipleLocator(0.50))
    ax.grid(which="minor", color="#f3b8b3", linewidth=0.4)
    ax.grid(which="major", color="#e08078", linewidth=0.8)
    ax.plot(t, sinal, color="#12100f", linewidth=0.9)
    ax.set_xlim(0, DUR)
    ax.set_ylim(-1.0, 1.8)
    ax.set_xticklabels([]); ax.set_yticklabels([])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.tight_layout(pad=0.15)
    fig.savefig(caminho, facecolor="#fff5f4")
    plt.close(fig)


def main():
    registros = []
    for idx_classe, (nome, cfg) in enumerate(CLASSES.items()):
        pasta = os.path.join(OUT, nome)
        os.makedirs(pasta, exist_ok=True)
        for i in range(1, N_POR_CLASSE + 1):
            t, sinal = gerar_sinal(cfg)
            arq = f"ecg_{nome}_{i:03d}.png"
            salvar_png(t, sinal, os.path.join(pasta, arq))
            # FC estimada por contagem de picos R (serve de metadado e de
            # "gabarito" para exercicios de processamento de sinal)
            limiar = 0.62 * float(np.max(sinal))
            cand = np.where((sinal[1:-1] > limiar) &
                            (sinal[1:-1] >= sinal[:-2]) &
                            (sinal[1:-1] > sinal[2:]))[0] + 1
            picos = []                      # periodo refratario de 200 ms
            for p in cand:
                if not picos or (p - picos[-1]) > 0.20 * FS:
                    picos.append(p)
            fc_est = round(np.mean(60.0 / (np.diff(picos) / FS))) if len(picos) > 2 else 0
            registros.append({
                "arquivo": f"assets/ecg/{nome}/{arq}",
                "classe": nome,
                "classe_id": idx_classe,
                "achado_normal": int(nome == "normal"),
                "fc_estimada_bpm": fc_est,
                "duracao_s": DUR,
                "fs_hz": FS,
                "origem": "sintetico_cardioia_v1",
            })
        print(f"  {nome:22s} {N_POR_CLASSE} imagens")

    os.makedirs(DATA, exist_ok=True)
    df = pd.DataFrame(registros)
    df.to_csv(os.path.join(DATA, "ecg_labels.csv"), index=False, encoding="utf-8")
    print(f"OK  {len(df)} imagens + data/ecg_labels.csv")


if __name__ == "__main__":
    main()
