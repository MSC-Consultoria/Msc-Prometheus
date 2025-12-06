#!/usr/bin/env python3
"""
Prometheus CLI - Interface de Linha de Comando para Agente Evolutivo

Uso:
    python cli.py task "Sua tarefa aqui"
    python cli.py stats
    python cli.py timeline [--limit 10]
    python cli.py knowledge [--format json|markdown]
    python cli.py search "termo"
    python cli.py help
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from tabulate import tabulate

# Adicionar o diretório ao path para importar o agente
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.evolutionary_agent import EvolutionaryAgent
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()


class PrometheusCLI:
    """Interface de linha de comando para o Agente Evolutivo"""
    
    def __init__(self):
        self.agent = EvolutionaryAgent(
            api_key=os.getenv('OPENAI_API_KEY'),
            model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        )
        self.colors = {
            'success': '\033[92m',
            'error': '\033[91m',
            'info': '\033[94m',
            'warning': '\033[93m',
            'reset': '\033[0m',
            'bold': '\033[1m'
        }
    
    def print_colored(self, message: str, color: str = 'info') -> None:
        """Imprimir mensagem com cor"""
        c = self.colors.get(color, '')
        reset = self.colors['reset']
        print(f"{c}{message}{reset}")
    
    def print_header(self, title: str) -> None:
        """Imprimir cabeçalho de seção"""
        self.print_colored(f"\n{'='*60}", 'bold')
        self.print_colored(f"  {title}", 'bold')
        self.print_colored(f"{'='*60}\n", 'bold')
    
    # ==================== COMANDOS ====================
    
    def cmd_task(self, description: str, context: Optional[str] = None, 
                 files_context: Optional[list] = None) -> None:
        """Processar uma nova tarefa"""
        self.print_header("🚀 PROCESSANDO TAREFA")
        
        self.print_colored("Tarefa:", 'info')
        print(f"  {description}\n")
        
        if context:
            self.print_colored("Contexto:", 'info')
            print(f"  {context}\n")
        
        self.print_colored("Processando...", 'warning')
        
        try:
            result = self.agent.process_task(
                task_description=description,
                context=context or '',
                files_context=files_context or []
            )
            
            self.print_colored("✓ Tarefa processada com sucesso!", 'success')
            
            self.print_colored("\n📋 RESPOSTA:", 'info')
            print(f"{result.get('response', 'Sem resposta')}\n")
            
            if result.get('learning_points'):
                self.print_colored("📚 Pontos de Aprendizado:", 'info')
                for point in result['learning_points']:
                    print(f"  • {point}")
            
            self.print_colored(f"\n⏱️  Tempo: {result.get('elapsed_time', 0):.2f}s", 'info')
            self.print_colored(f"📊 Evolução #{result.get('evolution_count', 0)}", 'info')
            
        except Exception as e:
            self.print_colored(f"✗ Erro ao processar tarefa: {str(e)}", 'error')
            sys.exit(1)
    
    def cmd_stats(self) -> None:
        """Mostrar estatísticas do agente"""
        self.print_header("📊 ESTATÍSTICAS DO AGENTE")
        
        try:
            stats = self.agent.get_stats()
            
            data = [
                ['Versão do Agente', stats.get('version', 'N/A')],
                ['Total de Tarefas', stats.get('total_tasks', 0)],
                ['Taxa de Sucesso', f"{stats.get('success_rate', 0):.1f}%"],
                ['Entradas de Conhecimento', stats.get('knowledge_entries', 0)],
                ['Tempo de Execução', f"{stats.get('total_time', 0):.2f}s"],
            ]
            
            print(tabulate(data, headers=['Métrica', 'Valor'], tablefmt='grid'))
            
        except Exception as e:
            self.print_colored(f"✗ Erro ao obter estatísticas: {str(e)}", 'error')
            sys.exit(1)
    
    def cmd_timeline(self, limit: int = 10) -> None:
        """Mostrar timeline de evolução"""
        self.print_header(f"📈 TIMELINE DE EVOLUÇÃO (Últimos {limit})")
        
        try:
            timeline = self.agent.get_evolution_timeline(limit=limit)
            
            if not timeline:
                self.print_colored("Nenhuma tarefa processada ainda.", 'warning')
                return
            
            data = []
            for i, item in enumerate(timeline, 1):
                timestamp = item.get('timestamp', 'N/A')
                task_desc = item.get('task_description', 'Sem descrição')[:40]
                status = item.get('status', 'unknown')
                
                data.append([
                    i,
                    timestamp,
                    task_desc,
                    status
                ])
            
            print(tabulate(data, 
                          headers=['#', 'Timestamp', 'Tarefa', 'Status'], 
                          tablefmt='grid'))
            
        except Exception as e:
            self.print_colored(f"✗ Erro ao obter timeline: {str(e)}", 'error')
            sys.exit(1)
    
    def cmd_knowledge(self, format_type: str = 'json') -> None:
        """Exportar base de conhecimento"""
        self.print_header("📚 BASE DE CONHECIMENTO")
        
        try:
            knowledge = self.agent.export_knowledge(format=format_type)
            
            if format_type == 'json':
                print(json.dumps(knowledge, indent=2, ensure_ascii=False))
            else:
                print(knowledge)
            
        except Exception as e:
            self.print_colored(f"✗ Erro ao exportar conhecimento: {str(e)}", 'error')
            sys.exit(1)
    
    def cmd_search(self, query: str) -> None:
        """Buscar na base de conhecimento"""
        self.print_header(f"🔍 BUSCANDO: '{query}'")
        
        try:
            knowledge = self.agent.export_knowledge(format='json')
            
            if isinstance(knowledge, str):
                knowledge = json.loads(knowledge)
            
            results = []
            
            # Buscar em learning_points
            if 'learning_base' in knowledge:
                for point in knowledge['learning_base']:
                    if query.lower() in point.lower():
                        results.append(('Learning Point', point))
            
            # Buscar em tasks
            if 'tasks' in knowledge:
                for task in knowledge['tasks']:
                    task_desc = task.get('task_description', '')
                    if query.lower() in task_desc.lower():
                        results.append(('Tarefa', task_desc[:50]))
            
            if results:
                self.print_colored(f"✓ Encontrado {len(results)} resultado(s):", 'success')
                for item_type, content in results:
                    print(f"\n  [{item_type}]")
                    print(f"  {content}")
            else:
                self.print_colored(f"Nenhum resultado encontrado para '{query}'", 'warning')
            
        except Exception as e:
            self.print_colored(f"✗ Erro ao buscar: {str(e)}", 'error')
            sys.exit(1)
    
    def cmd_help(self) -> None:
        """Mostrar ajuda de comandos"""
        help_text = """
╔════════════════════════════════════════════════════════════════╗
║        PROMETHEUS CLI - AGENTE EVOLUTIVO DE IA                 ║
╚════════════════════════════════════════════════════════════════╝

COMANDOS DISPONÍVEIS:

📝 task <descrição> [--context <contexto>]
   Processar uma nova tarefa
   Exemplo:
     python cli.py task "Crie um exemplo de Juniper"
     python cli.py task "Analise o código" --context "Python 3.11"

📊 stats
   Mostrar estatísticas do agente
   Exemplo:
     python cli.py stats

📈 timeline [--limit N]
   Mostrar timeline de evolução (últimas N tarefas)
   Exemplo:
     python cli.py timeline --limit 20

📚 knowledge [--format json|markdown]
   Exportar base de conhecimento
   Exemplo:
     python cli.py knowledge --format json
     python cli.py knowledge --format markdown

🔍 search <termo>
   Buscar na base de conhecimento
   Exemplo:
     python cli.py search "integração"

ℹ️  help
   Mostrar esta mensagem

═══════════════════════════════════════════════════════════════════

CONFIGURAÇÃO:
  • Criar arquivo .env na raiz do projeto
  • Adicionar: OPENAI_API_KEY=sua-chave-aqui
  • Adicionar: OPENAI_MODEL=gpt-4o-mini (ou gpt-4)

═══════════════════════════════════════════════════════════════════
"""
        print(help_text)
    
    def run(self, args: list) -> None:
        """Executar CLI com argumentos"""
        
        parser = argparse.ArgumentParser(
            prog='prometheus',
            description='CLI para Agente Evolutivo Prometheus'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
        
        # Comando: task
        task_parser = subparsers.add_parser('task', help='Processar tarefa')
        task_parser.add_argument('description', help='Descrição da tarefa')
        task_parser.add_argument('--context', '-c', help='Contexto da tarefa')
        
        # Comando: stats
        subparsers.add_parser('stats', help='Mostrar estatísticas')
        
        # Comando: timeline
        timeline_parser = subparsers.add_parser('timeline', help='Mostrar timeline')
        timeline_parser.add_argument('--limit', '-l', type=int, default=10, 
                                     help='Número de itens (padrão: 10)')
        
        # Comando: knowledge
        knowledge_parser = subparsers.add_parser('knowledge', help='Exportar conhecimento')
        knowledge_parser.add_argument('--format', '-f', choices=['json', 'markdown'], 
                                      default='json', help='Formato de saída')
        
        # Comando: search
        search_parser = subparsers.add_parser('search', help='Buscar conhecimento')
        search_parser.add_argument('query', help='Termo a buscar')
        
        # Comando: help
        subparsers.add_parser('help', help='Mostrar ajuda')
        
        # Parse dos argumentos
        if not args or args[0] == 'help':
            self.cmd_help()
            return
        
        parsed = parser.parse_args(args)
        
        # Executar comando apropriado
        if parsed.command == 'task':
            self.cmd_task(parsed.description, parsed.context)
        elif parsed.command == 'stats':
            self.cmd_stats()
        elif parsed.command == 'timeline':
            self.cmd_timeline(parsed.limit)
        elif parsed.command == 'knowledge':
            self.cmd_knowledge(parsed.format)
        elif parsed.command == 'search':
            self.cmd_search(parsed.query)
        elif parsed.command == 'help':
            self.cmd_help()
        else:
            self.cmd_help()


def main():
    """Ponto de entrada da CLI"""
    cli = PrometheusCLI()
    cli.run(sys.argv[1:])


if __name__ == '__main__':
    main()
