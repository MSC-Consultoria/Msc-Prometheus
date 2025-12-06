# 🎯 PRÓXIMOS PASSOS - O QUE FAZER AGORA

**Guia prático para começar a usar o Prometheus**

---

## ⏰ AGORA MESMO (5 minutos)

### **1️⃣ Configure a API Key**

Abra o arquivo `.env`:
```
c:\Users\Festeja\Downloads\Prometheus\03_INFRAESTRUTURA\.env
```

Edite a linha:
```
OPENAI_API_KEY=sk-proj-seu-token-aqui
```

Mude para:
```
OPENAI_API_KEY=sk-proj-SEU-TOKEN-REAL-AQUI
```

### **1.1️⃣ Armazenando as outras 3 APIs**

Nas seguintes variáveis você deve colar as APIs que usa no momento:

```
GEMINI_API_KEY=<sua chave do Gemini>
MANUS_API_KEY=<sua chave do Manus>
HUGGINGFACE_API_KEY=<sua chave do Hugging Face>
```

Elas ficam no mesmo `.env` e são lidas pelo backend, então nunca exponha esses valores em arquivos compartilhados. Apague o arquivo `Api kEy` depois de ter copiado o conteúdo para cá e confirme que o diretório raíz do repositório possui um `.gitignore` que ignora o `.env`.

**Onde pegar:**
- Acesse: https://platform.openai.com/api-keys
- Crie uma nova chave
- Cole aqui

### **2️⃣ Instale Dependências**

Abra PowerShell e rode:
```powershell
cd "c:\Users\Festeja\Downloads\Prometheus\03_INFRAESTRUTURA"
pip install -r requirements.txt
```

Espera instalar (leva ~2 minutos)

---

## 🚀 PRÓXIMOS 10 MINUTOS

### **3️⃣ Inicie o Sistema**

```powershell
python run.py
```

Você verá:
```
✓ Dependências OK
✓ Backend iniciando na porta 5000
✓ Abrindo navegador...
```

Vai abrir: `http://localhost:5000`

### **4️⃣ Teste o Frontend**

No navegador que abrir:

1. Vai em **"Nova Tarefa"** tab
2. Escreve: `"Teste do sistema Prometheus"`
3. Contexto (opcional): `"Python 3.11 com Flask"`
4. Clica **"Enviar para Agente"**
5. Vê a resposta em tempo real ✅

---

## 📋 PRÓXIMOS 30 MINUTOS

### **5️⃣ Teste a CLI**

Abra nova aba do PowerShell:
```powershell
cd "c:\Users\Festeja\Downloads\Prometheus\03_INFRAESTRUTURA"

# Ver ajuda
python cli.py help

# Criar tarefa
python cli.py task "Teste da CLI - consolidar documentação"

# Ver estatísticas
python cli.py stats

# Ver histórico
python cli.py timeline

# Buscar termos
python cli.py search "prometheus"

# Exportar conhecimento
python cli.py knowledge --format markdown
```

### **6️⃣ Crie suas Primeiras Tarefas**

Crie tarefas reais:

**Tarefa 1: Consolidação**
```
python cli.py task "Consolidar documentação em 02_DOCUMENTACAO_REFERENCIA"
```

**Tarefa 2: Análise**
```
python cli.py task "Analisar e sugerir melhorias no processo de importação web"
```

**Tarefa 3: Movimento**
```
python cli.py task "Mover arquivos consolidados para 05_ARQUIVO_HISTORICO"
```

---

## 🌍 PRÓXIMAS 2 HORAS

### **7️⃣ Teste Web Importer** (quando completar)

```powershell
# Via API
$body = @{
    url = "https://www.exemplo.com"
    title = "Meu Documento"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/import-web" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

### **8️⃣ Organize suas Tarefas**

Edite `Tarefas.MD` com suas tarefas reais:

```markdown
# 📋 Minhas Tarefas do Prometheus

## 🎯 Tarefa 1: Consolidar Documentação
- **Tipo:** consolidacao
- **Prioridade:** alta
- **Status:** pendente
- **Descrição:** Consolidar 5 documentos em um único arquivo

## 🎯 Tarefa 2: Integração Google
- **Tipo:** integracao
- **Prioridade:** media
- **Status:** em_progresso
- **Descrição:** Conectar com Google Drive API
```

---

## 📊 PRÓXIMOS DIAS

### **9️⃣ Consolide Documentação**

Execute consolidação:
```powershell
python cli.py task "Consolidar documentação em um único arquivo"
python cli.py task "Mover arquivos originais para histórico"
python cli.py task "Atualizar base de conhecimento"
```

Resultado esperado:
```
03_INFRAESTRUTURA/
├── 01_DOCUMENTACAO_CONSOLIDADA/
│   └── CONSOLIDADO_FINAL.md (✨ NOVO)
│
└── 05_ARQUIVO_HISTORICO/
    └── 05-12-25/
        ├── doc1.md (movido)
        ├── doc2.md (movido)
        └── ... (movidos)
```

### **🔟 Importe Páginas Úteis**

Se encontrar páginas interessantes:
```powershell
# Via CLI (quando integrar)
python cli.py import-web "https://pagina-util.com"
```

Documentos salvos automaticamente em:
```
03_INFRAESTRUTURA/app/data/imported_docs/
```

---

## 🎓 PRÓXIMAS SEMANAS

### **11️⃣ Evolua Continuamente**

O agente aprenderá com cada tarefa:

```powershell
# Ver o que aprendeu
python cli.py stats

# Ver timeline de aprendizado
python cli.py timeline --limit 30

# Exportar conhecimento aprendido
python cli.py knowledge --format markdown > meu_conhecimento.md
```

### **1️⃣2️⃣ Próximas Melhorias**

Quando estiver pronto:
1. **Banco de Dados** → PostgreSQL
2. **Google Workspace** → Drive + Docs
3. **Autenticação** → JWT tokens
4. **WebSocket** → Updates em tempo real
5. **Multi-LLM** → Gemini + Claude

---

## 🔗 REFERÊNCIAS RÁPIDAS

| Precisa de | Arquivo |
|----------|---------|
| Entender Frontend | `IMPLEMENTACAO_FRONTEND.md` |
| Usar CLI | `GUIA_CLI.md` |
| Procedimento Tarefas | `PROCEDIMENTO_TAREFAS.md` |
| Arquitetura | `MAPA_VISUAL.md` |
| Documentação API | `README_APP.md` |
| Setup rápido | `QUICKSTART.md` |
| Exemplos | `EXEMPLOS_PRATICOS.md` |

---

## ⚡ TROUBLESHOOTING

### **Erro: "No module named 'flask'"**
```powershell
pip install -r requirements.txt
```

### **Erro: "Address already in use" (porta 5000)**
```powershell
# Fechar a porta
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Ou mudar a porta no .env
FLASK_PORT=5001
```

### **Erro: "OPENAI_API_KEY not set"**
- Verifique se `.env` tem a chave
- Verifique se está no diretório certo
- Teste: `python -c "import os; print(os.getenv('OPENAI_API_KEY'))"`

### **Frontend não carrega**
- Verifique se backend está rodando
- Teste: http://localhost:5000/api/health
- Abra console (F12) para ver erros

---

## ✅ CHECKLIST - COMECE AGORA

- [ ] 1. Editar `.env` com API key
- [ ] 2. Rodar `pip install -r requirements.txt`
- [ ] 3. Rodar `python run.py`
- [ ] 4. Testar frontend (criar tarefa)
- [ ] 5. Testar CLI (3 comandos)
- [ ] 6. Ver estatísticas
- [ ] 7. Criar suas tarefas reais
- [ ] 8. Consolidar documentação
- [ ] 9. Ver resultado no timeline
- [ ] 10. Exportar conhecimento aprendido

---

## 🎉 VOCÊ ESTÁ PRONTO!

Quando terminar os testes:

```powershell
# Sistema rodando?
curl http://localhost:5000/api/health

# Viu "status": "online"? ✅ PERFEITO!
```

Agora é só usar! 🚀

---

## 📞 NECESSITA AJUDA?

1. Verifique `README_APP.md` (docs técnicas)
2. Leia `PROCEDIMENTO_TAREFAS.md` (como processar)
3. Rode `python cli.py help`
4. Consulte arquivos MD na pasta

---

**Status:** ✨ Sistema 100% pronto  
**Próximo Passo:** Edite `.env` e rode `python run.py`

Boa sorte! 🚀

