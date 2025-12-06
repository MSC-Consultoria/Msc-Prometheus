"""
Gerenciamento de credenciais e integrações externas.
Permite configurar múltiplas APIs (OpenAI, Gemini, Manus, Hugging Face) a partir de variáveis de ambiente
sem expor chaves em código-fonte.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

PROVIDER_METADATA = {
    "openai": {
        "label": "OpenAI",
        "endpoint": "https://api.openai.com/v1/",
        "hint": "OPENAI_API_KEY",
    },
    "gemini": {
        "label": "Gemini",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/",
        "hint": "GEMINI_API_KEY",
    },
    "manus": {
        "label": "Manus AI",
        "endpoint": "https://api.manus.ai/v1/",
        "hint": "MANUS_API_KEY",
    },
    "huggingface": {
        "label": "Hugging Face",
        "endpoint": "https://api-inference.huggingface.co/models/",
        "hint": "HUGGINGFACE_API_KEY",
    },
    "deepseek": {
        "label": "DeepSeek",
        "endpoint": "https://api.deepseek.com/v1/",
        "hint": "DEEPSEEK_API_KEY",
    },
    "openrouter": {
        "label": "OpenRouter",
        "endpoint": "https://openrouter.ai/api/v1/",
        "hint": "OPENROUTER_API_KEY",
    },
    "anthropic": {
        "label": "Anthropic Claude",
        "endpoint": "https://api.anthropic.com/v1/",
        "hint": "ANTHROPIC_API_KEY",
    },
    "github": {
        "label": "GitHub API",
        "endpoint": "https://api.github.com",
        "hint": "GITHUB_TOKEN",
    },
    "n8n": {
        "label": "N8N Workflow Automation",
        "endpoint": "N8N_WEBHOOK_URL",
        "hint": "N8N_WEBHOOK_URL e N8N_API_KEY",
    },
}


@dataclass
class ApiCredentials:
    """Agrupa as chaves usadas pelos provedores do Prometheus."""

    openai: str = os.getenv("OPENAI_API_KEY", "")
    gemini: str = os.getenv("GEMINI_API_KEY", "")
    manus: str = os.getenv("MANUS_API_KEY", "")
    huggingface: str = os.getenv("HUGGINGFACE_API_KEY", "")
    deepseek: str = os.getenv("DEEPSEEK_API_KEY", "")
    openrouter: str = os.getenv("OPENROUTER_API_KEY", "")
    anthropic: str = os.getenv("ANTHROPIC_API_KEY", "")
    github: str = os.getenv("GITHUB_TOKEN", "")
    n8n_webhook: str = os.getenv("N8N_WEBHOOK_URL", "")
    n8n_api: str = os.getenv("N8N_API_KEY", "")

    def __post_init__(self):
        self._keys = {
            "openai": self.openai,
            "gemini": self.gemini,
            "manus": self.manus,
            "huggingface": self.huggingface,
            "deepseek": self.deepseek,
            "openrouter": self.openrouter,
            "anthropic": self.anthropic,
            "github": self.github,
            "n8n": self.n8n_webhook,  # Considera configurado se webhook URL existe
        }

    def status(self) -> Dict[str, Dict[str, Any]]:
        """Retorna o status de cada provedor sem expor as chaves."""
        return {
            name: {
                "label": PROVIDER_METADATA[name]["label"],
                "endpoint": PROVIDER_METADATA[name]["endpoint"],
                "configured": bool(value),
                "hint": PROVIDER_METADATA[name]["hint"],
            }
            for name, value in self._keys.items()
        }

    def missing(self) -> Dict[str, str]:
        """Retorna os provedores que ainda não foram configurados"""
        missing = {}
        for name, value in self._keys.items():
            if not value:
                missing[name] = PROVIDER_METADATA[name]["hint"]
        return missing

    def provider_headers(self, provider: str, prefix: str = "Bearer") -> Dict[str, str]:
        """Cabeçalhos básicos para usar quando a API exige Authorization Bearer."""
        if provider not in self._keys:
            raise ValueError(f"Provedor desconhecido: {provider}")

        token = self._keys[provider]
        if not token:
            raise EnvironmentError(f"Chave para '{provider}' não definida. Veja {PROVIDER_METADATA[provider]['hint']}")
        return {"Authorization": f"{prefix} {token}"}


API_CREDENTIALS = ApiCredentials()


def get_provider_status_summary() -> Dict[str, Dict[str, Any]]:
    """Convenience helper usada pela API para mostrar status no frontend."""
    return API_CREDENTIALS.status()
