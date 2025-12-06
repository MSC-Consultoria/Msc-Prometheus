# 🔌 Guia de Integrações do Prometheus

## Integrações Implementadas

Este documento descreve as integrações adicionadas ao sistema Prometheus para conectar o agente com serviços externos.

---

## 1. GitHub Copilot Integration 🐙

### Funcionalidades
- ✅ Monitoramento de rate limits da API do GitHub
- ✅ Informações sobre o usuário autenticado
- ✅ Status da conexão com GitHub
- ⏳ Uso do Copilot (requer Copilot Business/Enterprise)

### Configuração

**1. Obter GitHub Personal Access Token:**
- Acesse: https://github.com/settings/tokens
- Clique em "Generate new token" → "Generate new token (classic)"
- Selecione os escopos:
  - `repo` (Full control of private repositories)
  - `read:user` (Read user profile data)
  - `read:org` (Read org and team membership)
- Copie o token gerado

**2. Configure no `.env`:**
```env
GITHUB_TOKEN=ghp_seu_token_aqui
```

### Uso via API

**Obter rate limits:**
```bash
GET /api/github/rate-limits
```

**Verificar status:**
```bash
GET /api/github/status
```

**Informações do usuário:**
```bash
GET /api/github/user
```

### Uso no Dashboard
1. Navegue até **Configurações**
2. Veja a seção **GitHub Integration**
3. Se configurado, mostra:
   - Usuário autenticado
   - Plano do GitHub
   - Rate limits disponíveis (com barra de progresso)

---

## 2. N8N Workflow Automation 🔄

### Funcionalidades
- ✅ Enviar resultados de tarefas para workflows N8N
- ✅ Receber webhooks do N8N para processar tarefas
- ✅ Enviar notificações via N8N (Slack, Email, Discord, etc.)
- ✅ Validação de assinatura de webhooks (segurança)
- ✅ Agendamento de tarefas através do N8N

### Configuração

**1. Instalar N8N:**
```bash
npm install -g n8n
```

**2. Iniciar N8N:**
```bash
n8n start
```

**3. Criar Workflow no N8N:**
- Acesse http://localhost:5678
- Crie um novo workflow
- Adicione um nó "Webhook"
- Configure o webhook com método POST
- Copie a URL do webhook

**4. Configure no `.env`:**
```env
N8N_WEBHOOK_URL=http://localhost:5678/webhook
N8N_API_KEY=seu-api-key-aqui
N8N_WEBHOOK_SECRET=secret-opcional-para-validacao
```

### Workflows Sugeridos

#### Workflow 1: Notificar Task Concluída
```
Webhook (task-completed)
  → Filter (status === "success")
  → Slack Node (send message)
  → Email Node (send report)
```

#### Workflow 2: Agendar Tarefas
```
Schedule Trigger (cron: 0 9 * * *)
  → HTTP Request (POST /api/n8n/webhook)
  → Body: { "task": "Gerar relatório diário" }
```

#### Workflow 3: Processar Google Docs
```
Google Docs Trigger (on document update)
  → Extract Text
  → HTTP Request (POST /api/n8n/webhook)
  → Body: { "task": "Analisar documento", "context": "{{text}}" }
```

### Uso via API

**Receber webhook do N8N:**
```bash
POST /api/n8n/webhook
Content-Type: application/json

{
  "task": "Descrição da tarefa",
  "context": "Contexto opcional",
  "workflow_id": "meu-workflow"
}
```

**Triggar workflow no N8N:**
```bash
POST /api/n8n/trigger
Content-Type: application/json

{
  "workflow_id": "task-completed",
  "data": {
    "task_id": "task_123",
    "result": "Tarefa concluída"
  },
  "wait": false
}
```

**Enviar notificação:**
```bash
POST /api/n8n/notify
Content-Type: application/json

{
  "message": "Nova tarefa completada!",
  "channel": "slack",
  "level": "success"
}
```

### Uso no Dashboard
1. Navegue até **Agente IA**
2. Marque a checkbox "📬 Notificar resultado via N8N"
3. Envie a tarefa
4. O resultado será automaticamente enviado para o workflow N8N configurado

---

## 3. Multi-Provider LLM Support 🤖

### Provedores Suportados
- ✅ **OpenAI** (GPT-4, GPT-4o, GPT-4o-mini)
- ✅ **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus)
- ✅ **Google** (Gemini Pro, Gemini Pro Vision)
- ✅ **DeepSeek** (DeepSeek Chat, DeepSeek Coder)
- ✅ **OpenRouter** (Acesso a múltiplos modelos)

### Configuração

**Configure as API keys no `.env`:**
```env
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AI...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
```

### Uso via API

**Trocar provedor:**
```bash
POST /api/agent/provider
Content-Type: application/json

{
  "provider": "anthropic",
  "model": "claude-3-5-sonnet-20241022"
}
```

### Uso no Dashboard
1. Navegue até **Agente IA**
2. Na seção **Configuração do Modelo**:
   - Selecione o **Provedor LLM** desejado
   - Escolha o **Modelo**
   - Clique em **🔄 Atualizar Provedor**
3. Envie tarefas usando o novo provedor

### Comparação de Custos (por 1M tokens)

| Provedor | Modelo | Input | Output |
|----------|--------|-------|--------|
| OpenAI | GPT-4o Mini | $0.15 | $0.60 |
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4 | $30.00 | $60.00 |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |
| Google | Gemini Pro | $0.50 | $1.50 |
| DeepSeek | DeepSeek Chat | $0.14 | $0.28 |

---

## 4. Segurança 🔐

### Proteção de API Keys
- ✅ Todas as keys armazenadas em `.env` (não versionado)
- ✅ Keys nunca expostas no frontend
- ✅ Validação de assinaturas de webhooks N8N

### Validação de Webhooks
O N8N pode assinar webhooks com HMAC-SHA256:

```python
# No N8N, adicione header:
X-N8N-Signature: <hmac_sha256_signature>

# Prometheus valida automaticamente se N8N_WEBHOOK_SECRET configurado
```

### Boas Práticas
1. **Nunca comite** o arquivo `.env`
2. **Use secrets** ao fazer deploy em produção
3. **Rotacione keys** periodicamente
4. **Limite permissões** dos tokens ao mínimo necessário
5. **Monitore rate limits** para evitar bloqueios

---

## 5. Troubleshooting 🔧

### GitHub: "401 Unauthorized"
- ✅ Verifique se o token está correto no `.env`
- ✅ Verifique se o token não expirou
- ✅ Verifique se os escopos necessários foram concedidos

### N8N: "Connection Error"
- ✅ Verifique se N8N está rodando (`n8n start`)
- ✅ Verifique a URL do webhook no `.env`
- ✅ Teste o webhook manualmente com curl/Postman

### LLM: "Client não configurado"
- ✅ Verifique se a API key está no `.env`
- ✅ Verifique se instalou as dependências:
  - `pip install anthropic` (para Claude)
  - `pip install google-generativeai` (para Gemini)
- ✅ Reinicie o servidor Flask

### Rate Limits Excedidos
- ✅ Aguarde o reset (informação disponível no dashboard)
- ✅ Use outro provedor temporariamente
- ✅ Considere upgradar seu plano

---

## 6. Exemplos de Uso 💡

### Exemplo 1: Task Automática Agendada via N8N
```javascript
// N8N Workflow
Schedule → HTTP Request (POST /api/n8n/webhook)

Body:
{
  "task": "Analisar logs do sistema e gerar relatório",
  "context": "Verificar erros nas últimas 24h"
}
```

### Exemplo 2: Notificação no Slack Após Task
```python
# Prometheus envia resultado para N8N
# N8N workflow: Webhook → Slack Node

# Configuração:
notify_n8n = True  # No frontend ou API
```

### Exemplo 3: Trocar Modelo Baseado em Complexidade
```javascript
// Frontend JavaScript
if (taskComplexity === 'high') {
  await changeProvider('openai', 'gpt-4');
} else {
  await changeProvider('openai', 'gpt-4o-mini');
}
```

---

## 7. Próximos Passos 🚀

### Integrações Futuras
- [ ] **MCP Protocol** - Integração com Model Context Protocol
- [ ] **HuggingFace Spaces** - Deploy do dashboard como Space
- [ ] **Google Workspace** - Integração com Drive, Docs, Sheets
- [ ] **Manus AI** - Integração com sistema Manus
- [ ] **Discord/Slack Bots** - Interação via bots

### Melhorias Planejadas
- [ ] Dashboard de métricas de uso por provedor
- [ ] Sistema de fallback automático entre provedores
- [ ] Cache de respostas para reduzir custos
- [ ] Filas de tarefas com priorização
- [ ] Logs estruturados e observabilidade

---

## 8. Suporte 📞

Para dúvidas ou problemas:
1. Verifique este guia primeiro
2. Consulte a documentação oficial:
   - [GitHub API](https://docs.github.com/en/rest)
   - [N8N Docs](https://docs.n8n.io/)
   - [OpenAI API](https://platform.openai.com/docs)
   - [Anthropic API](https://docs.anthropic.com/)
3. Verifique os logs do servidor Flask
4. Abra uma issue no repositório

---

**Última atualização:** Dezembro 2025  
**Versão:** 1.0.0
