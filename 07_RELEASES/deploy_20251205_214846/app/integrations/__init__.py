"""
Integrações - Módulo de integrações externas
Integração com Google, importação web, etc.
"""

from .web_importer import WebImporter
from .api_clients import API_CREDENTIALS, get_provider_status_summary

__all__ = ['WebImporter', 'API_CREDENTIALS', 'get_provider_status_summary']
