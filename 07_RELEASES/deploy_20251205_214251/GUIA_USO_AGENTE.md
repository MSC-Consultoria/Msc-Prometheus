# 🎓 Guia de Uso - Prometheus Agente Evolutivo

## 🚀 Primeiros Passos

### Passo 1: Setup Inicial

```bash
# 1. Navegar para pasta
cd 03_INFRAESTRUTURA

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Criar arquivo .env
cp .env.example .env
# Editar .env e adicionar sua OPENAI_API_KEY
```

### Passo 2: Iniciar Sistema

```bash
# Opção 1: Modo Completo (Recomendado)
python run.py

# Opção 2: Apenas Backend
cd app/backend
python api.py
```

**Resultado esperado:**
```
====================================================
🚀 PROMETHEUS - Agente Evolutivo
====================================================
✅ Dependências encontradas
✅ Backend iniciado (PID: 12345)
   API disponível em: http://localhost:5000
✅ Frontend aberto em: ...

====================================================
✨ Prometheus está rodando!
====================================================

📊 Dashboard: http://localhost:5000
🔗 API Docs: http://localhost:5000/docs
```

---

## 💻 Usando via Interface Web

### Interface Dashboard

Quando você executa `python run.py`, o navegador abre automaticamente:

```
http://file:///.../app/frontend/index.html
```

### Fluxo de Uso

1. **Nova Tarefa**
   - Escrever descrição (obrigatório)
   - Adicionar contexto (opcional)
   - Clicar "Enviar para Agente"

2. **Resposta**
   - Agente processa via LLM
   - Extrai aprendizados
   - Salva histórico

3. **Monitorar**
   - Ver estatísticas em tempo real
   - Consultar timeline de evolução
   - Pesquisar na base de conhecimento

### Exemplo de Tarefa

```
Descrição:
"Crie um exemplo de documentação no formato Juniper que combine Python e Markdown"

Contexto (opcional):
"Use boas práticas de engenharia de software, com type hints"
```

**Resposta Esperada:**
```markdown
# Exemplo Juniper

## Conceito
...

## Código Python
```python
...
```

## Documentação Markdown
...
```

---

## 🔌 Usando via API REST

### 1. Health Check

```bash
curl http://localhost:5000/api/health
```

**Resposta:**
```json
{
  "status": "online",
  "version": "1.0.0",
  "timestamp": "2025-12-05T10:30:00"
}
```

### 2. Criar Tarefa

```bash
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Crie um exemplo de Juniper",
    "context": "Use Python e Markdown"
  }'
```

**Resposta:**
```json
{
  "task_id": "task_1733406600",
  "status": "success",
  "response": "# Exemplo Juniper\n...",
  "learning_points": ["documentation", "integration"],
  "elapsed_time": 3.45,
  "timestamp": "2025-12-05T10:31:00",
  "evolution_count": 1
}
```

### 3. Ver Estatísticas

```bash
curl http://localhost:5000/api/agent/stats
```

**Resposta:**
```json
{
  "version": "1.0.0",
  "created_at": "2025-12-05T10:00:00",
  "total_tasks": 5,
  "successful": 5,
  "failed": 0,
  "success_rate": "100%",
  "knowledge_entries": 5,
  "learning_areas": ["documentation", "integration", "optimization"]
}
```

### 4. Timeline de Evolução

```bash
curl http://localhost:5000/api/agent/timeline?limit=10
```

**Resposta:**
```json
{
  "timeline": [
    {
      "timestamp": "2025-12-05T10:31:00",
      "task_id": "task_1733406600",
      "task": "Crie um exemplo de Juniper",
      "success": true,
      "learnings": ["documentation"]
    }
  ]
}
```

### 5. Base de Conhecimento

```bash
# JSON
curl http://localhost:5000/api/knowledge?format=json

# Markdown
curl http://localhost:5000/api/knowledge?format=markdown
```

### 6. Buscar Conhecimento

```bash
curl "http://localhost:5000/api/knowledge/search?q=juniper"
```

**Resposta:**
```json
{
  "query": "juniper",
  "results_count": 2,
  "results": [
    {
      "task_id": "task_1733406600",
      "excerpt": "# Exemplo Juniper\n..."
    }
  ]
}
```

---

## 🐍 Usando Diretamente em Python

### Importar Agente

```python
from app.agents.evolutionary_agent import EvolutionaryAgent

# Inicializar
agent = EvolutionaryAgent()

# Processar tarefa
result = agent.process_task(
    task_description="Crie um exemplo",
    context="Use Markdown estruturado"
)

print(result)
# Resultado:
# {
#   'task_id': 'task_1733406600',
#   'status': 'success',
#   'response': '...',
#   'learning_points': ['documentation'],
#   'elapsed_time': 3.45,
#   ...
# }
```

### Ver Estatísticas

```python
stats = agent.get_stats()
print(stats)
# {
#   'version': '1.0.0',
#   'total_tasks': 1,
#   'successful': 1,
#   'failed': 0,
#   'success_rate': '100%',
#   ...
# }
```

### Ver Timeline

```python
timeline = agent.get_evolution_timeline(limit=5)
for item in timeline:
    print(f"{item['timestamp']} - {item['task']}")
```

### Exportar Conhecimento

```python
# Como JSON
json_kb = agent.export_knowledge(format='json')

# Como Markdown
md_kb = agent.export_knowledge(format='markdown')
with open('knowledge.md', 'w') as f:
    f.write(md_kb)
```

---

## 📊 Monitorando Progresso

### Via Dashboard
- Abrir http://localhost:5000
- Ver stats em tempo real
- Consultar timeline visualmente

### Via Arquivo
```bash
# Windows
type %USERPROFILE%\...\app\data\evolution_history.json

# Linux/Mac
cat ~/.../app/data/evolution_history.json
```

### Via API
```bash
curl http://localhost:5000/api/agent/stats | python -m json.tool
```

---

## 🎯 Casos de Uso

### 1. Documentação Estruturada
```
Tarefa: "Crie documentação para um novo módulo Python em formato Juniper"
Contexto: "Módulo de autenticação com tipo hints e docstrings"
```

### 2. Conversão de Código
```
Tarefa: "Converta este script bash para Python compatível com Windows/Linux"
Contexto: "[cole o script bash]"
```

### 3. Melhorias de Infra
```
Tarefa: "Sugira melhorias para este Dockerfile"
Contexto: "[cole o Dockerfile]"
```

### 4. Explicação de Conceitos
```
Tarefa: "Explique o padrão Juniper (Markdown + Python) com exemplos"
Contexto: "Inclua casos de uso reais"
```

---

## 🔍 Troubleshooting

### "Connection refused" na API
```bash
# Verificar se está rodando
curl http://localhost:5000/api/health

# Se falhar, iniciar:
cd app/backend
python api.py
```

### "OPENAI_API_KEY not found"
```bash
# Criar .env
echo OPENAI_API_KEY=sk-proj-xxx > .env

# Ou exportar
export OPENAI_API_KEY=sk-proj-xxx
```

### "Frontend não conecta"
```bash
# Verificar CORS em api.py está habilitado
CORS(app)

# Verificar porta
curl http://localhost:5000/docs
```

### Resposta vazia
```bash
# Verificar limite de tokens
# Editar em .env:
MAX_TOKENS=2000

# Ou em evolutionary_agent.py:
max_tokens=2000
```

---

## 📈 Dicas de Performance

### Reduzir Custos
```env
# Use gpt-4o-mini ao invés de gpt-4
OPENAI_MODEL=gpt-4o-mini
MAX_TOKENS=1000  # Reduzir tokens
TEMPERATURE=0.5  # Menos criativo = menos tokens
```

### Acelerar Resposta
```python
# Usar cache quando possível
result = agent.process_task(task)  # Primeira call é lenta
result = agent.process_task(task)  # Próximas são rápidas
```

### Gerenciar Histórico
```python
# Histórico fica em data/evolution_history.json
# Últimas 100 tarefas são mantidas
# Remover arquivo para resetar
```

---

## 🚀 Próximos Passos

1. **Enviar várias tarefas** para agente aprender
2. **Consultar base de conhecimento** para ver aprendizados
3. **Integrar com Google Drive** (ver GUIA_INTEGRACAO_GOOGLE.md)
4. **Criar notebooks Jupyter** com agente
5. **Configurar automação** semanal

---

## 📞 Mais Informações

- **Arquitetura:** `../01_DOCUMENTACAO_CONSOLIDADA/CONSOLIDADO_ESTRATEGICO.md`
- **Status & Roadmap:** `../01_DOCUMENTACAO_CONSOLIDADA/STATUS_PROJETO.md`
- **Conceitos Avançados:** `../02_DOCUMENTACAO_REFERENCIA/Agente Markdown/`

---

**Pronto para começar?** Execute: `python run.py` 🚀
