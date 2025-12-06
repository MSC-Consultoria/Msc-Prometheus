# 🤖 COMO INTEGRAR TAREFAS AO AGENTE EVOLUTIVO

**Documento de Procedimento**

---

## 📋 VISÃO GERAL

O agente evolutivo agora pode ler tarefas do `Tarefas.MD` (seu arquivo de tarefas) e:

1. **Processar** as tarefas automaticamente
2. **Consolidar** documentos e remover repetição
3. **Sugerir** atualizações na base de conhecimento
4. **Mover** arquivos consolidados para pasta histórica
5. **Melhorar** processos em atualização

---

## 🔄 FLUXO INTEGRADO

```
┌─────────────────────────────────────────────────────┐
│         Você cria tarefa no Tarefas.MD              │
│  (ou via Frontend nas próximas semanas)             │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│    Agente lê Tarefas.MD automaticamente             │
│    (cron job ou manual via CLI)                     │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│  Agente processa cada tarefa:                       │
│  1. Entende o que fazer                             │
│  2. Consulta documentação relevante                 │
│  3. Executa ação (consolidar, mover, etc)           │
│  4. Aprende pontos-chave                            │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│  Agente atualiza:                                   │
│  ✅ Documentação consolidada                         │
│  ✅ Base de conhecimento                             │
│  ✅ Tarefas como "Completa"                          │
│  ✅ Histórico em evolution_history.json              │
└──────────────────┬──────────────────────────────────┘
                   ▼
┌─────────────────────────────────────────────────────┐
│  Você vê resultados:                                │
│  📄 Documentos consolidados                          │
│  📁 Arquivos movidos                                 │
│  🎓 Conhecimento atualizado                         │
│  ✨ Sugestões de melhorias                          │
└─────────────────────────────────────────────────────┘
```

---

## 📝 FORMATO DE TAREFA

No seu `Tarefas.MD`, use este formato:

```markdown
## 🎯 Tarefa: Consolidar documentação

**Tipo:** consolidacao
**Prioridade:** alta
**Status:** pendente

**Descrição:**
Consolidar todos os arquivos de documentação em um único arquivo.
Remover informações repetidas.

**Ações Esperadas:**
1. Ler documentos em 02_DOCUMENTACAO_REFERENCIA/
2. Extrair conteúdo único
3. Criar CONSOLIDADO.md
4. Mover originais para 05_ARQUIVO_HISTORICO/

**Resultado Esperado:**
- Arquivo consolidado criado
- Arquivo histórico preenchido
- Base de conhecimento atualizada
```

---

## 🛠️ TIPOS DE TAREFAS SUPORTADAS

### 1. **CONSOLIDACAO**
Consolidar múltiplos arquivos em um

```yaml
tipo: consolidacao
acao: consolidar arquivos repetidos
origem: 02_DOCUMENTACAO_REFERENCIA/
destino: 01_DOCUMENTACAO_CONSOLIDADA/
arquivo_historico: 05_ARQUIVO_HISTORICO/
```

### 2. **ANALISE**
Analisar documentação e sugerir melhorias

```yaml
tipo: analise
acao: analisar processo existente
arquivos: 
  - GUIA_CLI.md
  - QUICKSTART.md
sugestoes: verdadeiro
```

### 3. **ATUALIZACAO_CONHECIMENTO**
Adicionar novos pontos à base de conhecimento

```yaml
tipo: atualizacao_conhecimento
categoria: integracoes
topicos:
  - Google Workspace
  - API Key management
fonte: GUIA_INTEGRACAO_GOOGLE.md
```

### 4. **MOVIMENTO_ARQUIVOS**
Mover arquivos para pastas apropriadas

```yaml
tipo: movimento_arquivos
origem: [arquivo1.md, arquivo2.md]
destino: 05_ARQUIVO_HISTORICO/
motivo: "Consolidados em CONSOLIDADO.md"
```

### 5. **MELHORIA_PROCESSO**
Sugerir e implementar melhoria em processo

```yaml
tipo: melhoria_processo
processo: "Gerenciamento de tarefas"
problema: "Tarefas espalhadas em vários arquivos"
solucao: "Centralizar em Tarefas.MD"
implementar: verdadeiro
```

---

## 🔧 COMO USAR COM CLI

### **Opção 1: Manual com CLI**

```bash
# Ver tarefas pendentes
python cli.py task "Ler Tarefas.MD e processar tarefas pendentes"

# Consolidar documentos
python cli.py task "Consolidar documentos em 02_DOCUMENTACAO_REFERENCIA"

# Analisar processo
python cli.py task "Analisar e sugerir melhorias no GUIA_CLI.md"

# Mover arquivos
python cli.py task "Mover arquivos consolidados para 05_ARQUIVO_HISTORICO"

# Atualizar conhecimento
python cli.py task "Adicionar integração Google Workspace à base de conhecimento"
```

### **Opção 2: Automático (Script Watch)**

Criar arquivo `watch_tasks.py`:

```python
#!/usr/bin/env python3
"""Script para monitorar Tarefas.MD e processar automaticamente"""

import time
from pathlib import Path
from app.agents.evolutionary_agent import EvolutionaryAgent

agent = EvolutionaryAgent()

def process_tasks_file():
    tasks_file = Path("Tarefas.MD")
    
    if not tasks_file.exists():
        print("❌ Arquivo Tarefas.MD não encontrado")
        return
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enviar para agente processar
    result = agent.process_task(
        task_description="Processar tarefas do arquivo Tarefas.MD",
        context=content,
        files_context=["Tarefas.MD"]
    )
    
    print(f"✅ Tarefas processadas!")
    print(f"Status: {result['status']}")
    print(f"Resposta: {result['response'][:200]}...")

if __name__ == '__main__':
    print("🔍 Monitorando Tarefas.MD...")
    
    last_mtime = 0
    while True:
        try:
            mtime = Path("Tarefas.MD").stat().st_mtime
            
            if mtime > last_mtime:
                print("📝 Detectada mudança em Tarefas.MD")
                process_tasks_file()
                last_mtime = mtime
            
            time.sleep(10)  # Verificar a cada 10 segundos
        
        except KeyboardInterrupt:
            print("\n👋 Script parado")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            time.sleep(10)
```

Usar:
```bash
python watch_tasks.py
```

---

## 🎓 O QUE O AGENTE APRENDERA

Quando processar suas tarefas, o agente vai aprender:

```
📚 Base de Conhecimento Atualizada:

1. **Estrutura de Projetos**
   - Melhor organização de pastas
   - Nomenclatura consistente
   - Arquivamento eficiente

2. **Processos de Consolidação**
   - Como identificar redundâncias
   - Melhores práticas de merge
   - Eliminação de duplicatas

3. **Categorização**
   - Documentação → 01_DOCUMENTACAO_CONSOLIDADA/
   - Referências → 02_DOCUMENTACAO_REFERENCIA/
   - Histórico → 05_ARQUIVO_HISTORICO/
   - Operacional → 04_OPERACIONAL/

4. **Integrações Necessárias**
   - Google Workspace (Docs, Drive, Sheets)
   - APIs externas
   - Serviços web

5. **Melhorias Contínuas**
   - Automação de tarefas repetitivas
   - Otimização de processos
   - Sugestões baseadas em padrões
```

---

## 📊 EXEMPLO COMPLETO

### **Tarefa Inicial**
```markdown
## 🎯 Consolidar Documentação

Consolidar os 8 documentos em 02_DOCUMENTACAO_REFERENCIA/ 
em um arquivo único CONSOLIDADO_REFERENCIAS.md
```

### **Agente Processa:**
1. ✅ Lê 8 arquivos de referência
2. ✅ Identifica conteúdo duplicado
3. ✅ Merge em 1 arquivo consolidado
4. ✅ Move originais para histórico
5. ✅ Atualiza índice

### **Resultado:**
```
02_DOCUMENTACAO_REFERENCIA/
├── CONSOLIDADO_REFERENCIAS.md     (📝 NOVO)
├── Diretrizes do Sistema/          (movido)
└── ...

05_ARQUIVO_HISTORICO/
├── 05-12-25/
│   ├── Documento 1.md             (📦 MOVIDO)
│   ├── Documento 2.md             (📦 MOVIDO)
│   └── ...

01_DOCUMENTACAO_CONSOLIDADA/
└── CONSOLIDADO_REFERENCIAS.md    (✨ ATUALIZADO)
```

---

## 🔗 LOCAIS QUE PRECISAM API KEY

| Local | Necessidade | Como Usar |
|-------|------------|-----------|
| Frontend Config | Processar tarefas | `Configuração` tab → Cole API key |
| CLI | Executar comandos | Variável `.env` ou argumento |
| Backend API | Processar requests | `.env` OPENAI_API_KEY |
| Web Importer | Processar conteúdo web | Não precisa (usa requests) |
| Task Manager | Salvar tarefas | Não precisa (JSON local) |

**Boas práticas:**
- ✅ Sempre usar `.env` para produção
- ✅ Nunca commit API key
- ✅ Rotar keys regularmente
- ✅ Usar keys com escopo limitado

---

## 🚀 COMANDOS ÚTEIS

```bash
# Ler e processar Tarefas.MD
python cli.py task "Processar arquivo Tarefas.MD"

# Consolidar documentação
python cli.py task "Consolidar 02_DOCUMENTACAO_REFERENCIA"

# Ver o que foi aprendido
python cli.py stats

# Ver timeline de tarefas processadas
python cli.py timeline --limit 20

# Buscar por tema
python cli.py search "consolidacao"

# Exportar conhecimento atualizado
python cli.py knowledge --format markdown > knowledge_updated.md
```

---

## ✨ SUGESTÕES QUE O AGENTE VAI DAR

Após processar tarefas, você verá sugestões como:

```
🎓 SUGESTÕES DE MELHORIA:

1. "Considere separar Configuração em arquivo próprio"
   → Criar config.md com todas as variáveis

2. "Há 3 seções repetidas entre CLI.md e QUICKSTART.md"
   → Consolidar em um arquivo único

3. "Processo de importação web pode ser otimizado"
   → Adicionar cache de URLs já importadas

4. "Base de conhecimento está crescendo"
   → Considerar migrar para banco de dados

5. "Documentação de integração está incompleta"
   → Adicionar exemplos de código para Google Workspace
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Agora:** Usar CLI ou frontend para criar tarefas
2. **Semana 1:** Consolidar documentação existente
3. **Semana 2:** Integrar Google Workspace conforme agente sugere
4. **Semana 3:** Implementar melhorias recomendadas
5. **Semana 4:** Agente evolui e aprende mais

---

## 📞 SUPORTE

Se tiver dúvida:
1. Veja `GUIA_USO_AGENTE.md` para exemplos
2. Rode `python cli.py help`
3. Consulte `README_APP.md` para referência técnica

🚀 **Você está pronto!**

