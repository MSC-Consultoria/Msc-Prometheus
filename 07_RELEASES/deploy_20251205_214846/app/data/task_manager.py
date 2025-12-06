"""
Task Manager - Gerenciador de Tarefas do Prometheus
Mantém histórico e controle de todas as tarefas criadas
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import uuid


class TaskManager:
    """Gerenciar tarefas criadas no frontend"""
    
    def __init__(self, storage_dir: str = None):
        """
        Inicializar gerenciador de tarefas
        
        Args:
            storage_dir: Diretório para armazenar tarefas
        """
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / 'data' / 'tasks'
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.storage_dir / 'tasks.json'
        self._load_tasks()
    
    def _load_tasks(self):
        """Carregar tarefas do arquivo"""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
    
    def _save_tasks(self):
        """Salvar tarefas no arquivo"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def create_task(self, title: str, description: str, priority: str = 'media',
                   category: str = 'outro', deadline: Optional[str] = None) -> Dict:
        """
        Criar nova tarefa
        
        Args:
            title: Título da tarefa
            description: Descrição detalhada
            priority: Prioridade (baixa, media, alta, urgente)
            category: Categoria (frontend, backend, integração, etc)
            deadline: Data limite (opcional)
            
        Returns:
            Dict com dados da tarefa criada
        """
        task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'priority': priority,
            'category': category,
            'deadline': deadline,
            'status': 'pendente',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'notes': '',
            'subtasks': []
        }
        
        self.tasks.append(task)
        self._save_tasks()
        
        return task
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Obter tarefa por ID
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            Dict com dados da tarefa ou None
        """
        return next((t for t in self.tasks if t['id'] == task_id), None)
    
    def list_tasks(self, status: Optional[str] = None, 
                  category: Optional[str] = None,
                  priority: Optional[str] = None) -> List[Dict]:
        """
        Listar tarefas com filtros opcionais
        
        Args:
            status: Filtrar por status
            category: Filtrar por categoria
            priority: Filtrar por prioridade
            
        Returns:
            Lista de tarefas
        """
        tasks = self.tasks
        
        if status:
            tasks = [t for t in tasks if t['status'] == status]
        if category:
            tasks = [t for t in tasks if t['category'] == category]
        if priority:
            tasks = [t for t in tasks if t['priority'] == priority]
        
        # Ordenar por prioridade (urgente > alta > media > baixa)
        priority_order = {'urgente': 0, 'alta': 1, 'media': 2, 'baixa': 3}
        tasks.sort(key=lambda t: priority_order.get(t['priority'], 4))
        
        return tasks
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Dict]:
        """
        Atualizar tarefa
        
        Args:
            task_id: ID da tarefa
            **kwargs: Campos a atualizar (status, notes, etc)
            
        Returns:
            Dict com tarefa atualizada ou None
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        # Atualizar campos permitidos
        allowed_fields = {'status', 'notes', 'deadline', 'priority', 'category'}
        for key, value in kwargs.items():
            if key in allowed_fields:
                task[key] = value
        
        task['updated_at'] = datetime.now().isoformat()
        self._save_tasks()
        
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """
        Deletar tarefa
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            True se deletado, False se não encontrado
        """
        original_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        
        if len(self.tasks) < original_len:
            self._save_tasks()
            return True
        return False
    
    def add_subtask(self, task_id: str, subtask_title: str) -> Optional[Dict]:
        """
        Adicionar subtarefa
        
        Args:
            task_id: ID da tarefa pai
            subtask_title: Título da subtarefa
            
        Returns:
            Dict com subtarefa adicionada ou None
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        subtask = {
            'id': str(uuid.uuid4()),
            'title': subtask_title,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        
        task['subtasks'].append(subtask)
        self._save_tasks()
        
        return subtask
    
    def toggle_subtask(self, task_id: str, subtask_id: str) -> bool:
        """
        Marcar/desmarcar subtarefa como completa
        
        Args:
            task_id: ID da tarefa pai
            subtask_id: ID da subtarefa
            
        Returns:
            True se toggled, False se não encontrado
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        subtask = next((s for s in task['subtasks'] if s['id'] == subtask_id), None)
        if not subtask:
            return False
        
        subtask['completed'] = not subtask['completed']
        self._save_tasks()
        
        return True
    
    def get_stats(self) -> Dict:
        """
        Obter estatísticas das tarefas
        
        Returns:
            Dict com estatísticas
        """
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t['status'] == 'completa'])
        pending = len([t for t in self.tasks if t['status'] == 'pendente'])
        in_progress = len([t for t in self.tasks if t['status'] == 'em_progresso'])
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 1),
            'by_priority': {
                'urgente': len([t for t in self.tasks if t['priority'] == 'urgente']),
                'alta': len([t for t in self.tasks if t['priority'] == 'alta']),
                'media': len([t for t in self.tasks if t['priority'] == 'media']),
                'baixa': len([t for t in self.tasks if t['priority'] == 'baixa'])
            },
            'by_category': {}
        }
    
    def export_to_markdown(self) -> str:
        """
        Exportar tarefas como Markdown
        
        Returns:
            String com formatação Markdown
        """
        md = "# 📋 Tarefas do Prometheus\n\n"
        md += f"**Exportado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        stats = self.get_stats()
        md += f"## 📊 Estatísticas\n\n"
        md += f"- **Total de Tarefas:** {stats['total']}\n"
        md += f"- **Completas:** {stats['completed']}\n"
        md += f"- **Em Progresso:** {stats['in_progress']}\n"
        md += f"- **Pendentes:** {stats['pending']}\n"
        md += f"- **Taxa de Conclusão:** {stats['completion_rate']}%\n\n"
        
        # Agrupar por status
        for status in ['completa', 'em_progresso', 'pendente']:
            tasks_by_status = self.list_tasks(status=status)
            if tasks_by_status:
                status_emoji = {'completa': '✅', 'em_progresso': '🔄', 'pendente': '⏳'}
                md += f"## {status_emoji.get(status, '•')} {status.title()}\n\n"
                
                for task in tasks_by_status:
                    md += f"### {task['title']}\n"
                    md += f"- **Descrição:** {task['description']}\n"
                    md += f"- **Prioridade:** {task['priority']}\n"
                    md += f"- **Categoria:** {task['category']}\n"
                    md += f"- **Criada em:** {task['created_at']}\n"
                    
                    if task['deadline']:
                        md += f"- **Prazo:** {task['deadline']}\n"
                    
                    if task['notes']:
                        md += f"- **Notas:** {task['notes']}\n"
                    
                    if task['subtasks']:
                        md += f"\n**Subtarefas:**\n"
                        for subtask in task['subtasks']:
                            status_mark = "✓" if subtask['completed'] else "✗"
                            md += f"- [{status_mark}] {subtask['title']}\n"
                    
                    md += "\n"
        
        return md


# ==========================================
# EXEMPLO DE USO
# ==========================================

if __name__ == '__main__':
    manager = TaskManager()
    
    # Criar tarefa
    task = manager.create_task(
        title="Implementar banco de dados",
        description="Migrar de JSON para PostgreSQL",
        priority="alta",
        category="backend",
        deadline="2025-12-15"
    )
    
    print(f"✅ Tarefa criada: {task['id']}")
    
    # Listar tarefas
    tasks = manager.list_tasks()
    print(f"\n📋 {len(tasks)} tarefas no total")
    
    # Exportar para markdown
    md = manager.export_to_markdown()
    print("\n📄 Exportado para Markdown")
