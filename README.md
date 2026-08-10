# AI Assistant v3.0

### Assistente Virtual Inteligente 

O **AI Assistant v3.0** é um sistema de chatbot técnico baseado em **Modelos de Linguagem de Grande Porte (LLMs)** executados localmente via **Ollama**, integrado a uma arquitetura completa de **Geração Aumentada por Recuperação (RAG)**.

O objetivo principal do sistema é atuar como um assistente, O assistente fornece respostas precisas e contextualizadas a partir de uma base documental interna (manuais, PDFs técnicos, relatórios e documentação operacional), garantindo privacidade total, segurança de dados corporativos e execução 100% local.

---

# 📋 Pré-requisitos

Antes de executar o sistema, certifique-se de possuir:

* Python 3.10 
* Ollama instalado e em execução localmente
* Ambiente Linux recomendado para melhor compatibilidade

## Modelos Necessários

```bash
ollama pull llama3.1:8b
ollama pull snowflake-arctic-embed2:568m
```

---

# 🧠 Arquitetura Geral do Sistema

O sistema é dividido em dois pipelines principais, independentes e modulares, que compartilham o mesmo banco vetorial persistente (**ChromaDB**).

## 1. Pipeline de Ingestão (ETL Offline)

Responsável por construir e atualizar a base de conhecimento vetorial a partir de documentos técnicos em formato PDF.

```text
[ PDFs Técnicos ]
       │
       ▼
[ Leitura e Extração (PyMuPDF) ]
       │
       ▼
[ Limpeza + Chunking Semântico ]
       │
       ▼
[ Geração de Embeddings Locais ]
       │
       ▼
[ Armazenamento Vetorial ] ──► ChromaDB (chroma.sqlite3)
```

### Etapas Principais

* Varredura automática e leitura de PDFs técnicos na pasta `APP_BANCO/pdf/`
* Extração robusta de texto utilizando PyMuPDF (`fitz`)
* Normalização e limpeza de caracteres especiais
* Segmentação em chunks com overlap para preservar contexto
* Geração de embeddings locais
* Indexação e persistência dos vetores no ChromaDB

---

## 2. Pipeline RAG (Consulta em Tempo Real)

Responsável pela interface do usuário e orquestração da busca semântica combinada com a geração de texto pelo modelo local.

```text
┌────────────────────────────────────────────────────────┐
│               Interface do Usuário (Streamlit)         │
│             APP/front_end/interface_main.py        │
└───────────────────────────┬────────────────────────────┘
                            │
                    Pergunta do Usuário
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                    Orquestrador RAG                    │
│           APP/Rag/llm_resposta_usuario.py          │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
   [ Busca Vetorial ]              [ LLM Local (Ollama) ]
   (busca_vetorial.py)             (Injeção de Contexto)
            │                               │
            └───────────────┬───────────────┘
                            ▼
              [ Contexto + Prompt Técnico ]
                            │
                            ▼
                    [ Resposta Final ]
```

### Fluxo de Execução

1. O usuário submete uma pergunta através da interface Streamlit.
2. A consulta é convertida em embedding.
3. O ChromaDB realiza a busca semântica dos documentos mais relevantes.
4. O contexto recuperado é incorporado ao prompt do sistema.
5. O modelo local gera uma resposta baseada exclusivamente nas informações recuperadas.

---

# 📁 Estrutura do Projeto

```text
projeto-assistente-ia-v3.0/
│
├── .streamlit/
│   └── config.toml
│
├── .vscode/
│   └── settings.json
│
├── banco_em_produção/producao
│
│
├── APP/
│   ├── busca_vetorial/
│   │   └── busca_vetorial.py
│   ├── front_end/
│   │   └── interface_main.py
│   ├── prompt/
│   │   ├── conf_prompt.py
│   │   └── prompt_2.txt
│   └── Rag/
│       └── llm_resposta_usuario.py
│
|
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🖥️ Requisitos de Hardware

### Mínimo

* CPU moderna (Intel i7 ou AMD Ryzen 7)
* 16 GB RAM
* SSD recomendado

### Recomendado

* GPU NVIDIA com suporte CUDA
* 8 GB ou mais de VRAM
* 16–32 GB RAM
* SSD NVMe

### Espaço em Disco

* Aproximadamente 15 GB livres para modelos Ollama e banco vetorial

---

# 🚀 Como Executar

## 1. Criar Ambiente Virtual

```bash
micromamba create -n nome
micromamba activate nome
```

## 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 3. Baixar os Modelos

_**Dependedo do seu so escolhas as opções de instalação do ollama:**_


```text
linux ubuntu : bash curl -fsSL https://ollama.com/install.sh | sh 

windows : "irm https://ollama.com/install.ps1 | iex"
```

Depois baixe os modelos a seguir

```bash
ollama pull llama3.1:8b # ou o modelo de sua preferência

ollama pull snowflake-arctic-embed2:568m # e importante que o mesmo modelo usado para criar os embeddigns, seja o memso usado na busca #vetorial
```


## 4. Iniciar a Aplicação

```bash

streamlit run APP_RAG/front_end/interface_main.py

# caso queira executa usando sua maquina como servido local

streamlit run APP_RAG/front_end/interface_main.py --server.address 0.0.0.0 --server.port 8501
```

A aplicação ficará disponível em:

```text
http://localhost:8501
```

---

# ⚙️ Configurações

| Variável          | Valor Padrão                 | Descrição                                |
| ----------------- | ---------------------------- | ---------------------------------------- |
| OLLAMA_MODEL      | llama3.1:8b                  | Modelo principal de geração              |
| EMBEDDING_MODEL   | snowflake-arctic-embed2:568m | Modelo de embeddings                     |
| CHROMA_DB_PATH    | ./APP_BANCO/banco            | Local do banco vetorial                  |
| RAG_TOP_K         | 6                            | Quantidade de chunks recuperados         |
| MODEL_KEEP_ALIVE  | 5m                           | Tempo de permanência do modelo carregado |
| MODEL_NUM_THREADS | 8                            | Número de threads utilizadas             |

---

# 🧩 Principais Tecnologias

### IA e Inferência

* Ollama


### Busca Vetorial

* ChromaDB


### Interface

* Streamlit

# 🔐 Segurança e Privacidade

* Execução 100% local
* Nenhuma dependência obrigatória de APIs externas
* Dados permanecem dentro da infraestrutura institucional
* Controle total sobre prompts, documentos e modelos utilizados
* Adequado para ambientes com requisitos de confidencialidade e governança de dados

---

# 📄 Licença

**open source**

