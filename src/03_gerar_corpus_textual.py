#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CardioIA - Fase 1 | Parte 2 - Dados Textuais (NLP)
==================================================
Gerador do CORPUS CLINICO EM PORTUGUES do projeto.

Diferencial do grupo: os textos NAO sao independentes do dataset numerico.
Cada prontuario e escrito a partir da linha correspondente de
`data/cardioia_pacientes.csv`, usando a mesma chave `id_paciente`. Isso cria
um corpus MULTIMODAL ALINHADO - tabela + texto + (via ECG) imagem - que
permite, nas fases seguintes:

  * treinar NLP e ML no mesmo paciente e comparar os desempenhos;
  * validar extracao de entidades (a resposta certa esta na tabela);
  * construir fusao tardia (late fusion) de modalidades na Fase 7.

Textos gerados:
  docs/texto_03_prontuarios_sinteticos_cardioia.txt   (300 prontuarios)
  docs/texto_04_teleatendimento_dialogos_cardioia.txt (200 dialogos rotulados)
  data/corpus_teleatendimento.csv                     (versao tabular rotulada)

IMPORTANTE: nenhum dado de pessoa real foi usado. Sao textos gerados por
template + amostragem aleatoria sobre a coorte sintetica.

Uso:  python src/03_gerar_corpus_textual.py
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd

SEED = 20260806
rng = np.random.default_rng(SEED)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
DOCS = os.path.join(BASE, "docs")
os.makedirs(DOCS, exist_ok=True)

df = pd.read_csv(os.path.join(DATA, "cardioia_pacientes.csv"))

# --------------------------------------------------------------------------
# BANCO DE EXPRESSOES  (linguagem de prontuario + linguagem leiga)
# --------------------------------------------------------------------------
QUEIXA = {
    "Tipica_anginosa": [
        "dor em aperto no meio do peito que irradia para o braco esquerdo",
        "sensacao de peso retroesternal ao caminhar, aliviada com o repouso",
        "dor precordial em queimacao com irradiacao para a mandibula",
        "aperto no peito desencadeado por esforco, com sudorese fria",
    ],
    "Atipica": [
        "desconforto epigastrico que a paciente descreve como ma digestao",
        "dor no peito em pontadas, sem relacao clara com esforco",
        "cansaco desproporcional e dor entre as escapulas",
        "queimacao no estomago associada a nausea e falta de ar",
    ],
    "Nao_anginosa": [
        "dor pontual na parede toracica que piora a palpacao",
        "dor toracica ventilatorio-dependente, tipo pleuritica",
        "desconforto muscular na regiao peitoral apos esforco fisico",
    ],
    "Assintomatico": [
        "assintomatico; comparece para avaliacao de rotina",
        "sem queixas cardiovasculares; encaminhado por alteracao em exame admissional",
        "nega dor toracica; veio por indicacao do clinico geral apos exame alterado",
    ],
}

CONDUTA_ALTO = [
    "Solicitado ecocardiograma transtoracico e teste ergometrico. Iniciado AAS 100 mg/dia e estatina de alta potencia. Retorno em 15 dias.",
    "Encaminhado a estratificacao invasiva. Otimizado tratamento anti-isquemico. Orientado sobre sinais de alarme e procura imediata do pronto-socorro.",
    "Internacao para investigacao de sindrome coronariana. Coletados marcadores de necrose miocardica seriados.",
]
CONDUTA_MEDIO = [
    "Solicitado perfil lipidico de controle e teste ergometrico ambulatorial. Reforcada mudanca de estilo de vida. Retorno em 60 dias.",
    "Ajustada dose do anti-hipertensivo. Orientada dieta com reducao de sodio e atividade fisica supervisionada. Retorno em 90 dias.",
    "Mantido tratamento clinico. Solicitado Holter 24h por relato de palpitacoes.",
]
CONDUTA_BAIXO = [
    "Paciente de baixo risco. Orientacoes de prevencao primaria e retorno anual.",
    "Sem indicacao de investigacao adicional no momento. Reforcado controle ponderal e adesao as medidas preventivas.",
    "Mantida conduta expectante. Solicitados exames laboratoriais de rotina em 12 meses.",
]

# --------------------------------------------------------------------------
# 1. PRONTUARIOS
# --------------------------------------------------------------------------
def fmt(v, casas=0):
    if pd.isna(v):
        return "nao realizado"
    return f"{v:.{casas}f}"


def monta_prontuario(r):
    sexo_txt = "masculino" if r.sexo == "M" else "feminino"
    queixa = rng.choice(QUEIXA[r.dor_toracica_tipo])

    ant = []
    if r.hipertensao_diagnosticada: ant.append("hipertensao arterial sistemica")
    if r.diabetes: ant.append("diabetes mellitus tipo 2")
    if r.tabagismo: ant.append("tabagismo ativo")
    if r.etilismo == 2: ant.append("etilismo de risco")
    if r.historico_familiar_dac: ant.append("historia familiar de doenca arterial coronariana")
    if not ant: ant.append("nega comorbidades previas")

    sint = []
    if r.dispneia_esforco: sint.append("dispneia aos esforcos")
    if r.palpitacoes: sint.append("palpitacoes")
    if r.sincope: sint.append("episodio sincopal")
    if r.edema_mmii: sint.append("edema de membros inferiores")
    if r.fadiga: sint.append("fadiga")
    sint_txt = ", ".join(sint) if sint else "nega demais sintomas cardiovasculares"

    conduta = rng.choice({"Alto": CONDUTA_ALTO,
                          "Intermediario": CONDUTA_MEDIO,
                          "Baixo": CONDUTA_BAIXO}[r.risco_cardiovascular])

    desfecho = ("Registrado evento cardiovascular maior no seguimento de 12 meses."
                if r.evento_cardiaco_12m else
                "Sem eventos cardiovasculares no seguimento de 12 meses.")

    return f"""=== PRONTUARIO {r.id_paciente} | Ambulatorio de Cardiologia - Hospital CardioIA (SIMULADO) ===
IDENTIFICACAO: Paciente do sexo {sexo_txt}, {r.idade} anos, procedente de {r.regiao_atendimento}.
QUEIXA PRINCIPAL: Refere {queixa}.
HISTORIA DA DOENCA ATUAL: Quadro com evolucao progressiva. Ao interrogatorio, {sint_txt}. Classe funcional NYHA {r.classe_funcional_nyha}.
ANTECEDENTES PESSOAIS: {"; ".join(ant)}.
HABITOS DE VIDA: pratica atividade fisica em {r.dias_ativos_semana} dia(s) por semana.
EXAME FISICO: PA {r.pressao_sistolica}x{r.pressao_diastolica} mmHg; FC {r.frequencia_cardiaca_repouso} bpm; SatO2 {r.saturacao_o2}%; IMC {fmt(r.imc,1)} kg/m2.
EXAMES COMPLEMENTARES: colesterol total {fmt(r.colesterol_total)} mg/dL; LDL {fmt(r.colesterol_ldl)} mg/dL; HDL {fmt(r.colesterol_hdl)} mg/dL; triglicerides {fmt(r.triglicerides)} mg/dL; glicemia de jejum {fmt(r.glicemia_jejum)} mg/dL.
ELETROCARDIOGRAMA DE REPOUSO: {r.ecg_repouso.replace("_", " ")}.
TEMPO ATE O PRIMEIRO ATENDIMENTO: {r.tempo_ate_atendimento_min} minutos.
ESTRATIFICACAO: risco cardiovascular {r.risco_cardiovascular.lower()} (escore estimado {r.escore_risco_10a_pct}% em 10 anos).
CONDUTA: {conduta}
DESFECHO: {desfecho}
"""


CABECALHO_PRONT = """CORPUS CLINICO SINTETICO - PRONTUARIOS CARDIOIA
================================================
Projeto: CardioIA - FIAP | Fase 1 - Batimentos de Dados
Natureza: TEXTO 100% SINTETICO, gerado por template a partir da coorte
          sintetica `data/cardioia_pacientes.csv`. Nenhum paciente real.
Licenca: uso academico livre.
Chave de ligacao com a base numerica: campo `id_paciente` (formato CARD-XXXX).
Total de registros neste arquivo: 300.

------------------------------------------------------------------------
"""

amostra = df.sample(300, random_state=SEED)
textos = [monta_prontuario(r) for r in amostra.itertuples()]
p1 = os.path.join(DOCS, "texto_03_prontuarios_sinteticos_cardioia.txt")
with open(p1, "w", encoding="utf-8") as f:
    f.write(CABECALHO_PRONT + "\n".join(textos))

# --------------------------------------------------------------------------
# 2. TELEATENDIMENTO  (alimenta o chatbot da Fase 5)
# --------------------------------------------------------------------------
FALAS = [
    # (fala do paciente, intencao, urgencia, sentimento, resposta do assistente)
    ("Estou com uma dor forte no peito agora, que vai pro braco esquerdo, e suando frio.",
     "sintoma_emergencia", "critica", "negativo",
     "Isso pode ser um infarto. Ligue imediatamente para o SAMU 192 ou va ao pronto-socorro mais proximo. Nao dirija ate o hospital."),
    ("Meu coracao esta disparado desde ontem, parece que vai sair pela boca.",
     "sintoma_emergencia", "alta", "negativo",
     "Palpitacoes persistentes por mais de 24 horas precisam de eletrocardiograma. Procure um servico de urgencia hoje."),
    ("Acordei com falta de ar e as pernas muito inchadas.",
     "sintoma_emergencia", "alta", "negativo",
     "Falta de ar com inchaco nas pernas pode indicar descompensacao cardiaca. Procure atendimento ainda hoje."),
    ("Posso tomar o remedio da pressao junto com o cafe da manha?",
     "duvida_medicacao", "baixa", "neutro",
     "Sim, na maioria dos casos. O importante e manter sempre o mesmo horario. Confirme com o seu cardiologista no retorno."),
    ("Esqueci de tomar o comprimido ontem a noite. E perigoso?",
     "duvida_medicacao", "media", "preocupado",
     "Uma dose esquecida raramente causa problema. Nao dobre a dose hoje; retome o horario habitual e anote para comentar na consulta."),
    ("Esse remedio esta me dando muita tosse seca, e normal?",
     "efeito_adverso", "media", "negativo",
     "Tosse seca e um efeito conhecido de alguns anti-hipertensivos. Nao suspenda por conta propria; agende reavaliacao para possivel troca."),
    ("Quero remarcar minha consulta de cardiologia para a proxima semana.",
     "agendamento", "baixa", "neutro",
     "Posso encaminhar seu pedido a central de agendamento. Confirme sua preferencia de turno."),
    ("Minha pressao hoje deu 180 por 110. O que eu faco?",
     "monitoramento", "alta", "preocupado",
     "Esse valor e elevado. Repita a medicao apos 15 minutos de repouso. Se permanecer acima de 180x110, procure atendimento imediatamente."),
    ("Medi a pressao e deu 118 por 76. Esta bom?",
     "monitoramento", "baixa", "positivo",
     "Esta dentro da faixa desejada. Continue registrando as medidas para levar na consulta."),
    ("Consegui parar de fumar faz tres meses, estou muito feliz com isso.",
     "adesao_habitos", "baixa", "positivo",
     "Excelente conquista. Em um ano sem fumar o risco de infarto cai de forma expressiva. Continue assim."),
    ("Estou com medo de fazer o cateterismo, nao durmo direito pensando nisso.",
     "apoio_emocional", "media", "ansioso",
     "E natural sentir medo antes de um exame invasivo. O cateterismo e um procedimento comum e monitorado o tempo todo. Podemos registrar suas duvidas para a equipe esclarecer antes."),
    ("Depois que meu pai infartou eu fico o tempo todo achando que vou infartar tambem.",
     "apoio_emocional", "media", "ansioso",
     "Historia familiar aumenta o risco, mas nao define o seu destino: controle de pressao, colesterol e tabagismo muda muito esse cenario. Vale conversar tambem com apoio psicologico."),
    ("Posso voltar a caminhar depois da angioplastia?",
     "orientacao_atividade", "baixa", "neutro",
     "Em geral a caminhada leve e liberada precocemente, mas a autorizacao depende da avaliacao do seu cardiologista. Nao inicie sem essa liberacao."),
    ("Qual dieta e melhor pra baixar o colesterol?",
     "orientacao_dieta", "baixa", "neutro",
     "Reduzir gordura saturada e ultraprocessados e aumentar fibras, peixes e azeite tem boa evidencia. O acompanhamento com nutricionista potencializa o resultado."),
    ("Sinto tontura quando levanto rapido da cama.",
     "sintoma_leve", "media", "preocupado",
     "Pode ser hipotensao postural, comum com alguns anti-hipertensivos. Levante-se devagar e relate na proxima consulta; se houver desmaio, procure atendimento."),
    ("Meu relogio apontou 43 batimentos por minuto durante a noite, isso e ruim?",
     "monitoramento", "media", "preocupado",
     "Frequencias baixas durante o sono podem ser normais, sobretudo em pessoas treinadas. Se vier acompanhada de tontura ou desmaio, procure avaliacao."),
    ("Nao consigo pagar o remedio esse mes.",
     "acesso_tratamento", "alta", "negativo",
     "Nao interrompa o tratamento. Varios anti-hipertensivos e estatinas estao disponiveis pelo Farmacia Popular e nas UBS. Posso registrar isso para a equipe orientar a retirada."),
    ("Moro na zona rural e a consulta mais proxima e a 3 horas de onibus.",
     "acesso_tratamento", "media", "negativo",
     "Vamos verificar a possibilidade de teleconsulta e de acompanhamento na UBS do seu municipio para reduzir esse deslocamento."),
    ("Estou melhor depois que comecei a caminhar todo dia, quase nao canso mais.",
     "adesao_habitos", "baixa", "positivo",
     "Otimo sinal de melhora da capacidade funcional. Mantenha a regularidade e registre a frequencia semanal."),
    ("O exame deu 'alteracao de ST-T', o que significa isso?",
     "duvida_exame", "media", "ansioso",
     "E uma alteracao no eletrocardiograma que pode ter varias causas, algumas benignas. Ela precisa ser interpretada junto com seus sintomas pelo cardiologista."),
]

CANAIS = ["chat_web", "aplicativo_movel", "whatsapp", "totem_ubs"]

CAB_DIAL = """CORPUS DE TELEATENDIMENTO CARDIOLOGICO - CARDIOIA (SIMULADO)
=============================================================
Projeto: CardioIA - FIAP | Fase 1 - Batimentos de Dados
Natureza: dialogos SINTETICOS entre paciente e assistente virtual, escritos
          pela equipe do projeto. Nenhuma conversa real foi utilizada.
Rotulos por dialogo: intencao, nivel de urgencia e sentimento do paciente.
Objetivo: treinar classificacao de intencao, triagem automatica por urgencia
          e analise de sentimento (Fase 5 - Assistente Cardiologico Virtual).
Total de dialogos: 200.

-------------------------------------------------------------------------
"""

linhas, registros = [], []
ids = df.id_paciente.sample(len(FALAS) * 10, replace=True, random_state=SEED).tolist()
for i in range(200):
    fala, intencao, urg, sent, resposta = FALAS[i % len(FALAS)]
    canal = rng.choice(CANAIS)
    linhas.append(
        f"--- ATENDIMENTO {i+1:03d} | paciente: {ids[i]} | canal: {canal} | "
        f"intencao: {intencao} | urgencia: {urg} | sentimento: {sent} ---\n"
        f"PACIENTE: {fala}\n"
        f"ASSISTENTE: {resposta}\n"
    )
    registros.append({"id_atendimento": f"ATD-{i+1:03d}", "id_paciente": ids[i],
                      "canal": canal, "texto_paciente": fala,
                      "resposta_assistente": resposta, "intencao": intencao,
                      "urgencia": urg, "sentimento": sent})

p2 = os.path.join(DOCS, "texto_04_teleatendimento_dialogos_cardioia.txt")
with open(p2, "w", encoding="utf-8") as f:
    f.write(CAB_DIAL + "\n".join(linhas))

pd.DataFrame(registros).to_csv(
    os.path.join(DATA, "corpus_teleatendimento.csv"), index=False, encoding="utf-8")

for p in (p1, p2):
    n = len(open(p, encoding="utf-8").read().split())
    print(f"OK  {os.path.relpath(p, BASE)}  ({n} palavras)")
print("OK  data/corpus_teleatendimento.csv")
