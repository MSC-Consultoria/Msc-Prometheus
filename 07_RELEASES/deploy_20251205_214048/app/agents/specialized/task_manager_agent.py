"""
Agente Especializado: Gerenciador de Tarefas
Monitora e processa o arquivo Tarefas.MD
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional


class TaskManagerAgent:
    """
    Agente responsável por ler, interpretar e gerenciar tarefas do Tarefas.MD
    """
    
    def __init__(self, tasks_file: str = "Tarefas.MD"):
        self.tasks_file = tasks_file
        self.tasks_history = []
        
    def read_tasks(self) -> str:
        """Ler conteúdo do arquivo Tarefas.MD"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return f.read()
            return ""
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"
    
    def parse_tasks(self, content: str) -> List[Dict]:
        """
        Extrair tarefas individuais do conteúdo
        Identifica linhas que representam tarefas/diretrizes
        """
        tasks = []
        lines = content.split('\n')
        
        for idx, line in enumerate(lines, 1):
            line = line.strip()
            
            # Identificar tarefas (linhas com ; no final ou com verbos de ação)
            if line and (line.endswith(';') or self._is_action_line(line)):
                tasks.append({
                    'line_number': idx,
                    'content': line.rstrip(';'),
                    'type': self._classify_task(line),
                    'priority': self._estimate_priority(line),
                    'status': 'pending'
                })
        
        return tasks
    
    def _is_action_line(self, line: str) -> bool:
        """Verificar se linha contém verbo de ação (imperativo)"""
        action_verbs = [
            'criar', 'fazer', 'implementar', 'desenvolver', 'configurar',
            'usar', 'integrar', 'buscar', 'verificar', 'validar', 'consolidar',
            'sugerir', 'listar', 'começar', 'trabalhar', 'focar', 'mover',
            'limpar', 'trazer', 'instalar', 'sinaliza', 'presar', 'vamos'
        ]
        
        line_lower = line.lower()
        return any(verb in line_lower for verb in action_verbs)
    
    def _classify_task(self, line: str) -> str:
        """Classificar tipo de tarefa"""
        line_lower = line.lower()
        
        if any(word in line_lower for word in ['integr', 'api', 'cli', 'llm']):
            return 'integration'
        elif any(word in line_lower for word in ['criar', 'desenvolv', 'implement']):
            return 'development'
        elif any(word in line_lower for word in ['consolid', 'organiz', 'limpar', 'mover']):
            return 'organization'
        elif any(word in line_lower for word in ['config', 'setup', 'install']):
            return 'configuration'
        elif any(word in line_lower for word in ['document', 'base de conhec', 'anot']):
            return 'documentation'
        else:
            return 'general'
    
    def _estimate_priority(self, line: str) -> str:
        """Estimar prioridade da tarefa"""
        line_lower = line.lower()
        
        # Alta prioridade
        if any(word in line_lower for word in ['urgente', 'imediato', 'crítico', 'agora', 'focar']):
            return 'high'
        # Média prioridade
        elif any(word in line_lower for word in ['importante', 'necessário', 'deve']):
            return 'medium'
        # Baixa prioridade
        elif any(word in line_lower for word in ['futuro', 'eventual', 'pode']):
            return 'low'
        else:
            return 'medium'
    
    def get_pending_tasks(self) -> List[Dict]:
        """Obter lista de tarefas pendentes"""
        content = self.read_tasks()
        return self.parse_tasks(content)
    
    def get_tasks_by_type(self, task_type: str) -> List[Dict]:
        """Filtrar tarefas por tipo"""
        all_tasks = self.get_pending_tasks()
        return [t for t in all_tasks if t['type'] == task_type]
    
    def get_tasks_by_priority(self, priority: str) -> List[Dict]:
        """Filtrar tarefas por prioridade"""
        all_tasks = self.get_pending_tasks()
        return [t for t in all_tasks if t['priority'] == priority]
    
    def archive_completed_tasks(self) -> bool:
        """
        Mover tarefas concluídas para arquivo histórico
        """
        try:
            content = self.read_tasks()
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            archive_dir = "04_OPERACIONAL/Rascunhos"
            os.makedirs(archive_dir, exist_ok=True)
            
            archive_file = os.path.join(archive_dir, f"Tarefas_Arquivadas_{timestamp}.md")
            
            with open(archive_file, 'w', encoding='utf-8') as f:
                f.write(f"# Tarefas Arquivadas\n\n")
                f.write(f"**Data de Arquivamento:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Erro ao arquivar tarefas: {e}")
            return False
    
    def generate_task_report(self) -> Dict:
        """Gerar relatório de tarefas"""
        tasks = self.get_pending_tasks()
        
        report = {
            'total': len(tasks),
            'by_type': {},
            'by_priority': {},
            'tasks': tasks
        }
        
        # Contar por tipo
        for task in tasks:
            task_type = task['type']
            report['by_type'][task_type] = report['by_type'].get(task_type, 0) + 1
        
        # Contar por prioridade
        for task in tasks:
            priority = task['priority']
            report['by_priority'][priority] = report['by_priority'].get(priority, 0) + 1
        
        return report
    
    def get_next_action(self) -> Optional[Dict]:
        """
        Retornar próxima ação recomendada baseada em prioridade
        """
        tasks = self.get_pending_tasks()
        
        if not tasks:
            return None
        
        # Priorizar: high > medium > low
        high_priority = [t for t in tasks if t['priority'] == 'high']
        if high_priority:
            return high_priority[0]
        
        medium_priority = [t for t in tasks if t['priority'] == 'medium']
        if medium_priority:
            return medium_priority[0]
        
        return tasks[0]


# ==========================================
# EXEMPLO DE USO
# ==========================================

if __name__ == "__main__":
    agent = TaskManagerAgent()
    
    print("=" * 60)
    print("TASK MANAGER AGENT - RELATÓRIO")
    print("=" * 60)
    
    # Gerar relatório
    report = agent.generate_task_report()
    
    print(f"\n📊 Total de Tarefas: {report['total']}")
    
    print("\n📋 Por Tipo:")
    for task_type, count in report['by_type'].items():
        print(f"  • {task_type}: {count}")
    
    print("\n⚡ Por Prioridade:")
    for priority, count in report['by_priority'].items():
        print(f"  • {priority}: {count}")
    
    # Próxima ação recomendada
    next_action = agent.get_next_action()
    if next_action:
        print(f"\n🎯 Próxima Ação Recomendada:")
        print(f"  Tipo: {next_action['type']}")
        print(f"  Prioridade: {next_action['priority']}")
        print(f"  Tarefa: {next_action['content']}")
