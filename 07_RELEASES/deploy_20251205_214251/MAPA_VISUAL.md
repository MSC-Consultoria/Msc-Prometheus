# 🗺️ MAPA VISUAL DO SISTEMA PROMETHEUS

**Diagrama da arquitetura completa implementada**

---

## 📊 ARQUITETURA GERAL

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROMETHEUS - SISTEMA COMPLETO                │
└─────────────────────────────────────────────────────────────────┘

                              🌐 INTERNET
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                ┌───▼────┐  ┌─────▼─────┐  ┌────▼─────┐
                │ Browser│  │ Web Pages │  │ API Keys │
                └───┬────┘  └─────┬─────┘  └────┬─────┘
                    │             │             │
         ┌──────────▼─────────────▼─────────────▼──────────┐
         │          FRONTEND (index.html - 500 linhas)     │
         │                                                   │
         │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
         │  │ Task │ │Status│ │Timeline│Config│Import│  │
         │  │      │ │Agent │ │       │      │ Web  │  │
         │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
         │                                                   │
         │  Local Storage:                                   │
         │  - API Key (encrypted)                           │
         │  - Configurações                                 │
         └─────────────────────┬─────────────────────────────┘
                               │
                     Fetch API (JSON)
                               │
         ┌─────────────────────▼─────────────────────────┐
         │      BACKEND API (Flask - api.py)             │
         │      Port 5000                                │
         │                                               │
         │ ┌─────────────────────────────────────────┐  │
         │ │ Endpoints:                              │  │
         │ │                                         │  │
         │ │ POST   /api/task                        │  │
         │ │        └─ Criar tarefa                  │  │
         │ │                                         │  │
         │ │ GET    /api/agent/stats                 │  │
         │ │        └─ Estatísticas do agente        │  │
         │ │                                         │  │
         │ │ GET    /api/agent/timeline              │  │
         │ │        └─ Histórico de tarefas          │  │
         │ │                                         │  │
         │ │ POST   /api/import-web                  │  │
         │ │        └─ Importar página web           │  │
         │ │                                         │  │
         │ │ GET    /api/imported-docs               │  │
         │ │        └─ Listar docs importados        │  │
         │ │                                         │  │
         │ │ GET/PUT /api/task/<id>                  │  │
         │ │        └─ Gerenciar tarefas             │  │
         │ │                                         │  │
         │ └─────────────────────────────────────────┘  │
         └────┬──────────────┬──────────────┬────────────┘
              │              │              │
              ▼              ▼              ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   AGENTE     │ │  INTEGRATIONS│ │  PERSISTÊNCIA│
    │ EVOLUTIVO    │ │              │ │              │
    │              │ │ WebImporter  │ │ JSON Files   │
    │ (core.py)    │ │ (350 linhas) │ │              │
    │              │ │              │ │ Tasks:       │
    │ Processa     │ │ - Download   │ │ - tasks.json │
    │ tarefas      │ │ - Parse HTML │ │              │
    │ com OpenAI   │ │ - HTML→MD    │ │ Imported:    │
    │ GPT          │ │ - Persistência
    │              │ │              │ │ - *.md files │
    │ Aprende      │ │              │ │ - index.json │
    │ continuamente│ │              │ │              │
    └──────────────┘ └──────────────┘ │ Evolution:   │
         │                            │ - history.   │
         │                            │   json       │
         │                            └──────────────┘
         │
         ▼
    ┌──────────────────────────────────────┐
    │  OPENAI API (GPT-4o-mini)            │
    │  Processamento com IA                │
    │  Aprendizado contínuo                │
    └──────────────────────────────────────┘
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
03_INFRAESTRUTURA/
│
├── 📁 app/
│   │
│   ├── 📁 agents/
│   │   └── 🐍 evolutionary_agent.py      (❤️ Core inteligência)
│   │       - Class: EvolutionaryAgent
│   │       - Processa tarefas com OpenAI
│   │       - Aprende e evolui
│   │       - 440 linhas
│   │
│   ├── 📁 backend/
│   │   └── 🐍 api.py                     (🚀 API REST Flask)
│   │       - 7 endpoints principais
│   │       - 5 novos endpoints (tarefas + web)
│   │       - CORS habilitado
│   │       - 360 linhas
│   │
│   ├── 📁 frontend/
│   │   └── 🌐 index.html                 (✨ Dashboard web)
│   │       - 5 abas de funcionalidade
│   │       - Design responsivo
│   │       - Local storage integration
│   │       - 500+ linhas
│   │
│   ├── 📁 integrations/              (✨ NOVO)
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 web_importer.py            (🌐 Importar web)
│   │       - Class: WebImporter
│   │       - Download + parse HTML
│   │       - Converter para Markdown
│   │       - 350+ linhas
│   │
│   └── 📁 data/
│       ├── 🐍 task_manager.py            (📋 Gerenciar tarefas)
│       │   - Class: TaskManager
│       │   - CRUD de tarefas
│       │   - Subtarefas
│       │   - Estatísticas
│       │   - 380+ linhas
│       │
│       ├── 📁 tasks/                 (Created automatically)
│       │   └── 📄 tasks.json             (Tarefas salvas)
│       │
│       ├── 📁 imported_docs/         (Created automatically)
│       │   ├── 📄 index.json             (Índice de docs)
│       │   └── 📄 *.md                   (Docs convertidos)
│       │
│       └── 📄 evolution_history.json     (Histórico agente)
│
├── 🐍 run.py                          (Iniciar tudo)
│   - Verifica dependências
│   - Inicia backend
│   - Abre frontend
│   - 70 linhas
│
├── 🐍 cli.py                          (CLI completa)
│   - 6 comandos: task, stats, timeline, knowledge, search, help
│   - Saída colorida com tabulate
│   - 480 linhas
│
├── 🐍 main.py                         (Script legado)
│
├── 📄 requirements.txt                (Dependências)
│   - openai
│   - flask + flask-cors
│   - beautifulsoup4 (✨ novo)
│   - requests
│   - tabulate
│   - python-dotenv
│
├── 📄 .env                            (Configuração)
│   - OPENAI_API_KEY
│   - OPENAI_MODEL
│   - FLASK config
│
├── 📄 .env.example                    (Template)
│
├── 📦 Dockerfile                      (Container)
│
├── 📄 QUICKSTART.md                   (Setup 5 min)
├── 📄 README_APP.md                   (Docs técnicas)
├── 📄 GUIA_USO_AGENTE.md             (Guia prático)
├── 📄 GUIA_CLI.md                     (CLI exemplos)
│
├── 📄 ESTRUTURA_COMPLETA.md           (Arquitetura)
├── 📄 EXEMPLOS_PRATICOS.md            (3 exemplos)
├── 📄 RESUMO_IMPLEMENTACAO.md         (Checklist)
│
├── 📄 IMPLEMENTACAO_FRONTEND.md       (✨ NOVO - Frontend summary)
├── 📄 PROCEDIMENTO_TAREFAS.md         (✨ NOVO - Como usar)
└── 📄 CHECKLIST_COMPLETO.md           (✨ NOVO - Progress)
```

---

## 🔄 FLUXO DE DADOS

### **Fluxo 1: Criar e Processar Tarefa**

```
User Input
    │
    ▼
┌─────────────────────┐
│  Frontend Form      │
│  (index.html)       │
│                     │
│  - Descrição        │
│  - Contexto         │
│  - Prioridade       │
│  - Categoria        │
└────────┬────────────┘
         │
         │ JSON POST
         ▼
   /api/task
         │
         ▼
┌─────────────────────┐
│  Backend API        │
│  (api.py)           │
│                     │
│  - Parse JSON       │
│  - Validação        │
│  - Chamada agente   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Agente Evolutivo   │
│  (evolutionary_     │
│   agent.py)         │
│                     │
│  1. Consulta OpenAI │
│  2. Processa        │
│  3. Aprende         │
│  4. Salva histórico │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Persistência       │
│  (evolution_        │
│   history.json)     │
│                     │
│  - Task ID          │
│  - Response         │
│  - Learning points  │
│  - Timestamp        │
└────────┬────────────┘
         │
         │ JSON Response
         ▼
   /api/task (200 OK)
         │
         ▼
┌─────────────────────┐
│  Frontend           │
│  Display Result     │
│                     │
│  - Status badge     │
│  - Resposta         │
│  - Tempo gasto      │
│  - Learning points  │
└────────┬────────────┘
         │
         ▼
   User Sees Result
```

### **Fluxo 2: Importar Página Web**

```
User Input
    │
    ▼
┌──────────────┐
│ URL + Title  │
└────┬─────────┘
     │
     │ JSON POST
     ▼
/api/import-web
     │
     ▼
┌──────────────────┐
│  WebImporter     │
│  (web_importer.py)
│                  │
│  1. Download URL │
│  2. Parse HTML   │
│  3. Extract text │
│  4. HTML→MD      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐
│  Save File       │
│  (imported_docs/)
│                  │
│  - Arquivo .md   │
│  - Index JSON    │
└────┬─────────────┘
     │
     │ JSON Response
     ▼
/api/imported-docs
     │
     ▼
┌──────────────────┐
│  Frontend        │
│  List Documents  │
│  - Title         │
│  - Date          │
│  - Size          │
│  - Download link │
└──────────────────┘
```

### **Fluxo 3: Gerenciar Tarefas**

```
Create Task
    │
    ├─ via Frontend Form
    │  └─ POST /api/task
    │
    └─ via CLI
       └─ python cli.py task "..."

TaskManager
    │
    ├─ Create
    │  └─ tasks.json
    │
    ├─ Read
    │  └─ GET /api/task
    │
    ├─ Update
    │  └─ PUT /api/task/<id>
    │
    └─ Delete
       └─ Mark as archived
```

---

## 🎯 MAPA DE FUNCIONALIDADES

```
PROMETHEUS SYSTEM
│
├── 🤖 AGENTE EVOLUTIVO
│   ├── Processa tarefas
│   ├── Aprende com OpenAI
│   ├── Mantém histórico
│   └── Exporta conhecimento
│
├── 🌐 FRONTEND DASHBOARD
│   ├── Nova Tarefa
│   │   ├── Form + envio
│   │   ├── Resposta em tempo real
│   │   └── Status visual
│   │
│   ├── Status Agente
│   │   ├── Estatísticas
│   │   ├── Versão
│   │   └── Status online/offline
│   │
│   └── Timeline
│       ├── Últimas tarefas
│       ├── Learning points
│       └── Timestamps
│
├── 🖥️ CLI INTERFACE
│   ├── task - Criar tarefa
│   ├── stats - Ver estatísticas
│   ├── timeline - Ver histórico
│   ├── knowledge - Exportar knowledge
│   ├── search - Buscar termos
│   └── help - Ajuda
│
├── 🌍 WEB IMPORTER
│   ├── Download de páginas
│   ├── Parse HTML
│   ├── Converter MD
│   ├── Persistir arquivos
│   └── Indexar documentos
│
├── 📋 TASK MANAGER
│   ├── Criar tarefas
│   ├── Prioridades
│   ├── Categorias
│   ├── Subtarefas
│   ├── Estatísticas
│   └── Export MD
│
└── 💾 PERSISTÊNCIA
    ├── evolution_history.json
    ├── tasks.json
    ├── imported_docs/
    └── index.json
```

---

## 📊 MATRIZ DE COMPONENTES

| Componente | Tipo | Linhas | Status | Função |
|-----------|------|--------|--------|--------|
| evolutionary_agent.py | Python | 440 | ✅ | IA Core |
| api.py | Python | 360 | ✅ | API REST |
| index.html | HTML/JS | 500+ | ✅ | Frontend |
| web_importer.py | Python | 350+ | ✅ | Web Scraper |
| task_manager.py | Python | 380+ | ✅ | Task CRUD |
| cli.py | Python | 480+ | ✅ | CLI |
| run.py | Python | 70 | ✅ | Bootstrap |
| requirements.txt | TXT | - | ✅ | Dependencies |
| Documentação | MD | 800+ | ✅ | Docs |
| **TOTAL** | | **~3,400+** | ✅ | **Completo** |

---

## 🔌 INTEGRAÇÃO DE COMPONENTES

```
┌────────────────────────────────────────────────────────┐
│                   FRONTEND BROWSER                      │
│         (HTML + CSS + JavaScript - 500+ lines)          │
└────────────┬─────────────────────────────────────────┬──┘
             │                                         │
      JSON via Fetch API                       LocalStorage
             │                                (API Key, Config)
             ▼
┌────────────────────────────────────────────────────────┐
│              FLASK BACKEND API (Port 5000)             │
│        (Python Flask + CORS - 360+ lines)              │
│                                                        │
│  Routes:                                               │
│  ├─ /api/task (CRUD)                                  │
│  ├─ /api/agent/stats                                  │
│  ├─ /api/agent/timeline                               │
│  ├─ /api/import-web                                   │
│  ├─ /api/imported-docs                                │
│  └─ /api/knowledge                                    │
└────────────┬──────────┬──────────┬─────────────────────┘
             │          │          │
             ▼          ▼          ▼
        ┌─────────┐ ┌──────────┐ ┌────────────┐
        │ Agente  │ │WebImporter│ │TaskManager │
        │Evolution│ │(350 lines)│ │(380 lines) │
        │(440 ln) │ │          │ │           │
        └─────────┘ └──────────┘ └────────────┘
             │          │              │
             ▼          ▼              ▼
    ┌──────────────────────────────────────────┐
    │    JSON Persistence (app/data/)          │
    │                                          │
    │  ├─ evolution_history.json               │
    │  ├─ tasks.json                           │
    │  ├─ imported_docs/*.md                   │
    │  └─ imported_docs/index.json             │
    └──────────────────────────────────────────┘
```

---

## 🚀 PIPELINE DE EXECUÇÃO

```
1. INICIALIZAÇÃO
   python run.py
   └─ Verifica .env
   └─ Inicia Flask (port 5000)
   └─ Abre browser

2. FRONTEND CARREGA
   http://localhost:5000
   └─ Carrega index.html
   └─ Inicializa JavaScript
   └─ Conecta a API

3. PRIMEIRA REQUISIÇÃO
   GET /api/agent/stats
   └─ Backend retorna dados
   └─ Frontend exibe

4. USUÁRIO CRIA TAREFA
   Form submission
   └─ POST /api/task {JSON}
   └─ Agente processa
   └─ Salva resultado
   └─ Response volta ao frontend

5. FRONTEND ATUALIZA
   Display result
   └─ Status badge
   └─ Response text
   └─ Loading stops

6. AUTO-REFRESH (30s)
   GET /api/agent/stats
   GET /api/agent/timeline
   └─ Frontend atualiza dados
```

---

**Este é o mapa completo do sistema Prometheus!** 🗺️🎉

