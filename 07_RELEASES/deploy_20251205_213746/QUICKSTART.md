# ⚡ Quick Start - Prometheus em 5 Minutos

## 1️⃣ Instalar (1 minuto)

```bash
# Windows PowerShell
cd 03_INFRAESTRUTURA
pip install -r requirements.txt
```

## 2️⃣ Configurar (1 minuto)

```bash
# Criar .env com sua OpenAI API Key
# Opção A: Editar arquivo
Copy-Item .env.example .env
# Editar .env e adicionar OPENAI_API_KEY

# Opção B: Via PowerShell
$key = "sk-proj-sua-chave-aqui"
Add-Content -Path .env -Value "OPENAI_API_KEY=$key"
```

## 3️⃣ Executar (1 minuto)

```bash
python run.py
```

Automaticamente:
- ✅ Verifica dependências
- ✅ Inicia API em http://localhost:5000
- ✅ Abre dashboard no navegador

## 4️⃣ Testar (2 minutos)

### Via Interface
1. Escrever tarefa: "Crie um exemplo de Juniper"
2. Clicar "Enviar para Agente"
3. Ver resposta em tempo real

### Via Terminal
```bash
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{"description": "Oi, tudo bem?"}'
```

## ✨ Resultado Esperado

```json
{
  "task_id": "task_1733406600",
  "status": "success",
  "response": "# Resposta do Agente\n...",
  "learning_points": ["documentation"],
  "elapsed_time": 3.45,
  "evolution_count": 1
}
```

---

## 🎯 Próximas Tarefas

1. **Enviar 5 tarefas diferentes** para agente aprender
2. **Verificar stats** em http://localhost:5000
3. **Consultar timeline** no dashboard
4. **Ler GUIA_USO_AGENTE.md** para usos avançados

---

## ❌ Problemas?

### Erro: "OPENAI_API_KEY not found"
```bash
# Adicionar ao .env
echo 'OPENAI_API_KEY=sk-proj-xxx' >> .env
```

### Erro: "Port 5000 already in use"
```bash
# Usar outra porta em api.py linha 140:
# app.run(port=8000)
```

### Frontend não carrega
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health
```

---

**Pronto? Execute:** `python run.py` 🚀

Perguntas? Ver `GUIA_USO_AGENTE.md`
