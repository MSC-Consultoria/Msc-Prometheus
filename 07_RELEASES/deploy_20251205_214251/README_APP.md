# 🚀 Prometheus - Agente Evolutivo com Interface

Sistema completo de agentes de IA que evoluem através de documentação estruturada.

## 📋 Estrutura

```
03_INFRAESTRUTURA/
├── app/
│   ├── agents/
│   │   └── evolutionary_agent.py      ← Agente evolutivo (core)
│   ├── backend/
│   │   └── api.py                     ← API REST Flask
│   └── frontend/
│       └── index.html                 ← Interface web moderna
├── main.py                            ← Script legado
├── run.py                             ← Iniciar sistema completo
├── requirements.txt                   ← Dependências
├── Dockerfile                         ← Containerização
└── .dockerignore
```

## 🎯 Features

### ✨ Agente Evolutivo
- Processa tarefas via LLM (OpenAI)
- Aprende com cada execução
- Mantém histórico de evolução
- Base de conhecimento persistente
- Extrai pontos de aprendizado automaticamente

### 🌐 Interface Web
- Dashboard moderno e responsivo
- Criar e monitorar tarefas em tempo real
- Estatísticas do agente
- Timeline de evolução
- Busca na base de conhecimento

### 🔗 API REST
- Endpoints para todos os recursos
- CORS habilitado para frontend
- Documentação automática
- Tratamento de erros robusto

## 🚀 Quickstart

### 1. Instalar Dependências

```bash
cd 03_INFRAESTRUTURA
pip install -r requirements.txt
```

### 2. Configurar API Key

Criar arquivo `.env`:
```env
OPENAI_API_KEY=sk-proj-xxx...
OPENAI_MODEL=gpt-4o-mini
```

### 3. Iniciar Sistema

**Opção A - Modo Completo (Com Interface):**
```bash
python run.py
```

Isso irá:
- ✅ Verificar dependências
- ✅ Iniciar API backend (porta 5000)
- ✅ Abrir dashboard no navegador

**Opção B - Apenas Backend:**
```bash
cd app/backend
python api.py
```

**Opção C - Usar Agente Diretamente:**
```bash
python
>>> from app.agents.evolutionary_agent import EvolutionaryAgent
>>> agent = EvolutionaryAgent()
>>> result = agent.process_task("Crie um exemplo em Juniper")
>>> print(result)
```

## 📚 API Endpoints

### Health Check
```bash
GET /api/health
```

### Criar Tarefa
```bash
POST /api/task
Content-Type: application/json

{
  "description": "Crie um exemplo de documentação",
  "context": "Use Markdown estruturado",
  "files": []
}
```

### Estatísticas
```bash
GET /api/agent/stats
```

### Timeline de Evolução
```bash
GET /api/agent/timeline?limit=20
```

### Base de Conhecimento
```bash
GET /api/knowledge?format=json
GET /api/knowledge?format=markdown
```

### Buscar Conhecimento
```bash
GET /api/knowledge/search?q=juniper
```

## 🎓 Como Funciona

### 1. Tarefa Entra
```
Usuário → Interface Web → API REST
```

### 2. Agente Processa
```
LLM (OpenAI) → Extrai Aprendizados → Salva em JSON
```

### 3. Evolução
```
Histórico de Tarefas → Machine Learning → Base de Conhecimento
```

### 4. Próximas Execuções
```
Agente usa aprendizados anteriores → Melhora continuamente
```

## 📊 Dados Persistidos

### Evolution History (`data/evolution_history.json`)
```json
{
  "version": "1.0.0",
  "total_evolutions": 42,
  "history": [
    {
      "timestamp": "2025-12-05T10:30:00",
      "task_id": "task_1733406600",
      "task_description": "Crie um exemplo...",
      "success": true,
      "learning_points": ["documentation", "integration"],
      "version": "1.0.0"
    }
  ],
  "knowledge_base": {
    "task_1": "conteúdo aprendido...",
    "task_2": "outro aprendizado..."
  }
}
```

## 🔧 Customização

### Trocar Modelo LLM
Editar em `evolutionary_agent.py`:
```python
agent = EvolutionaryAgent(model="gpt-4")  # Use gpt-4 para tarefas complexas
```

### Sistema Prompt Customizado
Modificar `_build_system_prompt()` em `evolutionary_agent.py`

### Porta da API
Editar em `api.py`:
```python
app.run(host='0.0.0.0', port=8000)  # Mudar porta
```

## 🐳 Docker

### Build
```bash
docker build -t prometheus .
```

### Run
```bash
docker run -p 5000:5000 \
  -e OPENAI_API_KEY=sk-proj-xxx \
  prometheus
```

## 📈 Métricas

Monitorar no dashboard:
- **Total de Tarefas:** Quantas foram processadas
- **Taxa de Sucesso:** % de execuções bem-sucedidas
- **Entradas de Conhecimento:** Quantos aprendizados foram salvos
- **Áreas de Aprendizado:** Tópicos em que o agente se especializou

## 🔒 Segurança

- ✅ API Key em variáveis de ambiente
- ✅ CORS habilitado apenas para localhost (customizar se necessário)
- ✅ Validação de entrada em todos os endpoints
- ✅ Histórico criptografável (implementar se necessário)

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"
```bash
# Criar .env na pasta 03_INFRAESTRUTURA
echo OPENAI_API_KEY=sk-proj-xxx > .env
```

### Erro: "Port 5000 já em uso"
```bash
# Usar outra porta
# Editar api.py: app.run(port=8000)
```

### Frontend não conecta na API
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health

# Verificar CORS em api.py
CORS(app)  # Deve estar habilitado
```

## 📝 Próximas Features

- [ ] Autenticação de usuários
- [ ] Persistência em banco de dados (não apenas JSON)
- [ ] WebSocket para tempo real
- [ ] Suporte para múltiplos LLMs (Gemini, Cohere, etc)
- [ ] Export de relatórios
- [ ] Integração GitHub para versionamento
- [ ] CLI unificada
- [ ] Notebooks Jupyter integrados

## 📞 Suporte

Consulte:
- `../01_DOCUMENTACAO_CONSOLIDADA/CONSOLIDADO_ESTRATEGICO.md` - Arquitetura
- `../01_DOCUMENTACAO_CONSOLIDADA/STATUS_PROJETO.md` - Progresso
- `../02_DOCUMENTACAO_REFERENCIA/` - Conceitos e guias

---

**Versão:** 1.0.0  
**Data:** 05-12-2025  
**Status:** ✅ Pronto para usar
