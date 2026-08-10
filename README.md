# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://tse2.mm.bing.net/th/id/OIP.3xs_MSeNC0T1UOrJaCEqWAHaEK?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# ❤️ CardioIA — Fase 1: Batimentos de Dados

> **Construção da base de dados multimodal** que alimentará as Fases 2 a 7 do projeto CardioIA — dados numéricos, textuais e visuais gerados por código versionado, alinhados pela mesma chave de paciente.

<p align="center">
<a href="https://www.fiap.com.br/"><img src="https://avatars.githubusercontent.com/u/85091676?s=200" alt="FIAP" width="200"></a>
</p>

---

## 👨‍⚕️ Integrantes do Grupo
- Miriã Leal Mantovani (RM567811) — 2TIAOR-2026
- João Pedro Santos Azevedo (RM566701) — 2TIAOR-2026

## 👩‍🏫 Tutores
- Leonardo Ruiz Orabona

---

> ⚠️ **Aviso:** todos os dados clínicos deste repositório são **simulados**.
> Nenhum dado de pessoa real foi coletado, tratado ou publicado.
> Nada aqui constitui orientação médica.

---

## 📑 Sumário
- [Links dos Dados em Nuvem](#-links-dos-dados-em-nuvem)
- [Pré-requisitos](#-pré-requisitos)
- [Como Rodar o Projeto](#-como-rodar-o-projeto-passo-a-passo-detalhado)
- [O que torna esta entrega diferente](#-o-que-torna-esta-entrega-diferente)
- [Parte 1 — Dados Numéricos](#-parte-1--dados-numéricos)
- [Parte 2 — Dados Textuais](#-parte-2--dados-textuais)
- [Parte 3 — Dados Visuais](#-parte-3--dados-visuais)
- [Governança de Dados, LGPD e Viés](#-governança-de-dados-lgpd-e-viés)
- [Troubleshooting](#-troubleshooting--problemas-comuns)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Ponte para as Próximas Fases](#-ponte-para-as-próximas-fases)
- [Vídeo de Demonstração](#-vídeo-de-demonstração)

---

## 🔗 Links dos Dados em Nuvem

> Configure o compartilhamento como *"Qualquer pessoa com o link pode visualizar"*
> para que a equipe FIAP consiga acessar durante a correção.

| Conjunto | Formato | Volume | Link público |
|----------|---------|--------|--------------|
| **Parte 1** — Dados numéricos | `.csv` + `.xlsx` | 800 linhas × 33 colunas | `https://drive.google.com/drive/u/1/folders/10-KjjKzmAhrhZYlPHX-fhsbF4kMmTK_1` |
| **Parte 2** — Dados textuais | 4 × `.txt` | ~83 mil palavras | `https://drive.google.com/drive/u/1/folders/16-ujb53o-viimmShOm-SEFgoX9SVzU8C` |
| **Parte 3** — Imagens de ECG | 120 × `.png` | 6 classes | `https://drive.google.com/drive/u/1/folders/17_9TrlV4x6Y4E44yc-lKYaIuhG3iTi_9` |
| **Pacote completo** (tudo) | `.zip` | ~4 MB | `COLE_O_LINK_AQUI` |

📄 **Documento resumo da entrega:** [`docs/CardioIA_Fase1_Documento_Resumo.pdf`](docs/CardioIA_Fase1_Documento_Resumo.pdf)
(versão editável em `.docx` na mesma pasta)

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

| Software | Versão mínima | Como verificar | Como instalar |
|---|---|---|---|
| **Python** | 3.10+ | `python --version` | https://python.org/downloads (marque "Add to PATH" no Windows) |
| **pip** | 23.0+ | `pip --version` | Já vem com Python |
| **Git** | 2.30+ | `git --version` | https://git-scm.com/downloads |
| **VS Code** (recomendado) | qualquer | — | https://code.visualstudio.com |

### Espaço em disco
- **Mínimo**: 150 MB (dados já gerados, sem regenerar)
- **Completo**: 400 MB (com ambiente virtual e dependências)

### Sistema operacional
- ✅ Windows 10/11
- ✅ macOS 11+
- ✅ Linux (Ubuntu 20.04+, Debian 11+)

### Conexão com a internet
Necessária **apenas** para o script `src/04_baixar_textos_publicos.py`, que baixa
as duas obras de domínio público do Project Gutenberg. Todo o restante roda offline.

---

## 🚀 Como Rodar o Projeto (passo a passo detalhado)

### 1️⃣ Clonar o repositório e entrar na pasta

```bash
git clone https://github.com/joaostazevedo172/cardioia-fase1.git
cd cardioia-fase1
```

Se você baixou o ZIP:

```bash
# Linux/Mac
unzip CardioIA_Fase1_completo.zip
cd cardioia-fase1
```

```powershell
# Windows (PowerShell)
Expand-Archive CardioIA_Fase1_completo.zip -DestinationPath .
cd cardioia-fase1
```

#### ✅ Verificação:
Liste os arquivos com `ls` (Linux/Mac) ou `dir` (Windows). Você deve ver:
```
README.md      requirements.txt    .gitignore
data/          docs/               assets/         src/          notebooks/
```

---

### 2️⃣ Criar e ativar ambiente virtual (MUITO recomendado)

O ambiente virtual isola as dependências do projeto, evitando conflitos com outros
projetos Python no seu computador.

#### 🪟 Windows (PowerShell)

```powershell
# Criar o ambiente virtual
python -m venv venv

# Se aparecer erro de "execution policy", rode UMA vez:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Ativar o ambiente
venv\Scripts\Activate.ps1
```

#### 🪟 Windows (CMD tradicional)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### 🐧 Linux / 🍎 macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### ✅ Verificação:
Você saberá que ativou quando aparecer **`(venv)`** no início do prompt do terminal:

```bash
(venv) $ _              # Linux/Mac
(venv) PS C:\...> _     # Windows PowerShell
```

> 💡 **Dica:** sempre que abrir um novo terminal para trabalhar no projeto, ative o
> ambiente novamente com o comando da etapa 2. Para sair: `deactivate`.

---

### 3️⃣ Instalar dependências

#### Atualize o pip primeiro (recomendado)
```bash
python -m pip install --upgrade pip
```

#### Instale tudo de uma vez
```bash
pip install -r requirements.txt
```

#### ⏱️ Tempo esperado de instalação

| Pacote | Tamanho | Tempo médio |
|---|---|---|
| numpy, pandas | ~60 MB | 30-60s |
| matplotlib | ~40 MB | 20-40s |
| openpyxl | ~2 MB | 5s |
| jupyter | ~90 MB | 1-2 min |

> 💡 Nenhuma dependência pesada (sem `torch`, sem `tensorflow`). A instalação
> completa leva cerca de **3 minutos** em conexão média.

#### ✅ Verificação:
```bash
pip list | grep pandas       # Linux/Mac
pip list | findstr pandas    # Windows
```
Deve mostrar `pandas 2.0.0` ou superior.

---

### 4️⃣ Gerar as três bases de dados

Os dados já vêm prontos no repositório, mas **todos podem ser regenerados do zero**.
Rode os scripts **na ordem numérica** — o `03` depende do CSV gerado pelo `01`.

```bash
# Parte 1 — coorte sintética de 800 pacientes (~2s)
python src/01_gerar_dataset_numerico.py

# Parte 3 — 120 imagens de ECG em 6 classes (~40s)
python src/02_gerar_imagens_ecg.py 20

# Parte 2a — prontuários e diálogos autorais (~3s)
python src/03_gerar_corpus_textual.py

# Parte 2b — obras de domínio público do Gutenberg (requer internet, ~10s)
python src/04_baixar_textos_publicos.py
```

#### ✅ Verificação:
Cada script imprime um resumo no terminal. O esperado é:

```
OK  data/cardioia_pacientes.csv
    800 linhas x 33 colunas
    prevalencia de evento em 12m: 18.0%

OK  120 imagens + data/ecg_labels.csv

OK  docs/texto_03_prontuarios_sinteticos_cardioia.txt  (45175 palavras)
OK  docs/texto_04_teleatendimento_dialogos_cardioia.txt  (10432 palavras)
```

> 💡 **Quer uma base maior?** `python src/02_gerar_imagens_ecg.py 100` gera 600
> imagens. Para mais pacientes, altere `N_PACIENTES` em `src/01`.

---

### 5️⃣ Abrir o notebook de exploração

```bash
jupyter notebook notebooks/01_exploracao_dados.ipynb
```

O navegador deve abrir automaticamente em `http://localhost:8888`. Se não abrir,
copie a URL com token que aparece no terminal.

#### O que o notebook faz (rode as células na ordem):

| Seção | Conteúdo |
|---|---|
| 1 | EDA da coorte: estrutura, tipos, distribuições clínicas, correlações |
| 2 | **Auditoria de viés** — sexo, acesso geográfico, desbalanceamento |
| 3 | Corpus textual: contagens, termos frequentes e **validação do alinhamento multimodal** |
| 4 | Imagens de ECG: distribuição por classe e amostra visual das 6 classes |
| 5 | **Checklist automático** conferindo as contagens mínimas da rubrica |

#### ✅ Verificação:
A última célula deve imprimir:

```
OK   Parte 1: 800 linhas (mínimo 100)
OK   Parte 2: 4 arquivos .txt (mínimo 2)
OK   Parte 3: 120 imagens .png (mínimo 100)
OK   README.md
OK   subpasta docs/
OK   documento de governança
```

#### Para parar o servidor:
Pressione `Ctrl+C` no terminal (duas vezes).

---

### 6️⃣ Publicar os dados em nuvem

1. Compacte a pasta ou envie `data/`, `docs/` e `assets/` para o Google Drive ou OneDrive
2. Clique com o botão direito → **Compartilhar** → **Qualquer pessoa com o link**
3. Copie os links e cole na tabela [Links dos Dados em Nuvem](#-links-dos-dados-em-nuvem) deste README
4. Faça o commit e o push:

```bash
git add .
git commit -m "Fase 1 - Batimentos de Dados"
git push origin main
```

---

## 🎯 O que torna esta entrega diferente

A maior parte dos grupos baixa o *UCI Heart Disease* (303 linhas, usado em
milhares de tutoriais), pega dois PDFs soltos e um pacote de raios-X do Kaggle.
As três bases ficam **desconectadas** — e o projeto vira três exercícios isolados.

Nossa decisão foi outra: **construir um ecossistema de dados coerente e autoral**,
apoiado em três escolhas de projeto.

### 1. Tudo é gerado por código versionado, não baixado

Cada base tem um script gerador em `src/`, com **seed fixa (`20260806`)**. Isso dá:

- **reprodutibilidade** — qualquer pessoa regenera exatamente os mesmos arquivos;
- **rastreabilidade total** — sabemos qual é o *processo gerador* dos dados;
- **zero risco de LGPD** — dado de saúde é dado sensível (Art. 11);
- **unicidade** — nenhum outro grupo terá esta base.

### 2. As três modalidades falam a mesma língua

O `id_paciente` (`CARD-0001`) é a **chave de junção multimodal**:

```
 data/cardioia_pacientes.csv ──┐
                               ├── id_paciente ──► mesmo paciente
 docs/texto_03_prontuarios ────┤                   nas três modalidades
 docs/texto_04_teleatendimento ┘
        │
 data/ecg_labels.csv ──── ecg_repouso ──► classe da imagem
```

O prontuário do `CARD-0634` **descreve exatamente** a linha `CARD-0634` do CSV. Isso
viabiliza, nas fases seguintes, coisas que uma base desconectada não permite:

- validar extração de entidades por NLP **contra o gabarito tabular**;
- comparar, no mesmo paciente, o desempenho de ML tabular vs. NLP;
- fazer **fusão multimodal (late fusion)** de tabela + texto + imagem na Fase 7.

### 3. Os vieses foram injetados de propósito — e documentados

Base sintética "perfeita" ensina o grupo a ignorar o problema mais importante da
IA em saúde. Colocamos vieses reais e mensuráveis: sub-representação feminina,
desigualdade geográfica de acesso e ausência de dados não aleatória.
Tudo detalhado em **[`docs/GOVERNANCA_DE_DADOS.md`](docs/GOVERNANCA_DE_DADOS.md)**.

---

## 📊 Parte 1 — Dados Numéricos

**Arquivos:** `data/cardioia_pacientes.csv` · `data/cardioia_pacientes.xlsx`
**Gerador:** `src/01_gerar_dataset_numerico.py`
**Dicionário completo:** [`data/dicionario_de_dados.md`](data/dicionario_de_dados.md)

### Origem dos dados

**Simulados.** A "Coorte Sintética Hospital CardioIA" tem 800 pacientes fictícios
(a rubrica pede no mínimo 100). Não se trata de amostragem aleatória independente:
cada variável foi gerada **condicionada às anteriores**, segundo relações de
dependência descritas na literatura (estudo de Framingham; diretrizes da SBC e da
AHA). Exemplos do modelo:

```python
pressao_sistolica ~ 108 + 0.42·(idade−30) + 22·hipertensao + 0.9·(imc−25) + ruído
colesterol_hdl    ~  58 −  8·(sexo=M) − 6·tabagismo − 0.55·(imc−25) + 1.1·dias_ativos
```

O desfecho vem de um **modelo logístico explícito** — o *ground truth* do processo
gerador, que ficará disponível para conferir se o modelo da Fase 2 aprendeu a
relação certa:

```python
logit(evento) = −3.55 + 0.055·(idade−55) + 0.62·(sexo=M) + 0.78·tabagismo
                + 0.85·diabetes + 0.60·hipertensao + 0.55·hist_familiar
                + 0.016·(PAS−120) + 0.011·(LDL−100) − 0.020·(HDL−50)
                + 0.045·(IMC−25) − 0.070·dias_ativos + ...
```

### Perfil da base

| Indicador | Valor |
|---|---|
| Pacientes | 800 |
| Variáveis | 33 |
| Prevalência de evento em 12 meses | ≈ 18% |
| Distribuição de risco | Baixo 29% · Intermediário 36% · Alto 35% |
| Sexo | 58% M / 42% F (viés deliberado — ver Governança) |
| Células ausentes | ≈ 200, com padrão MAR proposital |

### Variáveis mais relevantes do ponto de vista clínico

| Variável | Por que importa para um projeto de IA em saúde |
|---|---|
| **`idade`** | Preditor isolado mais forte de risco cardiovascular — o risco praticamente dobra a cada década. É também a variável que mais facilmente vira um *atalho* para o modelo: se ele acertar só pela idade, não aprendeu cardiologia. |
| **`dor_toracica_tipo`** | Uma anamnese bem feita ainda supera vários exames em valor preditivo. É a ponte natural entre o módulo tabular e o de NLP — o mesmo dado aparece em texto livre nos prontuários. |
| **`colesterol_ldl` e `colesterol_hdl`** | O LDL é o alvo causal da aterosclerose; o HDL entra com **sinal invertido** (protetor). Se o modelo aprender que "HDL alto = risco alto", há vazamento ou erro de sinal — é um excelente teste de sanidade. |
| **`pressao_sistolica`** | Fator modificável com relação dose-resposta contínua e sem limiar de segurança. Também é a variável que virá do wearable ESP32 na Fase 3, o que a torna a ponte com o módulo de IoT. |
| **`diabetes`** | Tratado nas diretrizes como equivalente de risco coronariano. Interage fortemente com IMC e glicemia — bom caso para testar se o modelo captura interações ou só efeitos aditivos. |
| **`ecg_repouso`** | Único campo tabular que se conecta diretamente à base de imagens, viabilizando a fusão multimodal da Fase 7. |
| **`evento_cardiaco_12m`** | Alvo principal. Com 18% de prevalência, obriga o uso de **recall, F1 e AUC-PR** — acurácia é enganosa aqui (prever "ninguém infarta" já acerta 82%). |

---

## 📝 Parte 2 — Dados Textuais

**Arquivos:** pasta [`docs/`](docs/) — 4 arquivos `.txt`, ~83 mil palavras.

| Arquivo | Origem | Natureza | Palavras |
|---|---|---|---|
| `texto_01_harvey_1628_de_motu_cordis.txt` | Project Gutenberg #67065 — **domínio público** | Tratado fundador da cardiologia (Harvey, 1628) | ~20.000 |
| `texto_02_huxley_1878_descoberta_da_circulacao.txt` | Project Gutenberg #2939 — **domínio público** | Texto expositivo/divulgação (Huxley, 1878) | ~8.000 |
| `texto_03_prontuarios_sinteticos_cardioia.txt` | **Autoral** — `src/03` | 300 prontuários em português, alinhados ao CSV | ~45.000 |
| `texto_04_teleatendimento_dialogos_cardioia.txt` | **Autoral** — `src/03` | 200 diálogos paciente↔assistente, rotulados | ~10.000 |

Os dois primeiros são baixados por `src/04_baixar_textos_publicos.py` (o script
remove automaticamente o cabeçalho e o rodapé de licença do Gutenberg — caso
contrário o modelo de NLP aprenderia esse ruído jurídico repetido).
Os dois últimos são gerados por `src/03_gerar_corpus_textual.py`.

Cada diálogo já vem **rotulado em três dimensões** (também disponível em formato
tabular em `data/corpus_teleatendimento.csv`):

```
--- ATENDIMENTO 001 | paciente: CARD-0679 | canal: chat_web
    | intencao: sintoma_emergencia | urgencia: critica | sentimento: negativo ---
PACIENTE: Estou com uma dor forte no peito agora, que vai pro braco esquerdo, e suando frio.
ASSISTENTE: Isso pode ser um infarto. Ligue imediatamente para o SAMU 192 [...]
```

### Como esses textos podem ser explorados por algoritmos de NLP

**a) Extração de entidades clínicas (NER) — com gabarito.**
Rodar NER sobre os prontuários para extrair sintomas, medicações e valores de
exame. O diferencial: **a resposta certa está no CSV**. Podemos calcular
precisão e recall reais da extração, algo raríssimo em corpus público —
normalmente seria necessário anotar tudo à mão.

**b) Classificação de intenção e triagem por urgência.**
Os 200 diálogos rotulados treinam o classificador que decide se uma mensagem é
emergência (`sintoma_emergencia` → orientar SAMU) ou dúvida administrativa
(`agendamento`). É o núcleo do chatbot da Fase 5. Em saúde, o erro não é
simétrico: classificar emergência como rotina pode custar uma vida, então o
modelo deve ser otimizado para **recall na classe crítica**, aceitando falsos
positivos.

**c) Análise de sentimento aplicada à adesão.**
Os rótulos `ansioso`, `preocupado`, `negativo`, `positivo` permitem detectar
pacientes em sofrimento emocional — que abandonam tratamento com mais frequência.
Um assistente que só responde tecnicamente a "estou com medo do cateterismo"
perde o paciente.

**d) Classificação de tópicos e mapeamento de barreiras de acesso.**
Agrupar as mensagens revela padrões acionáveis: `acesso_tratamento` concentra
relatos de custo de medicação e distância — informação de gestão, não só clínica.

**e) Contraste diacrônico de linguagem médica (Harvey/Huxley vs. prontuários).**
Comparar o vocabulário do século XVII com o prontuário contemporâneo é um
laboratório de *domain shift*: um modelo treinado em texto moderno degrada em
texto histórico, e vice-versa. É a forma mais didática de mostrar por que um
modelo treinado no hospital A pode falhar no hospital B.

### Por que isso é relevante para IA em saúde

Estima-se que a maior parte da informação clínica registrada esteja em **texto
livre**, não em campos estruturados. Um projeto de IA em saúde que só consome
tabelas ignora a maior parte do que o médico realmente escreveu. Além disso, o
corpus textual é a única modalidade que carrega a **voz do paciente** — o que ele
sente, teme e não consegue pagar. Sem isso, o sistema otimiza o diagnóstico e
falha na adesão, que é onde o tratamento cardiovascular costuma naufragar.

---

## 📷 Parte 3 — Dados Visuais

**Arquivos:** `assets/ecg/<classe>/` — **120 imagens `.png`**
**Manifesto rotulado:** `data/ecg_labels.csv`
**Gerador:** `src/02_gerar_imagens_ecg.py`

### Origem

**Simuladas.** Cada traçado é sintetizado como soma de componentes gaussianas
representando as ondas **P, Q, R, S e T** — abordagem inspirada no gerador
ECGSYN (McSharry et al., 2003), reimplementada de forma simplificada e autoral.
O sinal é renderizado sobre papel milimetrado no padrão clínico
(**25 mm/s, 10 mm/mV**), com grade fina de 0,04 s e grossa de 0,2 s.

| Classe | Imagens | Achado simulado | FC média |
|---|---|---|---|
| `normal` | 20 | Ritmo sinusal | ~75 bpm |
| `taquicardia_sinusal` | 20 | FC > 100 bpm | ~132 bpm |
| `bradicardia_sinusal` | 20 | FC < 55 bpm | ~46 bpm |
| `fibrilacao_atrial` | 20 | Ausência de onda P + RR irregular | ~106 bpm |
| `isquemia_infra_st` | 20 | Infradesnivelamento de ST | ~75 bpm |
| `iam_supra_st` | 20 | Supradesnivelamento de ST + T apiculada | ~90 bpm |

**Ruídos realistas injetados de propósito:** deriva de linha de base
(respiração, 0,15–0,4 Hz), interferência da rede elétrica em 60 Hz, ruído
eletromiográfico de alta frequência e variabilidade de amplitude entre
"pacientes". Sem eles, a CNN aprenderia um traçado limpo demais e desabaria
diante de qualquer exame real.

### Como essas imagens podem ser analisadas por Visão Computacional

**a) Classificação por CNN.** Base balanceada (20 por classe) e rotulada, pronta
para transfer learning (ResNet/EfficientNet). O balanceamento aqui é intencional
e contrasta de propósito com o desbalanceamento da base tabular — as duas
situações exigem estratégias diferentes.

**b) Detecção de bordas e segmentação do complexo QRS.** Filtros de Sobel/Canny
isolam o pico R; a partir dele calculam-se intervalos RR, frequência cardíaca e
variabilidade (HRV). O `data/ecg_labels.csv` já traz a **FC estimada por detecção
de picos com período refratário de 200 ms**, servindo de gabarito para validar a
implementação do grupo.

**c) Reconhecimento de anomalias no segmento ST.** As classes `isquemia_infra_st`
e `iam_supra_st` diferem por um deslocamento sutil de poucos pixels em uma região
específica. É o caso ideal para **mapas de atenção (Grad-CAM)**: se a rede
destacar o segmento ST, ela aprendeu o achado clínico; se destacar a grade do
papel ou a borda da imagem, aprendeu um artefato — e o modelo é inútil apesar da
métrica boa.

**d) Detecção de anomalias sem rótulo.** Treinar um autoencoder apenas com a
classe `normal` e usar o erro de reconstrução como escore de anormalidade.
Espelha o cenário hospitalar real, em que exames normais são abundantes e os
patológicos, raros.

**e) Robustez a artefatos.** Como controlamos a geração do ruído, podemos variar
sua intensidade e medir a queda de desempenho — um teste de estresse que uma base
baixada pronta não permite.

### Por que isso é relevante para IA em saúde

O ECG é o exame cardiológico mais barato, rápido e disponível do mundo — e sua
interpretação depende de treinamento especializado que falta em boa parte da rede
básica. Um classificador confiável de ECG é, na prática, **triagem em escala**:
identifica quem precisa de cardiologista agora e quem pode esperar. Combinado com
o wearable da Fase 3, deixa de ser um exame pontual e vira monitoramento contínuo.

E há a lição que sustenta todo o resto: em imagem médica o modelo aprende com
enorme facilidade o atalho errado (o formato do papel, o texto do cabeçalho, o
equipamento usado). Sem interpretabilidade, não há uso clínico responsável.

---

## 🔐 Governança de Dados, LGPD e Viés

Documento completo: **[`docs/GOVERNANCA_DE_DADOS.md`](docs/GOVERNANCA_DE_DADOS.md)**. Em resumo:

- **LGPD** — dado de saúde é dado pessoal **sensível** (Art. 5º, II e Art. 11).
  Dado sintético contorna o problema na origem: não há titular a proteger.
- **Ciclo de vida documentado** — origem, coleta, armazenamento, qualidade, uso,
  retenção e descarte, com papéis definidos (*owner*, *steward*, revisor de viés).
- **Vieses mantidos e medidos** — sexo (58/42), acesso geográfico, ausência MAR e
  desbalanceamento de classe. Cada um com a métrica correspondente a monitorar.
- **Limitações declaradas** — bom desempenho nesta base **não** tem validade
  clínica; ela serve para exercitar o pipeline, não para diagnosticar ninguém.

### Vieses deliberados e como auditá-los

| Viés | Como está codificado | Métrica a monitorar |
|---|---|---|
| **Sexo** (58% M) | Mulheres recebem mais dor **atípica**, reproduzindo o padrão clínico real de subdiagnóstico feminino | *Recall* por sexo nas Fases 2 e 6 |
| **Acesso geográfico** | Tempo até atendimento: ~26 min na Capital contra ~105 min na Zona Rural | Tratar como variável de **auditoria**, nunca como *feature* de diagnóstico |
| **Ausência MAR** | Exames faltam em ~11% no Interior contra ~3% na Capital | Manter indicador binário `_faltante` junto de qualquer imputação |
| **Desbalanceamento** | Prevalência de evento de ~18% | Recall, F1, AUC-PR e matriz de confusão — nunca acurácia isolada |

---

## 🆘 Troubleshooting / Problemas Comuns

### Erro: `python: command not found`
**Causa:** Python não está no PATH.
**Solução:** No Windows, reinstale o Python marcando "Add Python to PATH". No Linux, use `python3` em vez de `python`.

---

### Erro: `ModuleNotFoundError: No module named 'pandas'`
**Causa:** O ambiente virtual não está ativo ou as dependências não foram instaladas.
**Solução:**
```bash
# Verifique se tem (venv) no prompt. Se não tiver, ative:
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

### Erro: `Set-ExecutionPolicy : ...` (PowerShell)
**Causa:** Windows bloqueia execução de scripts por padrão.
**Solução:**
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Responda **"S"** quando pedir confirmação.

---

### Erro: `FileNotFoundError: data/cardioia_pacientes.csv` ao rodar o `src/03`
**Causa:** O gerador de textos lê a coorte numérica. Você pulou o `src/01`.
**Solução:** rode os scripts **na ordem**:
```bash
python src/01_gerar_dataset_numerico.py
python src/03_gerar_corpus_textual.py
```

---

### Erro: `URLError` / `timed out` ao rodar o `src/04`
**Causa:** Sem internet, proxy corporativo ou Project Gutenberg fora do ar.
**Solução:** Os dois arquivos já estão versionados em `docs/`. O script `04` só é
necessário se você quiser rebaixá-los. Pule esta etapa — a entrega continua completa.

---

### Aviso: `[aviso] xlsx nao gerado: No module named 'openpyxl'`
**Causa:** O `openpyxl` não foi instalado.
**Solução:**
```bash
pip install openpyxl
python src/01_gerar_dataset_numerico.py
```
O CSV é gerado normalmente mesmo sem o `openpyxl` — só o `.xlsx` fica faltando.

---

### O notebook abre mas as células dão erro de caminho
**Causa:** O notebook detecta a raiz do projeto pelo diretório de execução.
**Solução:** abra o Jupyter **a partir da raiz do repositório**, não de dentro de `notebooks/`:
```bash
cd cardioia-fase1
jupyter notebook notebooks/01_exploracao_dados.ipynb
```

---

### As imagens de ECG saem em branco ou com erro de backend
**Causa:** Ambiente sem interface gráfica (servidor, WSL sem X11).
**Solução:** O script já força o backend `Agg` do matplotlib. Se persistir:
```bash
export MPLBACKEND=Agg     # Linux/Mac
set MPLBACKEND=Agg        # Windows CMD
python src/02_gerar_imagens_ecg.py 20
```

---

### Porta 8888 já está em uso (Jupyter)
**Solução:** Use outra porta:
```bash
jupyter notebook --port 8889
```

---

### Regenerei os dados e os números ficaram diferentes
**Causa:** Alguém alterou a constante `SEED` em algum script.
**Solução:** todos os geradores usam `SEED = 20260806`. Restaure esse valor e os
arquivos voltam a ser idênticos, bit a bit.

---

## 📁 Estrutura do Repositório

```
cardioia-fase1/
│
├── README.md                           # Este arquivo
├── requirements.txt                    # Dependências
├── .gitignore
│
├── data/                               # 📊 Dados estruturados
│   ├── cardioia_pacientes.csv          # ⭐ Parte 1 (800 × 33)
│   ├── cardioia_pacientes.xlsx
│   ├── dicionario_de_dados.md          # Descrição das 33 colunas
│   ├── ecg_labels.csv                  # Manifesto rotulado das 120 imagens
│   └── corpus_teleatendimento.csv      # Diálogos em formato tabular
│
├── docs/                               # 📝 Textos e documentação
│   ├── texto_01_harvey_1628_de_motu_cordis.txt          # Domínio público
│   ├── texto_02_huxley_1878_descoberta_da_circulacao.txt # Domínio público
│   ├── texto_03_prontuarios_sinteticos_cardioia.txt     # ⭐ Autoral
│   ├── texto_04_teleatendimento_dialogos_cardioia.txt   # ⭐ Autoral
│   ├── GOVERNANCA_DE_DADOS.md          # LGPD, vieses, limitações
│   ├── CardioIA_Fase1_Documento_Resumo.docx
│   └── CardioIA_Fase1_Documento_Resumo.pdf
│
├── assets/                             # 📷 Imagens
│   └── ecg/
│       ├── normal/                     (20 .png)
│       ├── taquicardia_sinusal/        (20 .png)
│       ├── bradicardia_sinusal/        (20 .png)
│       ├── fibrilacao_atrial/          (20 .png)
│       ├── isquemia_infra_st/          (20 .png)
│       └── iam_supra_st/               (20 .png)
│
├── src/                                # 🐍 Scripts geradores
│   ├── 01_gerar_dataset_numerico.py    # Coorte sintética
│   ├── 02_gerar_imagens_ecg.py         # ECGs sintéticos
│   ├── 03_gerar_corpus_textual.py      # Prontuários e diálogos
│   └── 04_baixar_textos_publicos.py    # Project Gutenberg
│
└── notebooks/                          # 📓 Análise
    └── 01_exploracao_dados.ipynb       # EDA + auditoria de viés + checklist
```

Pastas já preparadas para as próximas fases: os notebooks do Colab/Jupyter das
Fases 2 a 7 consomem diretamente `data/` e `assets/`.

---

## 🧭 Ponte para as Próximas Fases

| Fase | O que já está pronto aqui |
|---|---|
| **2 — Diagnóstico automatizado** | `evento_cardiaco_12m` e `risco_cardiovascular` como alvos; *ground truth* do gerador para auditar o que o modelo aprendeu |
| **3 — Monitoramento IoT (ESP32)** | `pressao_sistolica`, `frequencia_cardiaca_repouso` e `saturacao_o2` são exatamente as leituras do wearable |
| **4 — Visão computacional** | 120 ECGs rotulados + manifesto com FC de referência |
| **5 — Assistente virtual** | 200 diálogos com intenção, urgência e sentimento rotulados |
| **6 — Previsão de crises** | Base preparada para enriquecimento temporal (ver limitação nº 2 da Governança) |
| **7 — Plataforma integrada** | `id_paciente` já unifica tabela, texto e imagem para fusão multimodal |

---

## 🎬 Vídeo de Demonstração

🎥 **Demo Fase 1 — Batimentos de Dados**: `https://www.youtube.com/watch?v=6WVCRxFIfwg`

---

## 🧰 Tecnologias Utilizadas

- **Python 3.10+** — linguagem principal
- **NumPy** — geração estocástica das bases com seed controlada
- **Pandas** — manipulação e exportação dos dados tabulares
- **Matplotlib** — renderização dos traçados de ECG em papel milimetrado
- **openpyxl** — exportação em `.xlsx`
- **Jupyter Notebook** — exploração e auditoria de viés
- **Project Gutenberg** — acervo de obras médicas em domínio público

---

## 📚 Referências

- HARVEY, W. *An Anatomical Disquisition on the Motion of the Heart and Blood in Animals* (1628). [Project Gutenberg #67065](https://www.gutenberg.org/ebooks/67065)
- HUXLEY, T. H. *William Harvey and the Discovery of the Circulation of the Blood* (1878). [Project Gutenberg #2939](https://www.gutenberg.org/ebooks/2939)
- McSHARRY, P. E. et al. *A dynamical model for generating synthetic electrocardiogram signals.* IEEE Transactions on Biomedical Engineering, 2003.
- Sociedade Brasileira de Cardiologia — Diretrizes de Prevenção Cardiovascular.
- BRASIL. Lei nº 13.709/2018 (LGPD), Art. 5º, II e Art. 11.

---

## 📜 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sob <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

Os textos de Harvey e Huxley estão em domínio público (Project Gutenberg).
Os dados sintéticos são liberados para uso acadêmico.

---

## 🙏 Agradecimentos

Ao tutor **Leonardo Ruiz Orabona** pelo acompanhamento durante o desenvolvimento
desta fase. As orientações sobre governança de dados e viés em IA foram
determinantes para as escolhas metodológicas deste projeto.
