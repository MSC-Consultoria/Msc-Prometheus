# 🎨 Prometheus Dashboard - Novas Funcionalidades Implementadas

## 📍 Localização do Dashboard
**URL:** http://localhost:5000/dashboard.html

---

## ✨ Seção 1: AGENTE IA - Nova Interface com Multi-Provider

### 🔧 Configuração do Modelo (NOVO!)

```
┌─────────────────────────────────────────────────────────────────┐
│ ⚙️ Configuração do Modelo                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Provedor LLM ▼]    [Modelo ▼]           [🔄 Atualizar]       │
│   OpenAI (GPT)       GPT-4o Mini (Rápido)                       │
│   Anthropic          GPT-4o (Balanceado)                        │
│   Google Gemini      GPT-4 (Poderoso)                           │
│   DeepSeek                                                       │
│   OpenRouter                                                     │
│                                                                  │
│  Status: [✅ Provedor atualizado com sucesso!]                  │
└─────────────────────────────────────────────────────────────────┘
```

**Como Usar:**
1. Selecione o provedor desejado no dropdown
2. Escolha o modelo específico
3. Clique em "🔄 Atualizar Provedor"
4. Aguarde confirmação verde

**Provedores Disponíveis:**
- **OpenAI:** GPT-4o-mini (rápido/barato), GPT-4o (balanceado), GPT-4 (poderoso)
- **Anthropic:** Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Sonnet
- **Gemini:** Gemini Pro, Gemini Pro Vision
- **DeepSeek:** DeepSeek Chat, DeepSeek Coder (muito barato!)
- **OpenRouter:** Acesso a múltiplos modelos via uma API

---

### 🤖 Enviar Tarefa para o Agente

```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 Enviar Tarefa para o Agente                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Descrição da Tarefa *                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Escreva um poema sobre inteligência artificial...        │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  Contexto Adicional (opcional)                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Estilo: Shakespeare                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ☐ 📬 Notificar resultado via N8N (se configurado)             │
│                                                                  │
│  [🚀 Enviar para Agente]                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Nova Funcionalidade: Checkbox N8N**
- Quando marcada, o resultado é automaticamente enviado para seu workflow N8N
- Útil para enviar notificações no Slack, Email, Discord, etc.
- Aparece na resposta: "📬 Resultado enviado para N8N (Execution: xxx)"

---

## ✨ Seção 2: CONFIGURAÇÕES - Integrações Expandidas

### 🤖 Provedores de LLM

```
┌──────────────────────┬─────────────────────────────────────────┐
│ OpenAI               │ Configurado ✅                          │
│                      │ Variável: OPENAI_API_KEY               │
├──────────────────────┼─────────────────────────────────────────┤
│ Anthropic Claude     │ Não configurado ❌                      │
│                      │ Variável: ANTHROPIC_API_KEY            │
├──────────────────────┼─────────────────────────────────────────┤
│ Google Gemini        │ Não configurado ❌                      │
│                      │ Variável: GEMINI_API_KEY               │
├──────────────────────┼─────────────────────────────────────────┤
│ DeepSeek             │ Não configurado ❌                      │
│                      │ Variável: DEEPSEEK_API_KEY             │
├──────────────────────┼─────────────────────────────────────────┤
│ OpenRouter           │ Não configurado ❌                      │
│                      │ Variável: OPENROUTER_API_KEY           │
└──────────────────────┴─────────────────────────────────────────┘
```

---

### 🐙 GitHub Integration (NOVO!)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🐙 GitHub Integration                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [✅ Conectado ao GitHub]                                        │
│                                                                  │
│  👤 Usuário: seu-usuario                                         │
│  📦 Plano: Free / Pro / Enterprise                              │
│                                                                  │
│  📊 Rate Limits (API Core):                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 4999 / 5000 requisições disponíveis (99%)                │  │
│  │ ████████████████████████████████████████████░  99%       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Ou, se não configurado:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🐙 GitHub Integration                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [⚠️ GITHUB_TOKEN não configurado]                              │
│                                                                  │
│  Configure GITHUB_TOKEN no arquivo .env para habilitar          │
│  monitoramento de rate limits.                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Como Configurar:**
1. Obtenha token em: https://github.com/settings/tokens
2. Adicione ao `.env`: `GITHUB_TOKEN=ghp_seu_token_aqui`
3. Reinicie o servidor
4. Recarregue a página de Configurações

---

### 🔄 N8N Workflow Automation (NOVO!)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔄 N8N Workflow Automation                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [✅ Conectado ao N8N]                                           │
│                                                                  │
│  🔗 Webhook URL: http://localhost:5678/webhook                  │
│  🔑 API Key: Configurada ✅                                     │
│  🔐 Webhook Secret: Configurado ✅                              │
│                                                                  │
│  💡 Funcionalidades Disponíveis:                                │
│  • Enviar resultados de tarefas para workflows N8N             │
│  • Receber webhooks do N8N para processamento                  │
│  • Notificações via Slack, Email, Discord, etc.                │
│  • Agendamento de tarefas através do N8N                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Ou, se não configurado:**

```
┌─────────────────────────────────────────────────────────────────┐
│ 🔄 N8N Workflow Automation                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [⚠️ N8N_WEBHOOK_URL não configurado]                           │
│                                                                  │
│  Configure N8N_WEBHOOK_URL e N8N_API_KEY no arquivo .env       │
│  para habilitar automação.                                      │
│                                                                  │
│  📚 Como Configurar:                                            │
│  1. Instale o N8N: npm install -g n8n                          │
│  2. Inicie o N8N: n8n start                                    │
│  3. Crie workflows com webhooks no N8N                         │
│  4. Configure as URLs dos webhooks no .env                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Fluxo de Uso Completo

### Cenário 1: Usar Claude em vez de GPT

```
1. Vá para: Agente IA
2. Em "Configuração do Modelo":
   - Selecione "Anthropic (Claude)"
   - Escolha "Claude 3.5 Sonnet (Mais Recente)"
   - Clique "🔄 Atualizar Provedor"
3. Aguarde: "✅ Provedor atualizado"
4. Envie sua tarefa normalmente
5. O agente agora usa Claude em vez de GPT!
```

### Cenário 2: Notificação Automática no Slack via N8N

```
PRÉ-REQUISITO: N8N configurado com workflow "task-completed"

1. No N8N, crie workflow:
   Webhook → Filter (status=success) → Slack Node

2. No Prometheus Dashboard:
   - Vá para: Agente IA
   - Escreva sua tarefa
   - Marque: ☑️ "Notificar resultado via N8N"
   - Clique: "🚀 Enviar para Agente"

3. Resultado:
   - Tarefa processada normalmente
   - Resultado aparece no dashboard
   - Slack recebe notificação automaticamente!
   - Dashboard mostra: "📬 Resultado enviado para N8N"
```

### Cenário 3: Monitorar Rate Limits do GitHub

```
1. Configure GITHUB_TOKEN no .env
2. Vá para: Configurações
3. Veja seção "GitHub Integration"
4. Observe:
   - Quantas requisições restam
   - Barra de progresso visual
   - Quando o limite reseta
5. Use para planejar uso da API
```

### Cenário 4: Economizar com DeepSeek

```
DeepSeek é 50x mais barato que GPT-4!

1. Configure DEEPSEEK_API_KEY no .env
2. Vá para: Agente IA → Configuração
3. Selecione: "DeepSeek" → "DeepSeek Chat"
4. Clique: "🔄 Atualizar Provedor"
5. Use para tarefas simples e economize muito! 💰

Comparação de custos (1M tokens output):
- GPT-4: $60.00
- Claude 3.5: $15.00
- GPT-4o Mini: $0.60
- DeepSeek: $0.28 ← MAIS BARATO!
```

---

## 🔗 Novos Endpoints da API

Você também pode usar programaticamente:

```bash
# Trocar provedor
curl -X POST http://localhost:5000/api/agent/provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"}'

# Ver rate limits do GitHub
curl http://localhost:5000/api/github/rate-limits

# Status do N8N
curl http://localhost:5000/api/n8n/status

# Triggar workflow N8N
curl -X POST http://localhost:5000/api/n8n/trigger \
  -H "Content-Type: application/json" \
  -d '{"workflow_id": "meu-workflow", "data": {"teste": true}}'
```

---

## 🎨 Elementos Visuais Novos

### Cores e Indicadores

```
✅ Verde      - Configurado / Sucesso
❌ Vermelho   - Não configurado / Erro
⚠️ Amarelo    - Aviso / Atenção
🔄 Azul       - Ação / Atualizar
📬 Roxo       - Notificação N8N
```

### Barra de Progresso (Rate Limits)

```
Alta disponibilidade (>80%):  ████████████████████ Verde
Média (20-80%):               ████████░░░░░░░░░░░░ Amarelo
Baixa (<20%):                 ███░░░░░░░░░░░░░░░░░ Vermelho
```

---

## 📋 Checklist de Teste

Teste tudo no dashboard:

### ✅ Teste 1: Multi-Provider
- [ ] Abra "Agente IA"
- [ ] Veja seção "Configuração do Modelo"
- [ ] Troque de OpenAI para outro provedor
- [ ] Veja mensagem de sucesso verde
- [ ] Envie uma tarefa de teste
- [ ] Confirme que resposta vem do novo provedor

### ✅ Teste 2: GitHub Integration
- [ ] Abra "Configurações"
- [ ] Veja seção "GitHub Integration"
- [ ] Se configurado: veja rate limits
- [ ] Se não: veja instruções de configuração
- [ ] Observe barra de progresso (se configurado)

### ✅ Teste 3: N8N Integration
- [ ] Abra "Configurações"
- [ ] Veja seção "N8N Workflow Automation"
- [ ] Se configurado: veja funcionalidades disponíveis
- [ ] Se não: veja instruções de instalação
- [ ] Vá para "Agente IA"
- [ ] Veja checkbox "Notificar via N8N"
- [ ] Teste enviar tarefa com checkbox marcada

### ✅ Teste 4: Responsividade
- [ ] Redimensione a janela
- [ ] Confirme que layout se adapta
- [ ] Teste em diferentes resoluções

---

## 🚀 Onde Ver Cada Feature

| Feature | Tab | Localização |
|---------|-----|-------------|
| **Seletor de Provedor** | Agente IA | Topo da página, card "Configuração do Modelo" |
| **Checkbox N8N** | Agente IA | Formulário, antes do botão enviar |
| **Rate Limits GitHub** | Configurações | Segunda seção, "GitHub Integration" |
| **Status N8N** | Configurações | Terceira seção, "N8N Workflow Automation" |
| **Lista de Provedores LLM** | Configurações | Primeira seção, "Provedores de LLM" |

---

## 💡 Dicas de Uso

1. **Economize Custos:** Use GPT-4o-mini ou DeepSeek para tarefas simples
2. **Máxima Qualidade:** Use GPT-4 ou Claude 3.5 Sonnet para tarefas complexas
3. **Automação:** Configure N8N para notificações automáticas
4. **Monitore API:** Veja rate limits do GitHub para evitar bloqueios
5. **Teste Múltiplos Modelos:** Compare respostas de diferentes provedores

---

**Dashboard URL:** http://localhost:5000/dashboard.html  
**Status:** ✅ Todas as features implementadas e funcionais!
