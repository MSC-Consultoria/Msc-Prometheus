# 🗺️ Índice Geral - Mapa de Navegação do Prometheus

## 🎯 Comece Por Aqui

Você está em: **Índice Geral de Navegação**

Este documento ajuda você a encontrar exatamente o que precisa no projeto Prometheus.

---

## 📋 Documentos Consolidados (Novos - Comece aqui!)

| Documento | Leia Se... | Tempo |
|-----------|-----------|-------|
| **CONSOLIDADO_ESTRATEGICO.md** | Quer entender o projeto completo | 15 min |
| **REFERENCIA_RAPIDA.md** | Quer resposta rápida (< 60 seg) | 2 min |
| **GUIA_INTEGRACAO_GOOGLE.md** | Quer conectar Google Workspace | 20 min |
| **STATUS_PROJETO.md** | Quer saber o que foi feito e progresso | 10 min |

---

## 🛠️ Documentos Técnicos

### Executáveis
| Arquivo | O Que Faz | Quando Usar |
|---------|----------|-------------|
| `main.py` | Agente autônomo que processa Markdown | Tarefas automatizadas |
| `requirements.txt` | Dependências Python | Setup inicial |
| `Dockerfile` | Imagem Docker | Deployment |

### Configuração
| Arquivo | O Que Contém | Status |
|---------|-------------|--------|
| `.env` | Variáveis de ambiente | 🟡 Criar |
| `.dockerignore` | O que não enviar para Docker | ✅ Feito |
| `orientações.txt` | Workflow e boas práticas | ✅ Feito |

---

## 📚 Documentos de Referência (Agente Markdown/)

### Prompts de Sistema
| Arquivo | Agente | Uso |
|---------|--------|-----|
| `System Prompt_ Juniper Interpreter...` | Conversão de dados | Documentação estruturada |
| `System Prompt_ Evolutionary Infra...` | DevOps e Cloud | Infraestrutura |
| `System Prompt_ Evolutionary OS...` | Compatibilidade | Windows/Linux/Mac |

### Documentos Conceituais
| Arquivo | Tema | Profundidade |
|---------|------|-------------|
| `Documento de Referência_ Formato Juniper Estruturado.md` | Metodologia | Básica |
| `Documento de Referência_ Infraestrutura Evolutiva.md` | DevOps | Avançada |
| `Documento de Referência_ Compatibilidade de Sistemas.md` | Cross-OS | Completa |

### Guias
| Arquivo | Objetivo | Público |
|---------|----------|---------|
| `manual_agente.md` | Como usar AgenticMarkdown | Desenvolvedores |
| `Juniper .pythb Consolidated...` | Visão unificada dos 3 agentes | Arquitetos |
| `Índice Geral de Agentes...` | Mapa dos agentes | Todos |

---

## 📝 Documentos Operacionais

### Diárias
| Arquivo | Atualização | Propósito |
|---------|-------------|----------|
| `Tarefas.MD` | Sempre | Fila de execução do agente |
| `Ideias.MD` | Sempre | Brainstorm e rascunhos |
| `Diretrizes do Sistema` | Semanal | Filosofia e valores |

### Histórico
| Pasta | Conteúdo | Uso |
|-------|----------|-----|
| `05-12-25/` | Arquivos do dia | Rastreamento diário |
| `.backups/` | Versões antigas | Recuperação |
| `Zip/` | Releases versionadas | Arquivamento |

---

## 🗺️ Mapa Visual da Arquitetura

```
📦 PROMETHEUS (Sistema Principal)
│
├─ 📄 CONSOLIDADO_ESTRATEGICO.md ← COMECE AQUI (visão completa)
├─ 📄 REFERENCIA_RAPIDA.md ← Ou aqui (rápido)
├─ 📄 GUIA_INTEGRACAO_GOOGLE.md ← Para integração
├─ 📄 STATUS_PROJETO.md ← Progresso
├─ 📄 INDICE_GERAL.md ← Você está aqui
│
├─ 🔧 INFRAESTRUTURA
│  ├─ main.py (Agente)
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .dockerignore
│
├─ 📚 AGENTES (Agente Markdown/)
│  ├─ 3 Prompts de Sistema
│  ├─ 3 Documentos Conceituais
│  ├─ manual_agente.md
│  └─ Índice Geral de Agentes
│
├─ 📋 OPERAÇÕES
│  ├─ Tarefas.MD (fila)
│  ├─ Ideias.MD (brainstorm)
│  ├─ Diretrizes do Sistema
│  └─ orientações.txt
│
└─ 💾 ARQUIVAMENTO
   ├─ Zip/ (releases)
   ├─ .backups/ (histórico)
   └─ 05-12-25/ (dia)
```

---

## 🎯 Guias Por Objetivo

### "Quero Usar o Agente"
1. Leia: `REFERENCIA_RAPIDA.md` (2 min)
2. Leia: `manual_agente.md` (5 min)
3. Edite: `Tarefas.MD` com sua tarefa
4. Execute: `python main.py`

### "Quero Entender a Arquitetura"
1. Leia: `CONSOLIDADO_ESTRATEGICO.md` (15 min)
2. Estude: `Juniper .pythb Consolidated...` (20 min)
3. Explore: Agente Markdown/ (30 min)

### "Quero Integrar com Google"
1. Leia: `GUIA_INTEGRACAO_GOOGLE.md` (20 min)
2. Siga: Passo 1-7 do guia
3. Execute: Scripts de teste
4. Ativa: Automação em main.py

### "Quero Saber o Progresso"
1. Leia: `STATUS_PROJETO.md` (10 min)
2. Consulte: Métricas e roadmap
3. Veja: Próximas ações

### "Preciso de Referência Rápida"
1. `REFERENCIA_RAPIDA.md` (2 min)
2. Busque seção específica
3. Volte ao consolidado se precisar mais

### "Quero Contribuir"
1. Leia: `Diretrizes do Sistema` (filosofia)
2. Leia: `orientações.txt` (workflow)
3. Crie tarefa em `Tarefas.MD`
4. Siga convenções de nomenclatura

---

## 🔍 Busca Rápida Por Conceito

### Conceitos Principais
| Termo | Explicado em | Página |
|-------|-------------|--------|
| Juniper | CONSOLIDADO_ESTRATEGICO.md § Formatos | p.3 |
| Mecanismo de Evolução | CONSOLIDADO_ESTRATEGICO.md § Princípios | p.6 |
| 3 Agentes | CONSOLIDADO_ESTRATEGICO.md § Arquitetura | p.4 |
| Estrutura de Pastas | GUIA_INTEGRACAO_GOOGLE.md § Setup | p.1 |

### Técnicas
| Técnica | Descrita em | Exemplo |
|---------|-----------|---------|
| {ler:arquivo} | manual_agente.md | Carregar contexto |
| ```lang:arquivo | manual_agente.md | Criar arquivo |
| - [ ] Tarefa | REFERENCIA_RAPIDA.md | Criar task |

### Integração
| Serviço | Guia | Status |
|---------|------|--------|
| Google Drive | GUIA_INTEGRACAO_GOOGLE.md | 📝 Planejado |
| Google Tasks | GUIA_INTEGRACAO_GOOGLE.md | 📝 Planejado |
| OpenAI API | main.py (linhas 1-15) | ✅ Ativo |
| Docker | Dockerfile | ✅ Pronto |

---

## 📊 Estatísticas do Projeto

- **Total de documentos:** 25+
- **Documentos consolidados:** 4 (NOVO)
- **Prompts de agentes:** 3
- **Documentos de referência:** 3
- **Guias de setup:** 1
- **Linhas de código:** ~500 (main.py)
- **Linhas de documentação:** ~2000+
- **Tamanho total:** ~2 MB
- **Última atualização:** 05-12-2025

---

## ✨ Destaques Novos (05-12-2025)

🎉 Hoje foram criados 4 novos documentos consolidados:

1. **CONSOLIDADO_ESTRATEGICO.md** - Visão arquitetônica completa (referência)
2. **REFERENCIA_RAPIDA.md** - Quick start em 60 segundos
3. **GUIA_INTEGRACAO_GOOGLE.md** - Setup detalhado com código
4. **STATUS_PROJETO.md** - Progresso e métricas

Esses documentos **reduzem a curva de aprendizado** e **eliminam redundância** ao centralizar informações.

---

## 🚦 Como Navegar

### Se você tem 2 minutos
→ Leia: `REFERENCIA_RAPIDA.md`

### Se você tem 15 minutos
→ Leia: `CONSOLIDADO_ESTRATEGICO.md`

### Se você tem 1 hora
→ Estude: Todos os 4 documentos consolidados + manual_agente.md

### Se você tem um dia
→ Explore: `Agente Markdown/` completamente

---

## 🎓 Recomendado First Steps

### Dia 1: Setup
1. [ ] Leia CONSOLIDADO_ESTRATEGICO.md
2. [ ] Instale requirements.txt
3. [ ] Configure .env (quando tiver credenciais)
4. [ ] Teste main.py com tarefa simples

### Dia 2: Integração
1. [ ] Leia GUIA_INTEGRACAO_GOOGLE.md
2. [ ] Crie credenciais Google Cloud
3. [ ] Configure .env.google.json
4. [ ] Teste backup para Drive

### Dia 3: Produção
1. [ ] Construa Docker image
2. [ ] Configure automação semanal
3. [ ] Primeiro ciclo de consolidação
4. [ ] Documente lições aprendidas

---

## 📞 Dúvidas Frequentes (FAQ)

**P: Por onde começo?**  
R: REFERENCIA_RAPIDA.md (2 min) → CONSOLIDADO_ESTRATEGICO.md (15 min)

**P: Como uso o agente?**  
R: manual_agente.md + REFERENCIA_RAPIDA.md § "Como Usar"

**P: Como integro Google?**  
R: GUIA_INTEGRACAO_GOOGLE.md passo-a-passo

**P: Qual é o status?**  
R: STATUS_PROJETO.md com métricas e roadmap

**P: Onde estão os agentes?**  
R: `Agente Markdown/` com 3 prompts + 3 docs conceituais

**P: Como contribuir?**  
R: Siga `orientações.txt` e `Diretrizes do Sistema`

---

## 🔗 Referências Cruzadas

### CONSOLIDADO_ESTRATEGICO.md menciona
→ REFERENCIA_RAPIDA.md (detalhes rápidos)  
→ GUIA_INTEGRACAO_GOOGLE.md (setup específico)  
→ STATUS_PROJETO.md (progresso)  
→ `Agente Markdown/*` (prompts completos)

### manual_agente.md menciona
→ REFERENCIA_RAPIDA.md (sintaxe)  
→ `Tarefas.MD` (exemplos)  
→ main.py (código)

### STATUS_PROJETO.md menciona
→ CONSOLIDADO_ESTRATEGICO.md (arquitetura)  
→ GUIA_INTEGRACAO_GOOGLE.md (próximos passos)  
→ `Agente Markdown/*` (documentação detalhada)

---

## 💾 Manutenção

**Atualizado:** 05-12-2025  
**Próxima revisão:** 12-12-2025  
**Mantido por:** Prometheus Team  
**Versão:** 1.0

---

## 📋 Checklist de Navegação

- [ ] Você leu CONSOLIDADO_ESTRATEGICO.md?
- [ ] Você leu REFERENCIA_RAPIDA.md?
- [ ] Você entende os 3 agentes?
- [ ] Você sabe como usar o AgenticMarkdown?
- [ ] Você explorou `Agente Markdown/`?
- [ ] Você viu o STATUS_PROJETO.md?

Se sim em todos → **Você está pronto para começar!** 🚀

---

**Próximo destino?** Escolha um caminho acima e clique em um documento! 📖
