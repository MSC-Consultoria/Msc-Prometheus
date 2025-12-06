# 🖥️ Prometheus CLI - Guia de Uso

## Instalação

Certifique-se de ter as dependências instaladas:

```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-proj-seu-token-aqui
OPENAI_MODEL=gpt-4o-mini
```

2. Substitua `sk-proj-seu-token-aqui` pela sua chave da OpenAI

## Comandos Disponíveis

### 1. **Processar Tarefa**

Enviar uma tarefa para o agente processar:

```bash
python cli.py task "Sua descrição aqui"
```

Com contexto:

```bash
python cli.py task "Crie um exemplo" --context "Use Python e Markdown"
```

**Saída:**
```
============================================================
  🚀 PROCESSANDO TAREFA
============================================================

Tarefa:
  Crie um exemplo

Contexto:
  Use Python e Markdown

Processando...
✓ Tarefa processada com sucesso!

📋 RESPOSTA:
[Resposta do agente...]

📚 Pontos de Aprendizado:
  • python
  • markdown
  • example

⏱️  Tempo: 2.45s
📊 Evolução #1
```

---

### 2. **Ver Estatísticas**

Visualizar métricas do agente:

```bash
python cli.py stats
```

**Saída:**
```
============================================================
  📊 ESTATÍSTICAS DO AGENTE
============================================================

╒════════════════════════╤═════════╕
│ Métrica                │ Valor   │
╞════════════════════════╪═════════╡
│ Versão do Agente       │ 1.0.0   │
│ Total de Tarefas       │ 5       │
│ Taxa de Sucesso        │ 100.0%  │
│ Entradas de Conhecimento│ 12      │
│ Tempo de Execução      │ 15.23s  │
╘════════════════════════╧═════════╛
```

---

### 3. **Timeline de Evolução**

Ver histórico de tarefas processadas:

```bash
python cli.py timeline
```

Com limite customizado:

```bash
python cli.py timeline --limit 20
```

**Saída:**
```
============================================================
  📈 TIMELINE DE EVOLUÇÃO (Últimos 10)
============================================================

╒═╤═════════════════════════╤════════════════════════╤════════════╕
│ │ Timestamp               │ Tarefa                 │ Status     │
╞═╪═════════════════════════╪════════════════════════╪════════════╡
│ 1│ 2025-12-05 14:32:15     │ Crie um exemplo        │ success    │
│ 2│ 2025-12-05 14:30:00     │ Analise o código       │ success    │
│ 3│ 2025-12-05 14:28:45     │ Integre com Google     │ success    │
╘═╧═════════════════════════╧════════════════════════╧════════════╛
```

---

### 4. **Exportar Conhecimento**

Exportar a base de conhecimento aprendida:

```bash
python cli.py knowledge
```

Em formato Markdown:

```bash
python cli.py knowledge --format markdown
```

**Saída (JSON):**
```json
{
  "version": "1.0.0",
  "total_tasks": 5,
  "learning_base": [
    "python",
    "markdown",
    "api",
    "frontend",
    "integration"
  ],
  "tasks": [
    {
      "id": "task_1733406600",
      "task_description": "Crie um exemplo",
      "status": "success",
      "timestamp": "2025-12-05 14:32:15"
    }
  ]
}
```

---

### 5. **Buscar Conhecimento**

Procurar por termos na base de conhecimento:

```bash
python cli.py search "python"
```

**Saída:**
```
============================================================
  🔍 BUSCANDO: 'python'
============================================================

✓ Encontrado 3 resultado(s):

  [Learning Point]
  python

  [Tarefa]
  Crie um exemplo de Python

  [Tarefa]
  Analise código Python
```

---

### 6. **Ajuda**

Mostrar todos os comandos disponíveis:

```bash
python cli.py help
```

---

## 📝 Exemplos Práticos

### Exemplo 1: Criar documentação

```bash
python cli.py task "Crie um guia de instalação" --context "Para Windows e Linux"
```

### Exemplo 2: Análise de código

```bash
python cli.py task "Revise este código Python para melhorias"
```

### Exemplo 3: Fluxo completo

```bash
# 1. Processar tarefa
python cli.py task "Analise arquitetura de microsserviços"

# 2. Ver o que aprendemos
python cli.py stats

# 3. Ver histórico
python cli.py timeline --limit 5

# 4. Buscar por termos específicos
python cli.py search "microsserviços"

# 5. Exportar todo conhecimento
python cli.py knowledge --format markdown > knowledge.md
```

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError"

Instale as dependências:

```bash
pip install -r requirements.txt
```

### Erro: "OpenAI API Key not found"

Verifique se o arquivo `.env` existe e contém:

```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

### Erro: "Connection refused"

O arquivo `evolution_history.json` será criado automaticamente na primeira execução. Se houver erro de permissão, garanta que você tem permissão de escrita no diretório.

---

## 🚀 Próximos Passos

- Integrar com **banco de dados** para melhor escalabilidade
- Adicionar suporte a **múltiplos modelos LLM**
- Criar interface **web avançada** com WebSocket
- Implementar **autenticação** de usuários
- Adicionar **plugins customizados**

---

## 📞 Suporte

Para mais informações, consulte:
- `README_APP.md` - Documentação técnica completa
- `GUIA_USO_AGENTE.md` - Guia de uso do agente
- `QUICKSTART.md` - Setup rápido

