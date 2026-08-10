# Dicionário de Dados — `cardioia_pacientes.csv`

800 linhas × 33 colunas. Separador `,`. Codificação UTF-8.
Chave primária: `id_paciente` (também liga o corpus textual e, futuramente, os ECGs).

| # | Coluna | Tipo | Unidade / Domínio | Descrição | Relevância clínica |
|---|--------|------|-------------------|-----------|--------------------|
| 1 | `id_paciente` | texto | `CARD-0001`…`CARD-0800` | Identificador pseudonimizado | Chave de junção multimodal |
| 2 | `idade` | int | 29–92 anos | Idade na consulta índice | ⭐⭐⭐ Preditor isolado mais forte de risco CV |
| 3 | `sexo` | cat | `M` / `F` | Sexo biológico | ⭐⭐⭐ Modifica risco **e** apresentação sintomática |
| 4 | `regiao_atendimento` | cat | Capital / RM / Interior / Zona Rural | Origem do atendimento | ⭐ Variável de **auditoria de equidade**, não de diagnóstico |
| 5 | `imc` | float | 16,5–47,0 kg/m² | Índice de massa corporal | ⭐⭐ Fator de risco modificável |
| 6 | `tabagismo` | bin | 0/1 | Tabagismo ativo | ⭐⭐⭐ Maior fator de risco modificável isolado |
| 7 | `etilismo` | ord | 0 não, 1 social, 2 de risco | Consumo de álcool | ⭐ Associado a HAS e arritmias |
| 8 | `diabetes` | bin | 0/1 | DM tipo 2 diagnosticado | ⭐⭐⭐ Equivalente de risco coronariano |
| 9 | `hipertensao_diagnosticada` | bin | 0/1 | HAS prévia | ⭐⭐⭐ Principal causa de IC e AVC |
| 10 | `historico_familiar_dac` | bin | 0/1 | DAC precoce em parente 1º grau | ⭐⭐ Componente não modificável |
| 11 | `dias_ativos_semana` | int | 0–7 | Dias com atividade física | ⭐⭐ Proxy de sedentarismo |
| 12 | `pressao_sistolica` | int | 88–215 mmHg | PAS no consultório | ⭐⭐⭐ Alvo terapêutico direto |
| 13 | `pressao_diastolica` | int | 52–130 mmHg | PAD no consultório | ⭐⭐ |
| 14 | `frequencia_cardiaca_repouso` | int | 42–128 bpm | FC de repouso | ⭐⭐ FC elevada em repouso = pior prognóstico |
| 15 | `fc_maxima_esforco` | int | 78–202 bpm | FC máxima no teste de esforço | ⭐⭐ Incompetência cronotrópica |
| 16 | `saturacao_o2` | int | 84–100 % | SpO₂ | ⭐⭐ Sinal de descompensação |
| 17 | `colesterol_total` | int | mg/dL | Colesterol total | ⭐ Menos informativo que as frações |
| 18 | `colesterol_ldl` | int | 45–265 mg/dL | LDL ("ruim") | ⭐⭐⭐ Alvo causal da aterosclerose |
| 19 | `colesterol_hdl` | int | 18–96 mg/dL | HDL ("bom") | ⭐⭐⭐ Efeito **protetor** — sinal invertido |
| 20 | `triglicerides` | int | 45–620 mg/dL | Triglicérides | ⭐⭐ Distribuição log-normal |
| 21 | `glicemia_jejum` | int | 62–310 mg/dL | Glicemia de jejum | ⭐⭐ Confirma/gradua o diabetes |
| 22 | `dor_toracica_tipo` | cat | Típica / Atípica / Não anginosa / Assintomático | Caracterização da dor | ⭐⭐⭐ Maior valor preditivo da anamnese |
| 23 | `dispneia_esforco` | bin | 0/1 | Falta de ar aos esforços | ⭐⭐ Sintoma cardinal de IC |
| 24 | `palpitacoes` | bin | 0/1 | Palpitações | ⭐⭐ Sugere arritmia |
| 25 | `sincope` | bin | 0/1 | Desmaio | ⭐⭐⭐ Sinal de alarme |
| 26 | `edema_mmii` | bin | 0/1 | Edema de membros inferiores | ⭐⭐ Congestão sistêmica |
| 27 | `fadiga` | bin | 0/1 | Fadiga | ⭐ Inespecífico, mas frequente em mulheres |
| 28 | `classe_funcional_nyha` | ord | I–IV | Limitação funcional | ⭐⭐⭐ Padrão internacional de gravidade |
| 29 | `ecg_repouso` | cat | Normal / Alteração ST-T / HVE / FA | Laudo do ECG | ⭐⭐⭐ Ponte com a base de imagens |
| 30 | `tempo_ate_atendimento_min` | int | minutos | Tempo até o 1º atendimento | ⭐ Equidade de acesso (ver Governança §3.2) |
| 31 | `escore_risco_10a_pct` | float | 0,4–79 % | Risco estimado em 10 anos | ⭐⭐ Alvo de regressão |
| 32 | `risco_cardiovascular` | cat | Baixo / Intermediário / Alto | Estratificação | 🎯 **Alvo de classificação multiclasse** |
| 33 | `evento_cardiaco_12m` | bin | 0/1 | Evento CV maior em 12 meses | 🎯 **Alvo binário principal** (prevalência ≈ 18%) |

## Dados ausentes (propositais)

`colesterol_hdl`, `triglicerides`, `glicemia_jejum` e `imc` têm ausências
**não aleatórias** (MAR): ~11% em Interior/Zona Rural contra ~3% na Capital.
Ver `docs/GOVERNANCA_DE_DADOS.md`, seção 3.3.

## As 6 variáveis mais relevantes (justificativa resumida)

1. **`idade`** — o risco cardiovascular dobra aproximadamente a cada década.
2. **`dor_toracica_tipo`** — a anamnese bem feita ainda supera muitos exames em valor preditivo; é também o elo natural com o módulo de NLP.
3. **`colesterol_ldl` + `colesterol_hdl`** — a razão entre elas informa mais que o colesterol total; o HDL entra com sinal invertido, o que é um bom teste de sanidade para o modelo.
4. **`pressao_sistolica`** — fator de risco modificável com relação dose-resposta contínua, sem limiar de segurança.
5. **`diabetes`** — considerado equivalente de risco coronariano nas diretrizes.
6. **`ecg_repouso`** — único campo tabular que se conecta diretamente à base de imagens, viabilizando fusão multimodal na Fase 7.
