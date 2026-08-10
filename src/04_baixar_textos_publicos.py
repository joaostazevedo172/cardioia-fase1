#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CardioIA - Fase 1 | Parte 2 - Download dos textos de dominio publico
====================================================================
Baixa e limpa as obras classicas usadas no corpus de NLP.

Fonte: Project Gutenberg (dominio publico nos EUA e na maior parte do mundo).
O script remove o cabecalho e o rodape de licenca do Gutenberg, mantendo
apenas o corpo do texto - o que evita que o modelo de NLP aprenda ruido
juridico repetido.

Obras:
  #67065  HARVEY, William. An Anatomical Disquisition on the Motion of the
          Heart and Blood in Animals (1628). Primeira descricao correta da
          circulacao sanguinea - marco fundador da cardiologia.
  #2939   HUXLEY, Thomas H. William Harvey and the Discovery of the
          Circulation of the Blood (1878). Texto expositivo/divulgacao.

Uso:  python src/04_baixar_textos_publicos.py
"""

from __future__ import annotations

import os
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(BASE, "docs")
os.makedirs(DOCS, exist_ok=True)

OBRAS = [
    ("https://www.gutenberg.org/cache/epub/67065/pg67065.txt",
     "texto_01_harvey_1628_de_motu_cordis.txt"),
    ("https://www.gutenberg.org/cache/epub/2939/pg2939.txt",
     "texto_02_huxley_1878_descoberta_da_circulacao.txt"),
]


def limpar(txt: str) -> str:
    txt = txt.replace("\r\n", "\n")
    i = txt.find("*** START OF THE PROJECT GUTENBERG")
    if i >= 0:
        txt = txt[txt.find("\n", i) + 1:]
    j = txt.find("*** END OF THE PROJECT GUTENBERG")
    if j >= 0:
        txt = txt[:j]
    return txt.strip() + "\n"


for url, nome in OBRAS:
    destino = os.path.join(DOCS, nome)
    print(f"baixando {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "CardioIA-FIAP/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        bruto = r.read().decode("utf-8", errors="ignore")
    texto = limpar(bruto)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"OK  docs/{nome}  ({len(texto.split())} palavras)")
