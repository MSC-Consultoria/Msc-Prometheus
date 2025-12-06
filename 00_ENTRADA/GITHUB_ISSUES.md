# 🐛 GitHub Issues - Prometheus Project

**Total Issues:** 10  
**Geradas:** Dezembro 5, 2025  
**Método:** Análise automatizada do projeto

---

## Issue #1: 🔴 [CRÍTICO] Inicializar Git Repository e Conectar com GitHub

**Labels:** `critical`, `infrastructure`, `setup`  
**Prioridade:** 🔴 P0 - URGENTE  
**Estimativa:** 2-4 horas  
**Assignee:** @user

### 📝 Descrição

O projeto Prometheus atualmente **não possui controle de versão**. Todo o código está em um diretório local sem histórico de commits, branches ou backup remoto. Isso representa um risco crítico de perda de trabalho.

### 🎯 Objetivo

Inicializar Git repository local, criar repository no GitHub, e estabelecer conexão segura para versionamento e colaboração.

### 🔧 Tarefas

- [ ] **1.1** Inicializar Git no diretório raiz
  ```bash
  cd c:\Users\Festeja\Downloads\Prometheus
  git init
  ```

- [ ] **1.2** Criar `.gitignore` apropriado
  ```gitignore
  # Python
  __pycache__/
  *.py[cod]
  *$py.class
  *.so
  .Python
  env/
  venv/
  ENV/
  .venv
  
  # Environment
  .env
  .env.local
  *.env
  
  # IDEs
  .vscode/
  .idea/
  *.swp
  *.swo
  
  # OS
  .DS_Store
  Thumbs.db
  
  # Project specific
  03_INFRAESTRUTURA/app/data/*.json
  05_ARQUIVO_HISTORICO/
  06_BACKUPS/
  *.log
  ```

- [ ] **1.3** Criar GitHub repository
  - Nome: `prometheus-ai-agent`
  - Descrição: "Sistema de Agentes Evolutivos com Múltiplas Integrações LLM"
  - Visibilidade: Private (recomendado) ou Public
  - Inicializar com README: No (já temos local)

- [ ] **1.4** Configurar GitHub Personal Access Token
  - Gerar token em: https://github.com/settings/tokens
  - Scopes necessários: `repo`, `workflow`, `write:packages`
  - Salvar token em local seguro

- [ ] **1.5** Conectar repository local ao GitHub
  ```bash
  git remote add origin https://github.com/seu-usuario/prometheus-ai-agent.git
  git branch -M main
  ```

- [ ] **1.6** Criar branches principais
  ```bash
  git checkout -b develop
  git checkout -b staging
  git checkout main
  ```

- [ ] **1.7** Primeiro commit
  ```bash
  git add .
  git commit -m "Initial commit: Prometheus AI Agent System

  - Backend Flask API with 20+ endpoints
  - Frontend dashboard with 7 sections
  - Multi-LLM support (OpenAI, Claude, Gemini, DeepSeek, OpenRouter)
  - GitHub and N8N integrations
  - Comprehensive documentation"
  
  git push -u origin main
  ```

- [ ] **1.8** Configurar branch protection rules
  - Proteger `main` branch
  - Require pull request reviews
  - Require status checks to pass

### ✅ Critérios de Aceitação

1. Repository Git inicializado localmente
2. Repository criado no GitHub
3. Código pushed para GitHub com sucesso
4. Branches `main`, `develop`, `staging` criadas
5. `.gitignore` funcionando (arquivos sensíveis não commitados)
6. Branch protection configurado

### 📚 Documentação de Referência

- [GitHub: Create a repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [Git: Getting Started](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [GitHub: Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches)

### ⚠️ Avisos

- **IMPORTANTE:** Não commitar arquivo `.env` com API keys!
- Verificar `.gitignore` antes do primeiro commit
- Considerar usar GitHub CLI (`gh`) para automação

### 🔗 Issues Relacionados

- Issue #2 (CI/CD depende deste)
- Issue #5 (Deploy depende deste)

---

## Issue #2: 🔴 [CRÍTICO] Implementar Testes Automatizados (Coverage >30%)

**Labels:** `critical`, `testing`, `quality`  
**Prioridade:** 🔴 P0 - URGENTE  
**Estimativa:** 20-30 horas  
**Assignee:** @user

### 📝 Descrição

O projeto atualmente possui **0% de cobertura de testes**. Isso significa que qualquer refatoração ou nova feature pode quebrar funcionalidades existentes sem detecção automática.

### 🎯 Objetivo

Implementar suite de testes automatizados com cobertura mínima de 30% para componentes críticos do sistema.

### 🔧 Tarefas

- [ ] **2.1** Configurar ambiente de testes
  ```bash
  pip install pytest pytest-cov pytest-asyncio pytest-mock
  ```

- [ ] **2.2** Criar estrutura de testes
  ```
  03_INFRAESTRUTURA/tests/
  ├── __init__.py
  ├── conftest.py
  ├── unit/
  │   ├── test_evolutionary_agent.py
  │   ├── test_api_clients.py
  │   ├── test_github_copilot.py
  │   └── test_n8n_client.py
  ├── integration/
  │   ├── test_api_endpoints.py
  │   └── test_llm_providers.py
  └── fixtures/
      ├── sample_tasks.json
      └── mock_responses.json
  ```

- [ ] **2.3** Implementar testes unitários para `EvolutionaryAgent`
  ```python
  # test_evolutionary_agent.py
  def test_agent_initialization():
      agent = EvolutionaryAgent()
      assert agent.version == "1.0.0"
      assert len(agent.evolution_history) >= 0
  
  def test_process_task():
      agent = EvolutionaryAgent()
      result = agent.process_task("Test task")
      assert "task_id" in result
      assert "response" in result
      assert "status" in result
  
  def test_change_provider():
      agent = EvolutionaryAgent()
      result = agent.change_provider("anthropic", "claude-3-5-sonnet-20241022")
      assert result["provider"] == "anthropic"
  ```

- [ ] **2.4** Implementar testes para GitHub integration
  ```python
  def test_github_rate_limits(mock_requests):
      client = GitHubCopilotClient()
      result = client.get_rate_limits()
      assert "rate" in result
      assert result["status"] == "success"
  ```

- [ ] **2.5** Implementar testes para N8N integration
  ```python
  def test_n8n_trigger_workflow(mock_requests):
      client = N8NClient()
      result = client.trigger_workflow("test-workflow", {"data": "test"})
      assert result["status"] == "success"
  ```

- [ ] **2.6** Implementar testes de API endpoints
  ```python
  def test_api_task_endpoint(client):
      response = client.post('/api/task', json={
          "description": "Test task"
      })
      assert response.status_code == 200
      assert "task_id" in response.json
  ```

- [ ] **2.7** Configurar pytest.ini
  ```ini
  [pytest]
  testpaths = tests
  python_files = test_*.py
  python_classes = Test*
  python_functions = test_*
  addopts = 
      --verbose
      --cov=app
      --cov-report=html
      --cov-report=term-missing
      --cov-fail-under=30
  ```

- [ ] **2.8** Adicionar comando de teste ao README
  ```bash
  # Run all tests
  pytest
  
  # Run with coverage
  pytest --cov=app --cov-report=html
  
  # Run specific test file
  pytest tests/unit/test_evolutionary_agent.py
  ```

- [ ] **2.9** Integrar com CI/CD (após Issue #1)

### ✅ Critérios de Aceitação

1. Suite de testes executando sem erros
2. Coverage mínimo de 30% alcançado
3. Testes para componentes críticos:
   - EvolutionaryAgent
   - API endpoints principais
   - GitHub integration
   - N8N integration
4. HTML coverage report gerado
5. Documentação de como rodar testes

### 📚 Documentação de Referência

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/3.0.x/testing/)

### 🎯 Metas de Coverage por Módulo

| Módulo | Target | Prioridade |
|--------|--------|-----------|
| `evolutionary_agent.py` | 60% | Alta |
| `api.py` | 40% | Alta |
| `github_copilot.py` | 50% | Média |
| `n8n_client.py` | 50% | Média |
| `api_clients.py` | 30% | Baixa |

### 🔗 Issues Relacionados

- Issue #1 (Git setup primeiro)
- Issue #7 (CI/CD executará testes)

---

## Issue #3: 🟠 [ALTA] Implementar MCP (Model Context Protocol) Server

**Labels:** `feature`, `integration`, `high-priority`  
**Prioridade:** 🟠 P1 - Alta (Mencionado em Tarefas03.MD)  
**Estimativa:** 30-40 horas  
**Assignee:** @user

### 📝 Descrição

O usuário especificamente solicitou "Criar integrações com MCP" nas tarefas. MCP (Model Context Protocol) é um protocolo que permite que AI assistants (como Claude Desktop, VS Code Copilot) acessem ferramentas e recursos externos.

### 🎯 Objetivo

Implementar MCP server completo que exponha as capacidades do Prometheus para outros clientes MCP-compatible.

### 🔧 Tarefas

**Fase 1: Research e Setup**

- [ ] **3.1** Pesquisar MCP Protocol specification
  - Documentação oficial Anthropic
  - Exemplos de implementação
  - SDKs disponíveis

- [ ] **3.2** Escolher SDK/biblioteca
  - Python MCP SDK oficial (se disponível)
  - Ou implementação custom do protocol

- [ ] **3.3** Instalar dependências
  ```bash
  pip install mcp  # ou biblioteca equivalente
  ```

**Fase 2: Implementação do Server**

- [ ] **3.4** Criar estrutura MCP
  ```
  03_INFRAESTRUTURA/app/mcp/
  ├── __init__.py
  ├── server.py          # MCP server implementation
  ├── resources.py       # Recursos expostos (tasks, knowledge, etc.)
  ├── tools.py           # Tools disponíveis para clients
  ├── prompts.py         # System prompts
  └── config.py          # MCP configuration
  ```

- [ ] **3.5** Implementar MCP Server básico
  ```python
  # server.py
  from mcp import Server, Resource, Tool
  
  class PrometheusServer(Server):
      def __init__(self):
          super().__init__("prometheus")
          self.register_resources()
          self.register_tools()
      
      def register_resources(self):
          # Expõe recursos do Prometheus
          pass
      
      def register_tools(self):
          # Expõe ferramentas do Prometheus
          pass
  ```

- [ ] **3.6** Definir Resources (dados acessíveis)
  ```python
  # resources.py
  - prometheus://tasks - Lista de tarefas
  - prometheus://knowledge - Knowledge base
  - prometheus://evolution-history - Histórico de evoluções
  - prometheus://providers - Provedores LLM disponíveis
  ```

- [ ] **3.7** Definir Tools (ações executáveis)
  ```python
  # tools.py
  - process_task(description, context) - Processar tarefa com agente
  - search_knowledge(query) - Buscar na knowledge base
  - trigger_n8n_workflow(workflow_id, data) - Triggar workflow N8N
  - get_github_rate_limits() - Obter rate limits do GitHub
  - change_llm_provider(provider, model) - Trocar provedor
  ```

- [ ] **3.8** Implementar authentication/authorization

- [ ] **3.9** Adicionar logging e error handling

**Fase 3: Integração**

- [ ] **3.10** Integrar MCP server com main.py
  ```python
  # run.py
  from app.mcp.server import PrometheusServer
  
  mcp_server = PrometheusServer()
  mcp_server.start(port=5001)
  ```

- [ ] **3.11** Configurar .env
  ```env
  MCP_SERVER_PORT=5001
  MCP_SERVER_HOST=localhost
  MCP_AUTH_TOKEN=secure-token-here
  ```

**Fase 4: Testes**

- [ ] **3.12** Testar com Claude Desktop
  - Configurar Claude para conectar ao MCP server
  - Testar tools e resources
  - Validar funcionamento

- [ ] **3.13** Testar com VS Code (se possível)

- [ ] **3.14** Criar testes automatizados para MCP

**Fase 5: Documentação**

- [ ] **3.15** Criar `GUIA_MCP.md`
  - Como configurar MCP server
  - Como conectar clients
  - Exemplos de uso
  - API reference

- [ ] **3.16** Atualizar README com informações do MCP

### ✅ Critérios de Aceitação

1. MCP server rodando em porta configurável
2. Mínimo 3 resources expostos
3. Mínimo 5 tools implementados
4. Claude Desktop consegue conectar e usar
5. Autenticação funcionando
6. Documentação completa
7. Testes básicos implementados

### 📚 Documentação de Referência

- [Model Context Protocol - Anthropic](https://www.anthropic.com/news/model-context-protocol)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Examples](https://github.com/anthropics/mcp-examples)

### 💡 Use Cases

1. **Claude Desktop:** Usar Prometheus como ferramenta no Claude
2. **VS Code Copilot:** Acessar knowledge base do Prometheus
3. **Cursor IDE:** Integrar com Prometheus agent
4. **Outros Clients MCP:** Interoperabilidade

### 🔗 Issues Relacionados

- Issue #6 (Agente Evolutivo pode usar MCP)

---

## Issue #4: 🟠 [ALTA] Implementar Autenticação JWT e Rate Limiting

**Labels:** `security`, `feature`, `high-priority`  
**Prioridade:** 🟠 P1 - Alta  
**Estimativa:** 10-15 horas  
**Assignee:** @user

### 📝 Descrição

Atualmente a API Flask está **completamente aberta** - qualquer pessoa com acesso ao endpoint pode fazer requisições ilimitadas. Isso representa riscos de:
- Uso não autorizado
- Custos descontrolados com LLMs
- Abuso e DoS

### 🎯 Objetivo

Implementar sistema de autenticação JWT e rate limiting por usuário/IP para proteger a API.

### 🔧 Tarefas

**Fase 1: Autenticação JWT**

- [ ] **4.1** Instalar dependências
  ```bash
  pip install flask-jwt-extended flask-limiter
  ```

- [ ] **4.2** Configurar JWT
  ```python
  # app/backend/auth.py
  from flask_jwt_extended import JWTManager, create_access_token
  
  jwt = JWTManager(app)
  app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
  ```

- [ ] **4.3** Criar endpoints de autenticação
  ```python
  @app.route('/api/auth/login', methods=['POST'])
  def login():
      # username/password ou API key
      pass
  
  @app.route('/api/auth/register', methods=['POST'])
  def register():
      # criar novo usuário
      pass
  
  @app.route('/api/auth/refresh', methods=['POST'])
  def refresh():
      # refresh token
      pass
  ```

- [ ] **4.4** Proteger endpoints existentes
  ```python
  from flask_jwt_extended import jwt_required, get_jwt_identity
  
  @app.route('/api/task', methods=['POST'])
  @jwt_required()
  def create_task():
      current_user = get_jwt_identity()
      # ...
  ```

- [ ] **4.5** Criar sistema de API keys
  ```python
  # Alternative to JWT for programmatic access
  @app.route('/api/keys/generate', methods=['POST'])
  @jwt_required()
  def generate_api_key():
      # Gerar API key para usuário
      pass
  ```

**Fase 2: Rate Limiting**

- [ ] **4.6** Configurar Flask-Limiter
  ```python
  from flask_limiter import Limiter
  from flask_limiter.util import get_remote_address
  
  limiter = Limiter(
      app=app,
      key_func=get_remote_address,
      default_limits=["200 per day", "50 per hour"]
  )
  ```

- [ ] **4.7** Aplicar rate limits por endpoint
  ```python
  @app.route('/api/task', methods=['POST'])
  @jwt_required()
  @limiter.limit("10 per minute")
  def create_task():
      # LLM calls são caros, limitar uso
      pass
  
  @app.route('/api/github/rate-limits', methods=['GET'])
  @limiter.limit("30 per minute")
  def github_rate_limits():
      pass
  ```

- [ ] **4.8** Implementar rate limits por usuário
  ```python
  def get_user_id():
      return get_jwt_identity()
  
  limiter = Limiter(
      app=app,
      key_func=get_user_id
  )
  ```

**Fase 3: Database de Usuários**

- [ ] **4.9** Configurar SQLite (ou PostgreSQL)
  ```bash
  pip install flask-sqlalchemy
  ```

- [ ] **4.10** Criar model de User
  ```python
  from flask_sqlalchemy import SQLAlchemy
  
  class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      username = db.Column(db.String(80), unique=True)
      email = db.Column(db.String(120), unique=True)
      password_hash = db.Column(db.String(128))
      api_key = db.Column(db.String(64), unique=True)
      rate_limit_override = db.Column(db.Integer, default=None)
      created_at = db.Column(db.DateTime, default=datetime.utcnow)
  ```

- [ ] **4.11** Implementar password hashing
  ```bash
  pip install bcrypt
  ```

**Fase 4: Frontend Integration**

- [ ] **4.12** Adicionar login page ao dashboard
  ```html
  <!-- login.html -->
  <form id="login-form">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
  </form>
  ```

- [ ] **4.13** Armazenar JWT no localStorage
  ```javascript
  async function login(username, password) {
      const response = await fetch('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify({username, password})
      });
      const data = await response.json();
      localStorage.setItem('jwt_token', data.access_token);
  }
  ```

- [ ] **4.14** Adicionar JWT em todas as requests
  ```javascript
  const API_BASE = 'http://localhost:5000/api';
  const token = localStorage.getItem('jwt_token');
  
  fetch(`${API_BASE}/task`, {
      method: 'POST',
      headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
  });
  ```

### ✅ Critérios de Aceitação

1. Endpoints protegidos com JWT
2. Login/register funcionando
3. Rate limiting ativo
4. API keys geráveis
5. Frontend com tela de login
6. Usuários armazenados em database
7. Password hashing implementado
8. Documentação atualizada

### 📚 Documentação de Referência

- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Limiter](https://flask-limiter.readthedocs.io/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

### 🔗 Issues Relacionados

- Issue #5 (Deploy requer autenticação)

---

## Issue #5: 🟡 [MÉDIA] Configurar CI/CD Pipeline com GitHub Actions

**Labels:** `infrastructure`, `automation`, `devops`  
**Prioridade:** 🟡 P2 - Média  
**Estimativa:** 8-12 horas  
**Assignee:** @user

### 📝 Descrição

Automatizar processo de teste, build e deploy usando GitHub Actions.

### 🔧 Tarefas

- [ ] **5.1** Criar workflow de testes
  ```yaml
  # .github/workflows/test.yml
  name: Run Tests
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - uses: actions/setup-python@v4
          with:
            python-version: '3.11'
        - run: pip install -r requirements.txt
        - run: pytest --cov
  ```

- [ ] **5.2** Criar workflow de linting
  ```yaml
  # .github/workflows/lint.yml
  - run: pip install flake8 black
  - run: flake8 app/
  - run: black --check app/
  ```

- [ ] **5.3** Criar workflow de deploy
  ```yaml
  # .github/workflows/deploy.yml
  name: Deploy to Production
  on:
    push:
      branches: [main]
  ```

- [ ] **5.4** Configurar secrets no GitHub
  - `OPENAI_API_KEY`
  - `OPENROUTER_API_KEY`
  - `GITHUB_TOKEN`
  - `JWT_SECRET_KEY`

- [ ] **5.5** Adicionar status badges ao README

### ✅ Critérios de Aceitação

1. CI/CD pipeline funcionando
2. Testes rodando automaticamente
3. Deploy automático para staging
4. Badges no README

### 🔗 Issues Relacionados

- Issue #1 (Requer Git/GitHub)
- Issue #2 (Requer testes)

---

## Issue #6: 🟡 [MÉDIA] Melhorar Agente para Ser Verdadeiramente Evolutivo

**Labels:** `enhancement`, `ai`, `core-feature`  
**Prioridade:** 🟡 P2 - Média  
**Estimativa:** 25-35 horas  
**Assignee:** @user

### 📝 Descrição

O "Agente Evolutivo" atualmente apenas salva histórico mas não aprende de verdade. Implementar funcionalidades que tornem o agente verdadeiramente evolutivo.

### 🔧 Tarefas

- [ ] **6.1** Implementar Vector Database
  ```bash
  pip install chromadb  # ou pinecone, weaviate
  ```

- [ ] **6.2** Gerar embeddings para knowledge base
  ```python
  from openai import OpenAI
  
  def generate_embedding(text):
      response = client.embeddings.create(
          model="text-embedding-3-small",
          input=text
      )
      return response.data[0].embedding
  ```

- [ ] **6.3** Implementar RAG (Retrieval-Augmented Generation)
  ```python
  def retrieve_relevant_knowledge(query):
      query_embedding = generate_embedding(query)
      results = vector_db.search(query_embedding, top_k=5)
      return results
  ```

- [ ] **6.4** Adicionar memory layer (short-term + long-term)

- [ ] **6.5** Implementar feedback loop (usuário avalia respostas)

- [ ] **6.6** Treinar fine-tuning periódico (opcional)

### ✅ Critérios de Aceitação

1. Vector database funcionando
2. RAG implementado
3. Agente usa contexto de tarefas anteriores
4. Melhoria mensurável em respostas

---

## Issue #7: 🟡 [MÉDIA] Deploy para Staging e Produção

**Labels:** `infrastructure`, `deployment`, `devops`  
**Prioridade:** 🟡 P2 - Média  
**Estimativa:** 15-20 horas  
**Assignee:** @user

### 📝 Descrição

Deploy do sistema em ambiente de staging e produção para acesso externo.

### 🔧 Tarefas

**Staging:**
- [ ] **7.1** Configurar Railway/Render/Fly.io para staging
- [ ] **7.2** Configurar variáveis de ambiente
- [ ] **7.3** Deploy automático via GitHub Actions
- [ ] **7.4** Configurar domínio (staging.prometheus.com)

**Produção:**
- [ ] **7.5** Configurar servidor production (AWS/GCP/Azure)
- [ ] **7.6** Configurar HTTPS com Let's Encrypt
- [ ] **7.7** Configurar load balancer
- [ ] **7.8** Configurar monitoring (Sentry/DataDog)

### ✅ Critérios de Aceitação

1. Staging environment acessível
2. Production environment acessível
3. HTTPS funcionando
4. Monitoring ativo

---

## Issue #8: 🟡 [MÉDIA] Adicionar API Documentation (Swagger/OpenAPI)

**Labels:** `documentation`, `api`  
**Prioridade:** 🟡 P2 - Média  
**Estimativa:** 6-8 horas  
**Assignee:** @user

### 📝 Descrição

Gerar documentação interativa da API usando Swagger/OpenAPI.

### 🔧 Tarefas

- [ ] **8.1** Instalar Flask-RESTX ou flasgger
  ```bash
  pip install flask-restx
  ```

- [ ] **8.2** Adicionar decorators aos endpoints
  ```python
  @api.doc(
      description='Process task with AI agent',
      responses={200: 'Success', 400: 'Bad Request'}
  )
  @api.expect(task_model)
  def create_task():
      pass
  ```

- [ ] **8.3** Configurar Swagger UI em `/docs`

- [ ] **8.4** Adicionar exemplos de request/response

### ✅ Critérios de Aceitação

1. Swagger UI acessível em `/docs`
2. Todos endpoints documentados
3. Try-it-out funcionando

---

## Issue #9: 🔵 [BAIXA] Otimizar Performance do Frontend

**Labels:** `enhancement`, `frontend`, `performance`  
**Prioridade:** 🔵 P3 - Baixa  
**Estimativa:** 10-15 horas  
**Assignee:** @user

### 📝 Descrição

Melhorar performance do dashboard com lazy loading, caching e otimizações.

### 🔧 Tarefas

- [ ] **9.1** Implementar lazy loading de seções
- [ ] **9.2** Adicionar service worker para cache
- [ ] **9.3** Minificar JS/CSS
- [ ] **9.4** Implementar PWA
- [ ] **9.5** Otimizar imagens (se houver)
- [ ] **9.6** Adicionar loading skeletons

### ✅ Critérios de Aceitação

1. Lighthouse score >90
2. First Contentful Paint <2s
3. PWA installable
4. Funciona offline (básico)

---

## Issue #10: 🔵 [BAIXA] Adicionar Monitoring e Observabilidade

**Labels:** `infrastructure`, `monitoring`, `observability`  
**Prioridade:** 🔵 P3 - Baixa  
**Estimativa:** 10-15 horas  
**Assignee:** @user

### 📝 Descrição

Implementar sistema de monitoring para detectar problemas em produção.

### 🔧 Tarefas

- [ ] **10.1** Configurar Sentry para error tracking
  ```bash
  pip install sentry-sdk[flask]
  ```

- [ ] **10.2** Adicionar logs estruturados (JSON)
  ```bash
  pip install python-json-logger
  ```

- [ ] **10.3** Implementar health checks
  ```python
  @app.route('/health')
  def health():
      return {'status': 'ok', 'timestamp': datetime.now()}
  ```

- [ ] **10.4** Configurar métricas (Prometheus + Grafana)

- [ ] **10.5** Configurar alertas

### ✅ Critérios de Aceitação

1. Sentry capturando erros
2. Logs estruturados em JSON
3. Health checks funcionando
4. Dashboard de métricas (Grafana)
5. Alertas configurados (email/Slack)

---

## 📊 Priorização dos Issues

```
URGENTE (P0) - Fazer AGORA:
├─ Issue #1: Git/GitHub Setup (2-4h)
└─ Issue #2: Testes Básicos (20-30h)

ALTA (P1) - Próximas 2 semanas:
├─ Issue #3: MCP Protocol (30-40h) ← Requisito do usuário!
└─ Issue #4: Autenticação (10-15h)

MÉDIA (P2) - Próximo mês:
├─ Issue #5: CI/CD (8-12h)
├─ Issue #6: Agente Evolutivo (25-35h)
├─ Issue #7: Deploy (15-20h)
└─ Issue #8: API Docs (6-8h)

BAIXA (P3) - Quando possível:
├─ Issue #9: Frontend Performance (10-15h)
└─ Issue #10: Monitoring (10-15h)
```

### Total Esforço Estimado
- **URGENTE:** 22-34 horas
- **ALTA:** 40-55 horas
- **MÉDIA:** 54-75 horas
- **BAIXA:** 20-30 horas
- **TOTAL:** 136-194 horas (3.4 - 4.8 semanas full-time)

---

## 🎯 Roadmap Sugerido

### Sprint 1 (Semana 1)
- Issue #1: Git/GitHub Setup
- Issue #2: Testes Básicos (início)

### Sprint 2 (Semana 2)
- Issue #2: Testes Básicos (conclusão)
- Issue #4: Autenticação (início)

### Sprint 3 (Semana 3)
- Issue #4: Autenticação (conclusão)
- Issue #3: MCP Protocol (início)

### Sprint 4 (Semana 4)
- Issue #3: MCP Protocol (conclusão)
- Issue #5: CI/CD

---

**Gerado por:** AI Agent (GitHub Copilot Pro)  
**Data:** Dezembro 5, 2025  
**Método:** Análise automatizada do código-fonte e estrutura do projeto
