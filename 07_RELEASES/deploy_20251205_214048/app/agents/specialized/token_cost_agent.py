"""
Agente Especializado: Analisador de Custos de Tokens
Calcula e rastreia custos de uso de APIs de LLM
"""

from typing import Dict, List, Optional
from datetime import datetime
import json
import os


class TokenCostAgent:
    """
    Agente responsável por calcular custos de tokens e gerar relatórios
    """
    
    # Preços por 1M tokens (atualizado em Dezembro 2025)
    PRICING = {
        'openai': {
            'gpt-4-turbo': {'input': 10.00, 'output': 30.00},
            'gpt-4': {'input': 30.00, 'output': 60.00},
            'gpt-3.5-turbo': {'input': 0.50, 'output': 1.50},
            'gpt-4o': {'input': 5.00, 'output': 15.00},
            'gpt-4o-mini': {'input': 0.15, 'output': 0.60}
        },
        'anthropic': {
            'claude-3-opus': {'input': 15.00, 'output': 75.00},
            'claude-3-sonnet': {'input': 3.00, 'output': 15.00},
            'claude-3-haiku': {'input': 0.25, 'output': 1.25},
            'claude-3.5-sonnet': {'input': 3.00, 'output': 15.00}
        },
        'deepseek': {
            'deepseek-chat': {'input': 0.14, 'output': 0.28},
            'deepseek-coder': {'input': 0.14, 'output': 0.28}
        },
        'openrouter': {
            'meta-llama/llama-3.1-70b': {'input': 0.52, 'output': 0.75},
            'google/gemini-pro': {'input': 0.125, 'output': 0.375},
            'mistralai/mixtral-8x7b': {'input': 0.24, 'output': 0.24}
        }
    }
    
    def __init__(self, log_file: str = "data/token_usage.json"):
        self.log_file = log_file
        self.usage_history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Carregar histórico de uso"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_history(self):
        """Salvar histórico de uso"""
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_history, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    def calculate_cost(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> Dict:
        """
        Calcular custo de uma requisição
        """
        try:
            pricing = self.PRICING.get(provider, {}).get(model, None)
            
            if not pricing:
                return {
                    'error': f'Modelo {provider}/{model} não encontrado na tabela de preços',
                    'cost': 0.0
                }
            
            input_cost = (input_tokens / 1_000_000) * pricing['input']
            output_cost = (output_tokens / 1_000_000) * pricing['output']
            total_cost = input_cost + output_cost
            
            return {
                'provider': provider,
                'model': model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': input_tokens + output_tokens,
                'input_cost': round(input_cost, 6),
                'output_cost': round(output_cost, 6),
                'total_cost': round(total_cost, 6),
                'currency': 'USD'
            }
        except Exception as e:
            return {'error': str(e), 'cost': 0.0}
    
    def log_usage(self, provider: str, model: str, input_tokens: int, output_tokens: int, 
                  task_id: Optional[str] = None):
        """Registrar uso de tokens"""
        cost_info = self.calculate_cost(provider, model, input_tokens, output_tokens)
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task_id': task_id,
            **cost_info
        }
        
        self.usage_history.append(entry)
        self._save_history()
    
    def get_total_cost(self, provider: Optional[str] = None, 
                       start_date: Optional[str] = None) -> float:
        """Calcular custo total"""
        filtered = self.usage_history
        
        if provider:
            filtered = [e for e in filtered if e.get('provider') == provider]
        
        if start_date:
            filtered = [e for e in filtered if e.get('timestamp', '') >= start_date]
        
        return sum(e.get('total_cost', 0) for e in filtered)
    
    def get_usage_stats(self) -> Dict:
        """Gerar estatísticas de uso"""
        if not self.usage_history:
            return {
                'total_requests': 0,
                'total_cost': 0.0,
                'by_provider': {},
                'by_model': {}
            }
        
        stats = {
            'total_requests': len(self.usage_history),
            'total_cost': self.get_total_cost(),
            'total_tokens': sum(e.get('total_tokens', 0) for e in self.usage_history),
            'by_provider': {},
            'by_model': {}
        }
        
        # Por provider
        for entry in self.usage_history:
            provider = entry.get('provider', 'unknown')
            if provider not in stats['by_provider']:
                stats['by_provider'][provider] = {
                    'requests': 0,
                    'cost': 0.0,
                    'tokens': 0
                }
            
            stats['by_provider'][provider]['requests'] += 1
            stats['by_provider'][provider]['cost'] += entry.get('total_cost', 0)
            stats['by_provider'][provider]['tokens'] += entry.get('total_tokens', 0)
        
        # Por modelo
        for entry in self.usage_history:
            model = entry.get('model', 'unknown')
            if model not in stats['by_model']:
                stats['by_model'][model] = {
                    'requests': 0,
                    'cost': 0.0,
                    'tokens': 0
                }
            
            stats['by_model'][model]['requests'] += 1
            stats['by_model'][model]['cost'] += entry.get('total_cost', 0)
            stats['by_model'][model]['tokens'] += entry.get('total_tokens', 0)
        
        return stats
    
    def get_pricing_table(self) -> Dict:
        """Retornar tabela de preços"""
        return self.PRICING
    
    def compare_models(self, input_tokens: int = 1000, output_tokens: int = 1000) -> List[Dict]:
        """
        Comparar custos entre diferentes modelos para uma quantidade específica de tokens
        """
        comparisons = []
        
        for provider, models in self.PRICING.items():
            for model, pricing in models.items():
                cost = self.calculate_cost(provider, model, input_tokens, output_tokens)
                comparisons.append({
                    'provider': provider,
                    'model': model,
                    'cost_per_request': cost.get('total_cost', 0),
                    'cost_per_1k_tokens': cost.get('total_cost', 0) * (1000 / (input_tokens + output_tokens))
                })
        
        return sorted(comparisons, key=lambda x: x['cost_per_request'])


# ==========================================
# EXEMPLO DE USO
# ==========================================

if __name__ == "__main__":
    agent = TokenCostAgent()
    
    print("=" * 60)
    print("TOKEN COST AGENT - TABELA DE PREÇOS")
    print("=" * 60)
    
    print("\n💰 Preços por 1M tokens (USD):")
    for provider, models in agent.get_pricing_table().items():
        print(f"\n📌 {provider.upper()}:")
        for model, pricing in models.items():
            print(f"  • {model}")
            print(f"    Input:  ${pricing['input']:.2f}")
            print(f"    Output: ${pricing['output']:.2f}")
    
    print("\n\n📊 Comparação de Custos (1K input + 1K output tokens):")
    comparisons = agent.compare_models(1000, 1000)
    
    print(f"\n{'Rank':<6} {'Provider':<15} {'Model':<30} {'Cost':<10}")
    print("-" * 70)
    
    for i, comp in enumerate(comparisons[:10], 1):
        print(f"{i:<6} {comp['provider']:<15} {comp['model']:<30} ${comp['cost_per_request']:.6f}")
