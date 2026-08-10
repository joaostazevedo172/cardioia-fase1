# Governança de Dados e Viés — CardioIA Fase 1

> Documento obrigatório de acompanhamento das três bases entregues.
> Última revisão: agosto de 2026.

---

## 1. Por que uma coorte sintética (e não um dataset real)

Dados de saúde são **dados pessoais sensíveis** (LGPD, Lei 13.709/2018, Art. 5º, II
e Art. 11). Seu tratamento exige consentimento específico ou uma das hipóteses
legais restritas — o que um projeto acadêmico normalmente não consegue satisfazer
para dados identificáveis.

Três caminhos eram possíveis nesta fase:

| Caminho | Risco jurídico | Risco de reidentificação | Unicidade | Escolha |
|---|---|---|---|---|
| Dataset público real (ex.: UCI Heart Disease) | baixo | baixo (já anonimizado) | **nula** — usado por milhares de projetos | ❌ |
| Dados de prontuário real | alto | alto | alta | ❌ |
| **Coorte sintética com processo gerador documentado** | **nulo** | **nulo** | **total** | ✅ |

A síntese não é um "atalho": é uma técnica reconhecida de *privacy-preserving data
sharing*. O ganho adicional é epistemológico — como **conhecemos o processo
gerador**, podemos verificar nas fases seguintes se o modelo aprendeu a relação
causal correta ou apenas um atalho estatístico (*shortcut learning*).

---

## 2. Ciclo de vida do dado neste projeto

```
 [1] ORIGEM          → script gerador versionado (src/01, src/02, src/03)
 [2] COLETA          → seed fixa 20260806 → reprodutibilidade bit a bit
 [3] ARMAZENAMENTO   → CSV/PNG no repositório + espelho em nuvem público
 [4] QUALIDADE       → dicionário de dados + faixas plausíveis validadas
 [5] USO             → exclusivamente acadêmico (Fases 2 a 7)
 [6] RETENÇÃO        → sem prazo: nenhum dado é de pessoa real
 [7] DESCARTE        → não aplicável
```

**Rastreabilidade:** qualquer linha do CSV pode ser reproduzida a partir do script
e da seed. Nenhum dado foi editado manualmente.

**Papéis definidos (mesmo em contexto acadêmico):**

- *Data Owner* — o grupo, responsável pelas decisões sobre a base.
- *Data Steward* — quem mantém o dicionário de dados atualizado a cada fase.
- *Revisor de viés* — quem roda a auditoria da Seção 4 antes de cada entrega.

---

## 3. Vieses que foram **deliberadamente mantidos** na base

Um erro comum é gerar dados perfeitamente balanceados. Isso ensina o modelo — e o
grupo — a ignorar o problema mais importante da IA em saúde. Optamos por **injetar
vieses reais e documentá-los**, para que sejam medidos, não escondidos.

### 3.1 Viés de sexo (58% homens / 42% mulheres)

Coortes cardiológicas históricas sub-representam mulheres. Consequência conhecida:
modelos treinados nelas erram mais no diagnóstico feminino.

**Como está codificado:** mulheres recebem com mais frequência o rótulo
`dor_toracica_tipo = Atipica`, reproduzindo o fato clínico de que a apresentação
feminina do infarto foge do padrão "dor no braço esquerdo".

**Métrica a monitorar nas Fases 2 e 6:** *recall* (sensibilidade) por sexo. Se o
recall feminino for materialmente menor que o masculino, o modelo está reproduzindo
o viés — e não pode ir para produção sem correção.

### 3.2 Viés geográfico de acesso

`tempo_ate_atendimento_min` é sistematicamente maior em `Interior` e `Zona Rural`
(mediana ~68 e ~105 min contra ~26 min na Capital).

**Armadilha a evitar:** se o modelo usar essa variável como preditora, ele pode
aprender "morar longe = pior desfecho" e passar a **desqualificar** pacientes
rurais em vez de priorizá-los. Essa variável deve ser tratada como **variável de
auditoria de equidade**, não como *feature* de diagnóstico.

### 3.3 Dados ausentes não aleatórios (MAR)

Exames laboratoriais faltam em ~11% dos pacientes de Interior/Zona Rural contra
~3% na Capital. A ausência **carrega informação** sobre desigualdade de acesso.
Imputar pela média apaga essa informação e reforça a desigualdade. Recomendação:
manter um indicador binário `_faltante` junto de qualquer imputação.

### 3.4 Desbalanceamento de classe

`evento_cardiaco_12m` tem prevalência de ~18%. Acurácia é uma métrica enganosa
aqui: um modelo que diz "ninguém terá evento" acerta 82%. Nas fases seguintes usar
**recall, F1, AUC-PR e matriz de confusão**, nunca acurácia isolada.

---

## 4. Checklist de auditoria (rodar antes de cada entrega)

- [ ] A distribuição por sexo e região mudou desde a última fase?
- [ ] O *recall* do modelo é equivalente entre homens e mulheres? E entre regiões?
- [ ] Alguma variável proxy de condição socioeconômica entrou como *feature* de diagnóstico?
- [ ] O dado ausente foi imputado sem registro do indicador de ausência?
- [ ] A métrica principal continua sendo sensível ao desbalanceamento?
- [ ] Todo arquivo publicado está marcado como **SIMULADO**?

---

## 5. Limitações honestas desta base

1. **Não substitui dado real.** As correlações foram parametrizadas por nós; um
   modelo com desempenho excelente aqui não tem validade clínica alguma.
2. **Não há efeitos temporais** (progressão de doença, sazonalidade, adesão ao
   longo do tempo). A Fase 6 (séries temporais) exigirá enriquecimento da base.
3. **Não há comorbidades raras** nem interações medicamentosas.
4. **Os ECGs sintéticos** têm morfologia simplificada e derivação única; servem
   para exercitar pipeline de visão computacional, não para validação clínica.
5. **O corpus textual** é gerado por template — tem menos variabilidade
   linguística que texto humano real (abreviações, erros de digitação, jargão
   idiossincrático). Isso deve ser considerado ao avaliar o NLP.

---

## 6. Aviso de uso

> **Nenhum arquivo deste repositório contém dado de pessoa real.**
> Nenhum conteúdo aqui constitui orientação médica. As bases destinam-se
> exclusivamente ao desenvolvimento acadêmico do projeto CardioIA (FIAP).
