"""
API REST - Prometheus Backend
Interface para o agente evolutivo
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Optional

from agents.evolutionary_agent import EvolutionaryAgent
from integrations import get_provider_status_summary
from integrations.github_copilot import github_client as github
from integrations.n8n_client import n8n_client as n8n

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Inicializar agente
agent = EvolutionaryAgent()

# Configuração de Autenticação (Simples)
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'prometheus2025')

# ==========================================
# ROTAS DE AUTENTICAÇÃO
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    """Autenticação simples"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USER and password == ADMIN_PASS:
        # Em produção, usar JWT real. Aqui usamos um token simples.
        return jsonify({
            "status": "success",
            "token": "prometheus-session-token-valid",
            "user": username
        }), 200
    
    return jsonify({"error": "Credenciais inválidas"}), 401

# ==========================================
# ROTAS DE SAÚDE
# ==========================================

@app.route('/api/health', methods=['GET'])
def health():
    """Verificar saúde da API"""
    return jsonify({
        "status": "online",
        "version": agent.version,
        "timestamp": datetime.now().isoformat()
    }), 200


# ==========================================
# ROTAS DO AGENTE
# ==========================================

@app.route('/api/task', methods=['POST'])
def create_task():
    """Criar nova tarefa para o agente processar"""
    try:
        data = request.json
        
        task_description = data.get('description')
        context = data.get('context', None)
        files = data.get('files', [])
        notify_n8n = data.get('notify_n8n', False)  # Opcional: enviar resultado para N8N
        
        if not task_description:
            return jsonify({"error": "description é obrigatório"}), 400
        
        # Processar tarefa
        result = agent.process_task(
            task_description=task_description,
            context=context,
            files_context=files
        )
        
        # Se solicitado, envia resultado para N8N
        if notify_n8n and result.get("status") == "success":
            try:
                n8n_result = n8n.send_task_result(result.get("task_id"), result)
                result['n8n_notification'] = {
                    "sent": n8n_result.get("status") == "success",
                    "execution_id": n8n_result.get("execution_id")
                }
            except Exception as n8n_error:
                result['n8n_notification'] = {
                    "sent": False,
                    "error": str(n8n_error)
                }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/stats', methods=['GET'])
def get_agent_stats():
    """Obter estatísticas do agente"""
    try:
        stats = agent.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/agent/provider', methods=['POST'])
def change_agent_provider():
    """
    Trocar o provedor de LLM do agente
    
    Body:
    {
        "provider": "openai|anthropic|gemini|deepseek|openrouter",
        "model": "gpt-4o-mini|claude-3-5-sonnet-20241022|gemini-pro|...",
        "api_key": "optional_api_key"
    }
    """
    try:
        data = request.json
        
        provider = data.get('provider')
        model = data.get('model')
        api_key = data.get('api_key')
        
        if not provider or not model:
            return jsonify({
                "error": "provider e model são obrigatórios"
            }), 400
        
        result = agent.change_provider(provider, model, api_key)
        
        if result.get("status") == "success":
            return jsonify({
                "status": "success",
                "message": f"Provedor alterado para {provider} com modelo {model}",
                "provider": result["provider"],
                "model": result["model"]
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Falha ao inicializar cliente. Verifique API key e dependências.",
                "provider": provider,
                "model": model
            }), 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/agent/timeline', methods=['GET'])
def get_timeline():
    """Obter timeline de evolução"""
    try:
        limit = request.args.get('limit', 20, type=int)
        timeline = agent.get_evolution_timeline(limit)
        return jsonify({"timeline": timeline}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/knowledge', methods=['GET'])
def get_knowledge():
    """Obter base de conhecimento"""
    try:
        format = request.args.get('format', 'json')
        knowledge = agent.export_knowledge(format)
        
        if format == 'json':
            return jsonify(json.loads(knowledge)), 200
        else:
            return knowledge, 200, {'Content-Type': 'text/markdown; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/knowledge/search', methods=['GET'])
def search_knowledge():
    """Buscar na base de conhecimento"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({"error": "parâmetro 'q' é obrigatório"}), 400
        
        results = []
        for task_id, content in agent.knowledge_base.items():
            if query.lower() in content.lower():
                results.append({
                    "task_id": task_id,
                    "excerpt": content[:200]
                })
        
        return jsonify({
            "query": query,
            "results_count": len(results),
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/import-url', methods=['POST'])
def import_url():
    """Converter página web em markdown e salvar na base de conhecimento"""
    try:
        import requests
        from bs4 import BeautifulSoup
        import html2text
        
        data = request.json
        url = data.get('url')
        category = data.get('category', 'Web_Imports')
        title = data.get('title', None)
        
        if not url:
            return jsonify({"error": "url é obrigatório"}), 400
        
        # Buscar conteúdo da página
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remover scripts, styles, etc
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Extrair título se não fornecido
        if not title:
            title_tag = soup.find('title')
            title = title_tag.string if title_tag else url.split('//')[-1].split('/')[0]
        
        # Converter para markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        markdown_content = h.handle(str(soup))
        
        # Criar estrutura do arquivo
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{timestamp}_{safe_title[:50]}.md"
        
        # Montar conteúdo final
        final_content = f"""# {title}

**Fonte:** {url}  
**Data de Importação:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Categoria:** {category}

---

{markdown_content}

---

**Metadados:**
- URL Original: {url}
- Importado via: Prometheus Web Importer
- Status: Ativo
"""
        
        # Salvar arquivo
        base_path = os.path.join(os.getcwd(), '08_BASES_CONHECIMENTO', category)
        os.makedirs(base_path, exist_ok=True)
        file_path = os.path.join(base_path, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return jsonify({
            "success": True,
            "message": "Página importada com sucesso",
            "file": filename,
            "path": file_path,
            "title": title,
            "url": url
        }), 200
        
    except requests.RequestException as e:
        return jsonify({"error": f"Erro ao acessar URL: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao processar: {str(e)}"}), 500


# ==========================================
# ROTAS DE CONFIGURAÇÃO
# ==========================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """Obter configuração do agente"""
    return jsonify({
        "agent": {
            "version": agent.version,
            "model": agent.model,
            "created_at": agent.created_at
        },
        "api": {
            "version": "1.0.0",
            "endpoints": [
                "POST /api/task",
                "GET /api/agent/stats",
                "GET /api/agent/timeline",
                "GET /api/knowledge",
                "GET /api/knowledge/search"
            ]
        }
    }), 200


@app.route('/api/integration-status', methods=['GET'])
def integration_status():
    """Status das integrações externas configuradas"""
    summary = get_provider_status_summary()
    missing = {name: info["hint"] for name, info in summary.items() if not info["configured"]}
    return jsonify({
        "providers": summary,
        "missing_keys": missing
    }), 200


# ==========================================
# ROTAS DE INTEGRAÇÃO - GITHUB COPILOT
# ==========================================

@app.route('/api/github/rate-limits', methods=['GET'])
def github_rate_limits():
    """
    Obter rate limits do GitHub API
    Retorna informações sobre quotas e uso atual
    """
    try:
        result = github.get_rate_limits()
        return jsonify(result), 200 if result.get("status") == "success" else 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Erro ao obter rate limits do GitHub"
        }), 500


@app.route('/api/github/status', methods=['GET'])
def github_status():
    """
    Verifica status da integração com GitHub
    Retorna se está conectado, autenticado e informações do usuário
    """
    try:
        result = github.check_status()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/github/user', methods=['GET'])
def github_user():
    """Obter informações do usuário GitHub autenticado"""
    try:
        result = github.get_user_info()
        return jsonify(result), 200 if result.get("status") == "success" else 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/github/copilot-usage', methods=['GET'])
def github_copilot_usage():
    """
    Obter estatísticas de uso do GitHub Copilot
    Requer Copilot Business ou Enterprise
    """
    try:
        result = github.get_copilot_usage()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ==========================================
# ROTAS DE INTEGRAÇÃO - N8N
# ==========================================

@app.route('/api/n8n/webhook', methods=['POST'])
def n8n_webhook():
    """
    Recebe webhooks do N8N para processar tarefas
    
    Expected payload:
    {
        "task": "descrição da tarefa",
        "context": "contexto opcional",
        "workflow_id": "id do workflow que enviou"
    }
    """
    try:
        # Validar assinatura se configurada
        signature = request.headers.get('X-N8N-Signature', '')
        if signature:
            is_valid = n8n.validate_webhook_signature(request.data, signature)
            if not is_valid:
                return jsonify({
                    "status": "error",
                    "error": "Invalid signature",
                    "message": "Assinatura do webhook inválida"
                }), 401
        
        data = request.json
        
        task_description = data.get('task')
        context = data.get('context')
        workflow_id = data.get('workflow_id', 'unknown')
        
        if not task_description:
            return jsonify({
                "status": "error",
                "error": "task é obrigatório"
            }), 400
        
        # Processar tarefa com o agente
        result = agent.process_task(
            task_description=task_description,
            context=context
        )
        
        # Adicionar informações do webhook
        result['source'] = 'n8n'
        result['workflow_id'] = workflow_id
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/n8n/trigger', methods=['POST'])
def n8n_trigger():
    """
    Trigga um workflow específico no N8N
    
    Body:
    {
        "workflow_id": "nome-do-workflow",
        "data": { ... },
        "wait": false
    }
    """
    try:
        data = request.json
        
        workflow_id = data.get('workflow_id')
        workflow_data = data.get('data', {})
        wait = data.get('wait', False)
        
        if not workflow_id:
            return jsonify({
                "status": "error",
                "error": "workflow_id é obrigatório"
            }), 400
        
        result = n8n.trigger_workflow(workflow_id, workflow_data, wait=wait)
        return jsonify(result), 200 if result.get("status") == "success" else 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/n8n/status', methods=['GET'])
def n8n_status():
    """Verifica status da integração com N8N"""
    try:
        result = n8n.check_status()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/n8n/notify', methods=['POST'])
def n8n_notify():
    """
    Envia notificação através do N8N
    
    Body:
    {
        "message": "Mensagem a enviar",
        "channel": "slack|email|discord",
        "level": "info|warning|error|success"
    }
    """
    try:
        data = request.json
        
        message = data.get('message')
        channel = data.get('channel', 'general')
        level = data.get('level', 'info')
        
        if not message:
            return jsonify({
                "status": "error",
                "error": "message é obrigatório"
            }), 400
        
        result = n8n.send_notification(message, channel, level)
        return jsonify(result), 200 if result.get("status") == "success" else 500
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


# ==========================================
# ROTAS DE UTILIDADE
# ==========================================

@app.route('/', methods=['GET'])
def root():
    """Página raiz - informações da API"""
    return jsonify({
        "name": "Prometheus API",
        "description": "API do Sistema de Agentes Evolutivos Prometheus",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/api/health",
        "status": "running"
    }), 200


@app.route('/docs', methods=['GET'])
def docs():
    """Documentação da API"""
    return jsonify({
        "title": "Prometheus API Documentation",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/health": "Verificar saúde da API",
            "POST /api/task": "Criar nova tarefa",
            "GET /api/agent/stats": "Estatísticas do agente",
            "GET /api/agent/timeline": "Timeline de evolução",
            "GET /api/knowledge": "Base de conhecimento",
            "GET /api/knowledge/search": "Buscar na base de conhecimento",
            "GET /api/config": "Configuração do agente",
            "GET /api/integration-status": "Status das integrações externas",
            "POST /api/import-url": "Importar página web para markdown",
            "GET /api/tasks": "Obter tarefas do Tarefas.MD"
        }
    }), 200


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Obter tarefas do arquivo Tarefas.MD via Task Manager Agent"""
    try:
        import sys
        sys.path.append(os.path.join(os.getcwd(), 'app'))
        
        from agents.specialized import TaskManagerAgent
        
        agent = TaskManagerAgent()
        report = agent.generate_task_report()
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({"error": str(e), "tasks": []}), 500


# ==========================================
# ROTAS DE IMPORTAÇÃO WEB
# ==========================================

@app.route('/api/import-web', methods=['POST'])
def import_web():
    """Importar e converter página web para Markdown"""
    try:
        from integrations import get_provider_status_summary
        
        data = request.json
        url = data.get('url')
        title = data.get('title', None)
        
        if not url:
            return jsonify({"error": "URL é obrigatória"}), 400
        
        importer = WebImporter()
        result = importer.import_and_save(url, title)
        
        return jsonify({
            "success": True,
            "filename": result['filename'],
            "title": result['title'],
            "path": result['path'],
            "size": result['size']
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Erro ao importar: {str(e)}"}), 500


@app.route('/api/imported-docs', methods=['GET'])
def get_imported_docs():
    """Listar documentos importados"""
    try:
        from integrations.web_importer import WebImporter
        
        importer = WebImporter()
        docs = importer.list_docs()
        
        return jsonify(docs), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ROTAS DE GERENCIAMENTO DE TAREFAS
# ==========================================

@app.route('/api/task', methods=['GET'])
def list_tasks():
    """Listar todas as tarefas"""
    try:
        # Ler do arquivo de histórico
        history_file = 'app/data/tasks.json'
        
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        else:
            tasks = []
        
        return jsonify({"tasks": tasks, "count": len(tasks)}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/task/<task_id>', methods=['GET'])
def get_task(task_id):
    """Obter detalhes de uma tarefa específica"""
    try:
        history_file = 'app/data/tasks.json'
        
        if not os.path.exists(history_file):
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        with open(history_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        return jsonify(task), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/task/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualizar status de uma tarefa"""
    try:
        data = request.json
        history_file = 'app/data/tasks.json'
        
        if not os.path.exists(history_file):
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        with open(history_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        task = next((t for t in tasks if t['id'] == task_id), None)
        
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404
        
        # Atualizar status
        if 'status' in data:
            task['status'] = data['status']
        if 'notes' in data:
            task['notes'] = data['notes']
        
        task['updated_at'] = datetime.now().isoformat()
        
        # Salvar
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        
        return jsonify(task), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Rota não encontrada"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
