"""
Prometheus - Sistema de Agentes Evolutivos
Pacote principal da aplicação
"""

__version__ = "1.0.0"
__author__ = "Prometheus Team"
__description__ = "Sistema de agentes evolutivos que aprendem através de documentação estruturada"

from .app.agents.evolutionary_agent import EvolutionaryAgent

__all__ = ['EvolutionaryAgent']
