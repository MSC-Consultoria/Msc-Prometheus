# 🚀 ROADMAP - Próximos Passos do Prometheus

**Data:** 05-12-2025  
**Status:** Sistema base completo ✅ | CLI implementada ✅ | Dashboard web ✅

---

## 📊 VISÃO GERAL

### ✅ JÁ PRONTO
- [x] Agente Evolutivo (core inteligência)
- [x] API REST (7 endpoints)
- [x] Dashboard Web (interface moderna)
- [x] CLI (6 comandos)
- [x] Persistência JSON
- [x] Documentação completa

### 🔄 PRÓXIMAS PRIORIDADES
1. **Banco de Dados** (escalabilidade)
2. **Google Workspace** (integração externa)
3. **Autenticação** (multi-usuário)
4. **WebSocket** (atualizações reais)
5. **Multi-LLM** (múltiplos modelos)

---

## 📅 PLANO DETALHADO (Por Semana)

### **SEMANA 1: Banco de Dados (48h)**
**Objetivo:** Substituir JSON por SQLite/PostgreSQL

**Tarefas:**
- [ ] Criar schema do banco (evolution_history, tasks, knowledge_base, users)
- [ ] Implementar ORM (SQLAlchemy)
- [ ] Migrar dados de JSON → DB
- [ ] Atualizar `evolutionary_agent.py` para usar DB
- [ ] Testes de performance (JSON vs DB)
- [ ] Documentação de schema

**Benefícios:**
- ✨ Escalabilidade para milhões de tasks
- 🔒 Transações ACID
- 📊 Queries complexas
- 🔍 Índices para buscas rápidas

**Arquivo a criar:**
```
03_INFRAESTRUTURA/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py       ← Nova ORM
│   │   ├── connection.py   ← Configuração DB
│   │   └── migrations/
│   └── ...
```

---

### **SEMANA 2: Google Workspace (40h)**
**Objetivo:** Integrar com Google Drive, Docs, Sheets

**Tarefas:**
- [ ] Setup Google Cloud Console (OAuth 2.0)
- [ ] Criar `integrations/google_workspace.py`
- [ ] Implementar leitura de Google Docs
- [ ] Implementar escrita em Google Docs
- [ ] Sincronizar tarefas com Google Drive
- [ ] Criar endpoint `/api/google/auth`
- [ ] Testes de integração

**Features:**
```python
# Ler documento
agent.read_google_doc(doc_id)

# Escrever resultado
agent.write_google_doc(doc_id, content)

# Sincronizar pasta
agent.sync_google_drive(folder_id)
```

**Arquivo a criar:**
```
03_INFRAESTRUTURA/
├── app/
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── google_workspace.py  ← Nova integração
│   │   └── credentials.json     ← OAuth
```

---

### **SEMANA 3: Autenticação Multi-Usuário (40h)**
**Objetivo:** Sistema de login com JWT + roles

**Tarefas:**
- [ ] Criar modelo `User` no banco
- [ ] Implementar JWT tokens
- [ ] Criar endpoints de autenticação
- [ ] Proteger endpoints com decoradores
- [ ] Sistema de permissões (Admin, User, Viewer)
- [ ] Atualizar dashboard para login
- [ ] Testes de segurança

**Endpoints novos:**
```
POST /api/auth/register        → Criar usuário
POST /api/auth/login           → Fazer login
POST /api/auth/refresh         → Renovar token
GET  /api/auth/me              → Info do usuário
POST /api/auth/logout          → Logout
```

**Arquivo a criar:**
```
03_INFRAESTRUTURA/
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── models.py          ← User model
│   │   ├── utils.py           ← JWT, hashing
│   │   └── decorators.py      ← @require_auth
```

---

### **SEMANA 4: WebSocket + Atualizações Reais (36h)**
**Objetivo:** Substituir polling por WebSocket

**Tarefas:**
- [ ] Integrar `python-socketio` na API
- [ ] Criar eventos de WebSocket
- [ ] Atualizar dashboard para usar WebSocket
- [ ] Broadcast de atualizações em tempo real
- [ ] Notificações para usuários
- [ ] Fallback para polling (navegadores antigos)
- [ ] Testes de conexão

**Events:**
```
task:start         → Tarefa iniciou
task:progress      → Progresso (%)
task:complete      → Tarefa finalizada
knowledge:updated  → Conhecimento atualizado
stats:changed      → Estatísticas mudaram
```

**Arquivo a criar:**
```
03_INFRAESTRUTURA/
├── app/
│   ├── websocket/
│   │   ├── __init__.py
│   │   ├── events.py          ← Event handlers
│   │   └── namespace.py       ← Socket namespaces
```

---

### **SEMANA 5: Multi-LLM Support (32h)**
**Objetivo:** Suportar GPT, Gemini, Claude, LLaMA

**Tarefas:**
- [ ] Criar interface abstrata para LLM
- [ ] Implementar providers: OpenAI, Gemini, Claude, Ollama
- [ ] Sistema de fallback (se falhar, tenta outro)
- [ ] Seleção automática por tipo de tarefa
- [ ] Comparação de custos/performance
- [ ] Dashboard de LLMs
- [ ] Testes com cada modelo

**Código:**
```python
from app.llm import LLMFactory

# Usar modelo automático
response = agent.process_task("tarefa", model="auto")

# Ou específico
response = agent.process_task("tarefa", model="claude-3")

# Fallback automático
agent.enable_fallback(primary="gpt-4", secondary="gemini")
```

**Arquivo a criar:**
```
03_INFRAESTRUTURA/
├── app/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py            ← Interface base
│   │   ├── openai_provider.py
│   │   ├── gemini_provider.py
│   │   ├── claude_provider.py
│   │   ├── ollama_provider.py
│   │   └── factory.py         ← LLMFactory
```

---

## 🎯 QUICK WINS (Pequenas Melhorias - Baixa Prioridade)

**Para fazer rapidinho (1-2h cada):**
- [ ] Adicionar dark mode ao dashboard
- [ ] Criar favicon customizado
- [ ] Adicionar spinner no CLI
- [ ] Melhorar mensagens de erro
- [ ] Adicionar logging detalhado
- [ ] Criar arquivo `CHANGELOG.md`
- [ ] Adicionar suporte a `.gitignore`
- [ ] Criar `docker-compose.yml` com DB

---

## 🏗️ ARQUITETURA EVOLUTION

### ATUAL (MVP)
```
┌─────────────┐     ┌──────────┐     ┌──────────┐
│  Dashboard  │────▶│ Flask    │────▶│ EvAgent  │
│    HTML     │     │ API      │     │ + JSON   │
└─────────────┘     └──────────┘     └──────────┘
```

### SEMANA 1 (Com DB)
```
┌─────────────┐     ┌──────────┐     ┌──────────────┐
│  Dashboard  │────▶│ Flask    │────▶│ EvAgent      │
│    HTML     │     │ API      │     │ + SQLAlchemy │
└─────────────┘     └──────────┘     └──────┬───────┘
                                             │
                                    ┌────────▼────────┐
                                    │  PostgreSQL     │
                                    │  (ou SQLite)    │
                                    └─────────────────┘
```

### SEMANA 2 (Com Google)
```
                    ┌─────────────────────┐
                    │  Google Workspace   │
                    │  (Docs, Drive,      │
                    │   Sheets)           │
                    └──────────┬──────────┘
                               │
┌─────────────┐     ┌──────────▼──┐     ┌──────────────┐
│  Dashboard  │────▶│ Flask       │────▶│ EvAgent      │
│    HTML     │     │ API         │     │ + GoogleAPI  │
└─────────────┘     └──────────┬──┘     └──────┬───────┘
    ▲                           │               │
    └───────────────────────────┴───────────────┘
              WebSocket + REST
```

### SEMANA 3 (Com Auth)
```
    ┌─────────────────────────────────────────────┐
    │  Auth Layer (JWT + Roles)                   │
    └──────────────┬────────────────────────────┬─┘
                   │                            │
        ┌──────────▼─────────┐    ┌───────────▼────┐
        │  User: Admin       │    │  User: Regular │
        │  Todas permissões  │    │  Tarefas own   │
        └────────────────────┘    └────────────────┘
```

---

## 📈 MÉTRICAS DE SUCESSO

Após cada semana, validar:

```
✅ Testes passando (>85% coverage)
✅ Performance mantida (< 500ms por request)
✅ Documentação atualizada
✅ Zero erros em produção
✅ Feedback do usuário positivo
```

---

## 💰 ESTIMATIVA DE ESFORÇO

| Semana | Tarefa | Horas | Complexidade |
|--------|--------|-------|--------------|
| 1 | Banco de Dados | 48h | 🟡 Média |
| 2 | Google Workspace | 40h | 🟡 Média |
| 3 | Autenticação | 40h | 🟡 Média |
| 4 | WebSocket | 36h | 🟡 Média |
| 5 | Multi-LLM | 32h | 🟡 Média |
| **Total** | **5 Semanas** | **196h** | **~1 mês** |

---

## 🚀 COMO COMEÇAR

### Hoje (Semana 1 - Banco de Dados)

**1. Escolher banco:**
```bash
# Opção A: SQLite (simples, local)
pip install sqlalchemy

# Opção B: PostgreSQL (robusto, recomendado)
pip install psycopg2-binary sqlalchemy
```

**2. Criar estrutura:**
```bash
mkdir -p app/database
touch app/database/__init__.py
touch app/database/models.py
touch app/database/connection.py
```

**3. Implementar modelo base:**
```python
# app/database/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    task_id = Column(String, unique=True)
    description = Column(String)
    status = Column(String)
    timestamp = Column(DateTime)
```

**4. Testar conexão:**
```bash
python -c "from app.database.connection import db; print('✓ DB OK')"
```

---

## 📚 RECURSOS

- [SQLAlchemy Docs](https://docs.sqlalchemy.org)
- [Google API Docs](https://developers.google.com/workspace)
- [JWT Guide](https://jwt.io)
- [Socket.IO Docs](https://python-socketio.readthedocs.io)

---

## 🎯 RECOMENDAÇÃO FINAL

**Comece agora com Banco de Dados!**

Motivo:
1. ✅ Prepara para escala
2. ✅ Base para autenticação multi-usuário
3. ✅ Necessário para Google Workspace
4. ✅ Melhora performance
5. ✅ Implementação clara e testável

**Tempo estimado:** 2-3 dias de desenvolvimento

Quer que eu comece? 🚀

