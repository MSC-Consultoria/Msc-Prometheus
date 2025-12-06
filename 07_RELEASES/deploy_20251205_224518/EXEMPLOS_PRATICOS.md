# 💡 Exemplos Práticos - Prometheus Agente Evolutivo

## 🎯 Exemplos de Tarefas e Respostas

### Exemplo 1: Documentação Juniper

#### Input (Tarefa)
```
Descrição:
"Crie um exemplo completo de documentação no formato Juniper para um módulo de autenticação"

Contexto:
"Use type hints, docstrings em EN/PT, inclua exemplo de uso"
```

#### Resposta Esperada
```markdown
# Módulo de Autenticação - Documentação Juniper

## 📋 Visão Geral
Authentication module following Juniper format (Python + Markdown).

## 🔐 Implementação

```python
from typing import Optional, Dict, Tuple
from dataclasses import dataclass

@dataclass
class User:
    """Usuário do sistema"""
    username: str
    password_hash: str
    email: str

class AuthManager:
    """Gerenciador de autenticação"""
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        Autentica usuário
        
        Args:
            username: Nome de usuário
            password: Senha em texto plano
            
        Returns:
            Usuário autenticado ou None
        """
        # Implementation...
```

## 📖 Exemplo de Uso

```python
from auth import AuthManager

manager = AuthManager()
user = manager.authenticate("john", "secret123")
if user:
    print(f"Bem-vindo {user.username}")
```

## 🎓 Aprendizados
- Type hints melhoram IDE support
- Docstrings bilíngues facilitam colaboração
- Exemplos práticos ajudam adoção
```

#### Aprendizados Extraídos
```
✅ documentation
✅ code-structure
✅ type-hints
✅ bilingual-content
```

---

### Exemplo 2: Conversão de Código

#### Input (Tarefa)
```
Descrição:
"Converta este script Bash para Python multiplataforma (Windows/Linux/macOS)"

Contexto:
"Script que lista arquivos recursivamente e conta linhas de código"

```bash
#!/bin/bash
find . -name "*.py" -type f -exec wc -l {} + | tail -1
find . -name "*.md" -type f -exec wc -l {} + | tail -1
```
```

#### Resposta Esperada
```python
from pathlib import Path
from typing import Dict

def count_lines_by_extension(directory: str = ".") -> Dict[str, int]:
    """
    Count lines of code by file extension (cross-platform)
    
    Conta linhas de código por extensão (multiplataforma)
    
    Args:
        directory: Diretório para análise
        
    Returns:
        Dicionário com extensão e linhas
    """
    results = {}
    base_path = Path(directory)
    
    for pattern in ["*.py", "*.md"]:
        total_lines = 0
        for file in base_path.rglob(pattern):
            try:
                total_lines += len(file.read_text(encoding='utf-8').splitlines())
            except Exception as e:
                print(f"Erro lendo {file}: {e}")
        
        results[pattern] = total_lines
    
    return results

# Example / Exemplo
if __name__ == "__main__":
    stats = count_lines_by_extension()
    for ext, lines in stats.items():
        print(f"{ext}: {lines} linhas")
```

#### Aprendizados Extraídos
```
✅ cross-platform
✅ pathlib-usage
✅ error-handling
✅ bilingual-examples
```

---

### Exemplo 3: Análise de Infra

#### Input (Tarefa)
```
Descrição:
"Analise este Dockerfile e sugira melhorias"

Contexto:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "main.py"]
```
```

#### Resposta Esperada
```markdown
# Análise de Dockerfile - Melhorias Sugeridas

## 🔴 Problemas Encontrados

1. **Falta de tag específica**
   - Usar `python:3.11-slim` ao invés de `python:3.9`

2. **Layer não otimizado**
   - COPY antes de RUN desnecessário

3. **Falta de multi-stage**
   - Build e runtime devem ser separados

## ✅ Dockerfile Otimizado

```dockerfile
# Stage 1: Build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
HEALTHCHECK --interval=30s CMD python -c "import requests; requests.get('http://localhost:5000')"
CMD ["python", "main.py"]
```

## 🎯 Benefícios
- Imagem 70% menor (slim base)
- Build mais rápido (multi-stage)
- Healthcheck incluído
- PATH correto para user packages
```

#### Aprendizados Extraídos
```
✅ docker-optimization
✅ multi-stage-builds
✅ performance
✅ best-practices
```

---

## 🔌 Exemplos de API

### API: Criar Tarefa

**Request:**
```bash
curl -X POST http://localhost:5000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Crie um exemplo de teste unitário em Python",
    "context": "Use pytest, mocks, e coverage"
  }'
```

**Response:**
```json
{
  "task_id": "task_1733406600",
  "status": "success",
  "response": "# Teste Unitário com Pytest\n\n...",
  "learning_points": ["testing", "mocking", "best-practices"],
  "elapsed_time": 2.34,
  "timestamp": "2025-12-05T10:31:00",
  "evolution_count": 1
}
```

### API: Buscar Conhecimento

**Request:**
```bash
curl "http://localhost:5000/api/knowledge/search?q=teste+unitário"
```

**Response:**
```json
{
  "query": "teste unitário",
  "results_count": 1,
  "results": [
    {
      "task_id": "task_1733406600",
      "excerpt": "# Teste Unitário com Pytest\n\n## Exemplo Básico\n..."
    }
  ]
}
```

---

## 🐍 Exemplos em Python

### Usar Agente Diretamente

```python
from app.agents.evolutionary_agent import EvolutionaryAgent
import json

# Inicializar
agent = EvolutionaryAgent()

# Tarefa 1: Documentação
result1 = agent.process_task(
    task_description="Crie um exemplo de design pattern Factory",
    context="Use Python, type hints, e example de uso"
)

print(f"✅ Tarefa 1: {result1['status']}")
print(f"   Learning: {result1['learning_points']}")
print(f"   Tempo: {result1['elapsed_time']}s\n")

# Tarefa 2: Análise
result2 = agent.process_task(
    task_description="Analise esse código SQL",
    context="SELECT * FROM users WHERE active = 1",
    files_context=[]
)

print(f"✅ Tarefa 2: {result2['status']}")

# Ver estatísticas
stats = agent.get_stats()
print(f"\n📊 Estatísticas:")
print(f"   Total: {stats['total_tasks']}")
print(f"   Taxa: {stats['success_rate']}")
print(f"   Conhecimento: {stats['knowledge_entries']} items")

# Ver timeline
timeline = agent.get_evolution_timeline(limit=5)
print(f"\n📈 Timeline:")
for item in timeline:
    print(f"   {item['timestamp']}: {item['task']}")

# Exportar conhecimento
knowledge = agent.export_knowledge(format='markdown')
with open('conhecimento.md', 'w', encoding='utf-8') as f:
    f.write(knowledge)
    
print("\n✅ Conhecimento exportado para conhecimento.md")
```

---

## 🎨 Exemplos de Workflow Completo

### Workflow: Criar CLI Tool

#### Tarefa 1: Planejamento
```
Descrição:
"Crie um plano de implementação para CLI tool que gerencia tarefas"
```

Resposta: Estrutura, dependências, arquitetura

#### Tarefa 2: Código Core
```
Descrição:
"Implemente o módulo core do CLI com argparse"
```

Resposta: Código Python pronto

#### Tarefa 3: Testes
```
Descrição:
"Crie testes unitários para o CLI"
```

Resposta: Testes com pytest

#### Tarefa 4: Documentação
```
Descrição:
"Crie documentação completa em formato Juniper"
```

Resposta: README, exemplos, API docs

**Resultado Final:**
- Agente aprendeu: planning, python, testing, documentation
- Base de conhecimento: 4 items
- CLI tool: Pronto para usar

---

## 📊 Métricas de Exemplo

### Antes (Manual)
```
⏱️  Tempo: 8 horas
👨 Esforço: 1 pessoa
📚 Documentação: Incompleta
🐛 Qualidade: Média
💰 Custo: $0 (seu tempo)
```

### Depois (Com Prometheus)
```
⏱️  Tempo: 30 minutos
👨 Esforço: 1 pessoa + agente
📚 Documentação: Completa e estruturada
🐛 Qualidade: Alta
💰 Custo: ~$1 em API
```

**Resultado: 16x mais rápido, 10x melhor qualidade, 1000x melhor ROI**

---

## 🎯 Tarefas Recomendadas (Passo a Passo)

### Fase 1: Aprender (Dia 1)
```
1. "Qual é o padrão Juniper e por que usar?"
2. "Crie um exemplo de Juniper com Python"
3. "Explique type hints com exemplos"
4. "Crie documentação em formato Markdown"
5. "Como estruturar um projeto Python?"
```

### Fase 2: Praticar (Dia 2-3)
```
6. "Converta script Bash para Python"
7. "Analise este código e sugira melhorias"
8. "Crie testes para esta função"
9. "Implemente um design pattern"
10. "Crie CLI para processar arquivos"
```

### Fase 3: Dominar (Semana 1-2)
```
11. "Crie um sistema completo de logging"
12. "Implemente integração com Google Drive"
13. "Crie pipeline de CI/CD"
14. "Implemente autenticação JWT"
15. "Crie API REST completa"
```

---

## 💾 Resultado em JSON

Após 15 tarefas, histórico fica assim:

```json
{
  "total_tasks": 15,
  "successful": 15,
  "success_rate": "100%",
  "knowledge_entries": 15,
  "learning_areas": [
    "documentation",
    "code-structure",
    "testing",
    "python-best-practices",
    "api-design",
    "deployment",
    "authentication",
    "performance",
    "security",
    "cross-platform",
    "docker",
    "ci-cd",
    "logging",
    "integration",
    "juniper-format"
  ],
  "total_tokens_used": 12543,
  "avg_response_time": 2.8,
  "most_common_topic": "python",
  "expertise_level": "Expert"
}
```

---

## 🚀 Próximas Ideias

- [ ] Criar uma série de tarefas sobre microserviços
- [ ] Aprender sobre GraphQL
- [ ] Aprender sobre machine learning
- [ ] Criar documentação de projeto real
- [ ] Analisar código legado
- [ ] Planejar arquitetura nova
- [ ] Implementar segurança
- [ ] Otimizar performance

---

**Comece com a Tarefa 1 agora!** 🎯

`python run.py` → Nova Tarefa → Enviar
