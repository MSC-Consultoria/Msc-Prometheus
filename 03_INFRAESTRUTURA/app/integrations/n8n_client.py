"""
N8N Workflow Automation Integration
Integração com N8N para automação de workflows e orquestração de tarefas

This module provides:
- Bidirectional communication with N8N workflows
- Webhook signature validation for security
- Task result distribution to N8N
- Workflow triggering from Prometheus
"""

import os
import hmac
import hashlib
import requests
from typing import Dict, Optional, Any
from datetime import datetime
import json


class N8NClient:
    """
    Cliente para integração com N8N Workflow Automation
    
    Funcionalidades:
    - Enviar resultados de tarefas para workflows N8N
    - Triggerar workflows específicos
    - Validar webhooks recebidos do N8N (segurança)
    - Orquestração de multi-tool workflows
    """
    
    def __init__(self, webhook_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Inicializa o cliente do N8N
        
        Args:
            webhook_url: URL base do N8N webhook. Se não fornecido, busca N8N_WEBHOOK_URL do .env
            api_key: API key para autenticação. Se não fornecido, busca N8N_API_KEY do .env
        """
        self.webhook_url = webhook_url or os.getenv("N8N_WEBHOOK_URL")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        self.webhook_secret = os.getenv("N8N_WEBHOOK_SECRET")  # For signature validation
        
        if not self.webhook_url:
            print("⚠️ N8N_WEBHOOK_URL não configurado. Configure no arquivo .env")
        
        if not self.api_key:
            print("⚠️ N8N_API_KEY não configurado. Configure no arquivo .env")
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com autenticação"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if self.api_key:
            headers["X-N8N-API-KEY"] = self.api_key
        
        return headers
    
    def trigger_workflow(self, workflow_id: str, data: Dict[str, Any], wait: bool = False) -> Dict:
        """
        Trigga um workflow específico no N8N
        
        Args:
            workflow_id: ID ou nome do workflow no N8N
            data: Dados a serem enviados para o workflow
            wait: Se True, aguarda a execução completa do workflow
        
        Returns:
            dict: Resposta do N8N incluindo execution_id e status
        
        Exemplo:
            result = client.trigger_workflow("task-completed", {
                "task_id": "task_123",
                "status": "success",
                "result": "Task completed successfully"
            })
        """
        if not self.webhook_url:
            return {
                "status": "error",
                "error": "N8N_WEBHOOK_URL não configurado",
                "message": "Configure N8N_WEBHOOK_URL no arquivo .env"
            }
        
        try:
            # Constrói a URL do webhook
            url = f"{self.webhook_url}/{workflow_id}"
            
            # Adiciona parâmetros de query se necessário
            params = {}
            if wait:
                params["wait"] = "true"
            
            # Adiciona metadados
            payload = {
                "data": data,
                "metadata": {
                    "source": "prometheus",
                    "timestamp": datetime.now().isoformat(),
                    "workflow_id": workflow_id
                }
            }
            
            response = requests.post(
                url,
                json=payload,
                headers=self._get_headers(),
                params=params,
                timeout=30 if wait else 10
            )
            
            if response.status_code in [200, 201]:
                result = response.json() if response.text else {}
                
                return {
                    "status": "success",
                    "execution_id": result.get("executionId"),
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat(),
                    "data": result,
                    "message": f"Workflow '{workflow_id}' trigado com sucesso"
                }
            
            elif response.status_code == 404:
                return {
                    "status": "error",
                    "error": "Workflow não encontrado",
                    "message": f"Workflow '{workflow_id}' não existe no N8N"
                }
            
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "error": "Unauthorized",
                    "message": "N8N API key inválida ou ausente"
                }
            
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }
        
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error": "Timeout",
                "message": f"N8N não respondeu em {'30' if wait else '10'} segundos"
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "error": "Connection Error",
                "message": "Não foi possível conectar ao N8N"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": type(e).__name__,
                "message": str(e)
            }
    
    def send_task_result(self, task_id: str, result: Dict[str, Any]) -> Dict:
        """
        Envia resultado de uma tarefa processada para o N8N
        
        Args:
            task_id: ID da tarefa processada
            result: Resultado completo do processamento
        
        Returns:
            dict: Confirmação do envio
        
        Exemplo de uso:
            client.send_task_result("task_123", {
                "status": "success",
                "response": "Tarefa concluída",
                "elapsed_time": 2.5
            })
        """
        return self.trigger_workflow("task-completed", {
            "task_id": task_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    def send_notification(self, message: str, channel: str = "general", level: str = "info") -> Dict:
        """
        Envia notificação através do N8N
        
        Args:
            message: Mensagem a ser enviada
            channel: Canal de notificação (email, slack, discord, etc.)
            level: Nível de importância (info, warning, error, success)
        
        Returns:
            dict: Confirmação do envio
        
        Exemplo:
            client.send_notification(
                "Nova tarefa completada!",
                channel="slack",
                level="success"
            )
        """
        return self.trigger_workflow("send-notification", {
            "message": message,
            "channel": channel,
            "level": level,
            "timestamp": datetime.now().isoformat()
        })
    
    def validate_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Valida assinatura de webhook recebido do N8N
        
        Args:
            payload: Body do request em bytes
            signature: Assinatura recebida no header (X-N8N-Signature)
        
        Returns:
            bool: True se assinatura válida, False caso contrário
        
        Segurança:
            Use isso para validar que o webhook realmente veio do N8N
        """
        if not self.webhook_secret:
            print("⚠️ N8N_WEBHOOK_SECRET não configurado. Validação de assinatura desabilitada.")
            return True  # Se não tem secret configurado, aceita qualquer request
        
        try:
            # Calcula HMAC-SHA256
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            # Compara de forma segura (timing-safe)
            return hmac.compare_digest(expected_signature, signature)
        
        except Exception as e:
            print(f"❌ Erro ao validar assinatura: {e}")
            return False
    
    def send_agent_evolution(self, evolution_data: Dict[str, Any]) -> Dict:
        """
        Envia dados de evolução do agente para N8N arquivar/processar
        
        Args:
            evolution_data: Dados de evolução incluindo learning points
        
        Returns:
            dict: Confirmação do envio
        """
        return self.trigger_workflow("agent-evolution", evolution_data)
    
    def request_scheduled_task(self, task_description: str, schedule: str) -> Dict:
        """
        Solicita que N8N agende uma tarefa para execução futura
        
        Args:
            task_description: Descrição da tarefa
            schedule: Cron expression ou data/hora (ISO format)
        
        Returns:
            dict: Confirmação do agendamento
        
        Exemplo:
            client.request_scheduled_task(
                "Gerar relatório diário",
                schedule="0 9 * * *"  # Todo dia às 9h
            )
        """
        return self.trigger_workflow("schedule-task", {
            "task_description": task_description,
            "schedule": schedule,
            "requested_by": "prometheus",
            "timestamp": datetime.now().isoformat()
        })
    
    def check_status(self) -> Dict:
        """
        Verifica o status da conexão com N8N
        
        Returns:
            dict: Status da integração
        """
        if not self.webhook_url:
            return {
                "status": "not_configured",
                "connected": False,
                "message": "N8N_WEBHOOK_URL não configurado"
            }
        
        try:
            # Tenta fazer uma requisição de health check
            # Nota: Isso depende de você ter um workflow "health-check" no N8N
            result = self.trigger_workflow("health-check", {"ping": "pong"})
            
            if result.get("status") == "success":
                return {
                    "status": "connected",
                    "connected": True,
                    "webhook_url": self.webhook_url,
                    "api_key_configured": bool(self.api_key),
                    "webhook_secret_configured": bool(self.webhook_secret),
                    "message": "Conectado ao N8N com sucesso"
                }
            else:
                return {
                    "status": "error",
                    "connected": False,
                    "error": result.get("error"),
                    "message": result.get("message")
                }
        
        except Exception as e:
            return {
                "status": "error",
                "connected": False,
                "error": type(e).__name__,
                "message": str(e)
            }


# Instância global para uso fácil
n8n_client = N8NClient()


# Funções de conveniência
def trigger_workflow(workflow_id: str, data: Dict) -> Dict:
    """Atalho para triggar um workflow"""
    return n8n_client.trigger_workflow(workflow_id, data)


def send_task_result(task_id: str, result: Dict) -> Dict:
    """Atalho para enviar resultado de tarefa"""
    return n8n_client.send_task_result(task_id, result)


def send_notification(message: str, channel: str = "general", level: str = "info") -> Dict:
    """Atalho para enviar notificação"""
    return n8n_client.send_notification(message, channel, level)


def check_n8n_status() -> Dict:
    """Atalho para verificar status do N8N"""
    return n8n_client.check_status()


if __name__ == "__main__":
    # Teste rápido do módulo
    print("🔍 Testando N8N Integration...")
    print()
    
    status = check_n8n_status()
    print("📊 Status:", status)
    print()
    
    if status.get("connected"):
        print("✅ Conectado ao N8N!")
        print(f"🔗 Webhook URL: {status.get('webhook_url')}")
        print(f"🔑 API Key: {'Configurada' if status.get('api_key_configured') else 'Não configurada'}")
        print(f"🔐 Webhook Secret: {'Configurado' if status.get('webhook_secret_configured') else 'Não configurado'}")
    else:
        print("❌ Não conectado")
        print(f"💡 Mensagem: {status.get('message')}")
