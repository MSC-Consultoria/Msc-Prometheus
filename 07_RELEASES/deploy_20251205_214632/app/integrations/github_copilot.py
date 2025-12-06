"""
GitHub Copilot Integration Module
Integração com GitHub API para monitorar rate limits e uso do Copilot

This module provides:
- GitHub API rate limit monitoring
- Copilot usage tracking (requires Copilot Business/Enterprise)
- Authentication via GitHub Personal Access Token
"""

import os
import requests
from typing import Dict, Optional
from datetime import datetime


class GitHubCopilotClient:
    """
    Cliente para integração com GitHub API e Copilot
    
    Funcionalidades:
    - Monitoramento de rate limits da API do GitHub
    - Tracking de uso do Copilot (quando disponível)
    - Informações sobre quotas e limites
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Inicializa o cliente do GitHub
        
        Args:
            token: GitHub Personal Access Token. Se não fornecido, busca GITHUB_TOKEN do .env
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        
        if not self.token:
            print("⚠️ GITHUB_TOKEN não configurado. Configure no arquivo .env")
    
    def _get_headers(self) -> Dict[str, str]:
        """Retorna headers com autenticação"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    
    def get_rate_limits(self) -> Dict:
        """
        Obtém informações sobre rate limits da API do GitHub
        
        Returns:
            dict: Rate limit information including:
                - core: General API calls
                - search: Search API calls
                - graphql: GraphQL API calls
                - integration_manifest: Integration manifest API calls
                - code_scanning_upload: Code scanning upload API calls
        
        Exemplo de resposta:
        {
            "status": "success",
            "timestamp": "2025-12-05T10:30:00",
            "rate": {
                "limit": 5000,
                "remaining": 4999,
                "reset": 1733396400,
                "used": 1
            },
            "resources": {
                "core": {...},
                "search": {...},
                "graphql": {...}
            }
        }
        """
        if not self.token:
            return {
                "status": "error",
                "error": "GITHUB_TOKEN não configurado",
                "message": "Configure GITHUB_TOKEN no arquivo .env"
            }
        
        try:
            url = f"{self.base_url}/rate_limit"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "rate": data.get("rate"),
                    "resources": data.get("resources"),
                    "message": "Rate limits obtidos com sucesso"
                }
            
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "error": "Unauthorized",
                    "message": "Token do GitHub inválido ou expirado"
                }
            
            elif response.status_code == 403:
                return {
                    "status": "error",
                    "error": "Forbidden",
                    "message": "Token sem permissões necessárias"
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
                "message": "GitHub API não respondeu em 10 segundos"
            }
        
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "error": "Connection Error",
                "message": "Não foi possível conectar ao GitHub API"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": type(e).__name__,
                "message": str(e)
            }
    
    def get_user_info(self) -> Dict:
        """
        Obtém informações sobre o usuário autenticado
        
        Returns:
            dict: User information including login, name, email, plan
        """
        if not self.token:
            return {
                "status": "error",
                "error": "Token não configurado"
            }
        
        try:
            url = f"{self.base_url}/user"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    "status": "success",
                    "login": data.get("login"),
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "plan": data.get("plan", {}).get("name"),
                    "created_at": data.get("created_at"),
                    "message": "Informações do usuário obtidas com sucesso"
                }
            
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": type(e).__name__,
                "message": str(e)
            }
    
    def get_copilot_usage(self) -> Dict:
        """
        Obtém informações sobre uso do GitHub Copilot
        
        Note: This requires GitHub Copilot Business or Enterprise
        
        Returns:
            dict: Copilot usage information
        """
        if not self.token:
            return {
                "status": "error",
                "error": "Token não configurado"
            }
        
        try:
            # Note: Este endpoint pode não estar disponível para todos os planos
            # Requer Copilot Business ou Enterprise
            url = f"{self.base_url}/copilot/usage"
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    "status": "success",
                    "timestamp": datetime.now().isoformat(),
                    "usage": data,
                    "message": "Uso do Copilot obtido com sucesso"
                }
            
            elif response.status_code == 404:
                return {
                    "status": "not_available",
                    "message": "Copilot usage API não disponível. Requer Copilot Business/Enterprise."
                }
            
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "message": response.text
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": type(e).__name__,
                "message": str(e)
            }
    
    def check_status(self) -> Dict:
        """
        Verifica o status geral da integração com GitHub
        
        Returns:
            dict: Status completo incluindo conectividade, autenticação, rate limits
        """
        if not self.token:
            return {
                "status": "not_configured",
                "authenticated": False,
                "message": "GITHUB_TOKEN não configurado"
            }
        
        # Tenta obter rate limits para validar o token
        rate_limits = self.get_rate_limits()
        
        if rate_limits.get("status") == "success":
            user_info = self.get_user_info()
            
            return {
                "status": "connected",
                "authenticated": True,
                "user": user_info.get("login", "Unknown"),
                "plan": user_info.get("plan", "Unknown"),
                "rate_limit_remaining": rate_limits.get("rate", {}).get("remaining", 0),
                "rate_limit_total": rate_limits.get("rate", {}).get("limit", 0),
                "message": "Conectado ao GitHub com sucesso"
            }
        
        else:
            return {
                "status": "error",
                "authenticated": False,
                "error": rate_limits.get("error"),
                "message": rate_limits.get("message")
            }


# Instância global para uso fácil
github_client = GitHubCopilotClient()


# Funções de conveniência
def get_rate_limits() -> Dict:
    """Atalho para obter rate limits"""
    return github_client.get_rate_limits()


def check_github_status() -> Dict:
    """Atalho para verificar status do GitHub"""
    return github_client.check_status()


def get_copilot_usage() -> Dict:
    """Atalho para obter uso do Copilot"""
    return github_client.get_copilot_usage()


if __name__ == "__main__":
    # Teste rápido do módulo
    print("🔍 Testando GitHub Copilot Integration...")
    print()
    
    status = check_github_status()
    print("📊 Status:", status)
    print()
    
    if status.get("authenticated"):
        print("✅ Autenticado com sucesso!")
        print(f"👤 Usuário: {status.get('user')}")
        print(f"📦 Plano: {status.get('plan')}")
        print(f"🔢 Rate Limit: {status.get('rate_limit_remaining')}/{status.get('rate_limit_total')}")
    else:
        print("❌ Não autenticado")
        print(f"💡 Mensagem: {status.get('message')}")
