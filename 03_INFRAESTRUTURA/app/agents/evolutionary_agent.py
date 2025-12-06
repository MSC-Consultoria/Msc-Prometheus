"""
Prometheus Evolutionary Agent
Sistema de agentes evolutivos que aprendem através de documentação estruturada
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import re

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


@dataclass
class Evolution:
    """Registro de evolução do agente"""
    timestamp: str
    task_id: str
    task_description: str
    agent_response: str
    success: bool
    learning_points: List[str]
    version: str


class EvolutionaryAgent:
    """
    Agente que evolui através da documentação e experiência
    Aprende com cada tarefa e melhora continuamente
    
    Suporta múltiplos provedores de LLM:
    - OpenAI (GPT-4, GPT-4o, GPT-4o-mini)
    - Anthropic (Claude)
    - Google (Gemini)
    - DeepSeek
    - OpenRouter (multi-model)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", provider: str = "openai"):
        """
        Inicializar agente evolutivo
        
        Args:
            api_key: API key do provedor (opcional, busca do .env)
            model: Nome do modelo a usar
            provider: Provedor de LLM (openai, anthropic, gemini, deepseek, openrouter)
        """
        self.provider = provider.lower()
        self.model = model
        self.evolution_history: List[Evolution] = []
        self.knowledge_base: Dict[str, str] = {}
        self.version = "1.0.0"
        self.created_at = datetime.now().isoformat()
        
        # Inicializar cliente baseado no provedor
        self._init_provider_client(api_key)
        
        # Carregar histórico se existir
        self._load_evolution_history()
    
    def _init_provider_client(self, api_key: Optional[str] = None):
        """Inicializa o cliente do provedor de LLM"""
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.client = OpenAI(api_key=self.api_key) if OpenAI and self.api_key else None
            
        elif self.provider == "anthropic":
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            self.client = Anthropic(api_key=self.api_key) if Anthropic and self.api_key else None
            
        elif self.provider == "gemini":
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if genai and self.api_key:
                genai.configure(api_key=self.api_key)
                self.client = genai
            else:
                self.client = None
                
        elif self.provider == "deepseek":
            # DeepSeek usa API compatível com OpenAI
            self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
            if OpenAI and self.api_key:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.deepseek.com/v1"
                )
            else:
                self.client = None
                
        elif self.provider == "openrouter":
            # OpenRouter usa API compatível com OpenAI
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            if OpenAI and self.api_key:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://openrouter.ai/api/v1"
                )
            else:
                self.client = None
        
        else:
            raise ValueError(f"Provedor não suportado: {self.provider}")
        
        if not self.client:
            print(f"⚠️ Cliente {self.provider} não inicializado. Verifique API key e dependências.")
        
    def _load_evolution_history(self):
        """Carrega histórico de evolução anterior"""
        history_file = Path(__file__).parent.parent / "data" / "evolution_history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.evolution_history = [Evolution(**item) for item in data.get("history", [])]
                self.knowledge_base = data.get("knowledge_base", {})
                self.version = data.get("version", "1.0.0")
    
    def _save_evolution_history(self):
        """Salva histórico de evolução"""
        history_file = Path(__file__).parent.parent / "data" / "evolution_history.json"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "version": self.version,
            "created_at": self.created_at,
            "last_updated": datetime.now().isoformat(),
            "total_evolutions": len(self.evolution_history),
            "history": [asdict(e) for e in self.evolution_history[-100:]],  # Últimas 100
            "knowledge_base": self.knowledge_base
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def extract_learning_points(self, task_description: str, response: str) -> List[str]:
        """Extrai pontos de aprendizado de uma resposta"""
        learning_points = []
        
        # Padrões de aprendizado
        if "erro" in response.lower():
            learning_points.append("error_handling")
        if "otimiz" in response.lower():
            learning_points.append("optimization")
        if "integr" in response.lower():
            learning_points.append("integration")
        if "segur" in response.lower():
            learning_points.append("security")
        if "docum" in response.lower():
            learning_points.append("documentation")
        
        return learning_points
    
    def process_task(self, 
                    task_description: str,
                    context: Optional[str] = None,
                    files_context: Optional[List[str]] = None) -> Dict:
        """
        Processa uma tarefa e evoluí com a experiência
        
        Args:
            task_description: Descrição da tarefa
            context: Contexto adicional
            files_context: Arquivos para carregar como contexto
        
        Returns:
            Dicionário com resposta e metadata
        """
        
        task_id = f"task_{int(time.time())}"
        start_time = time.time()
        
        # Construir prompt
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(task_description, context, files_context)
        
        try:
            # Chamar LLM
            response_text = self._call_llm(system_prompt, user_prompt)
            success = True
            
        except Exception as e:
            response_text = f"Erro ao processar: {str(e)}"
            success = False
        
        # Extrair aprendizados
        learning_points = self.extract_learning_points(task_description, response_text)
        
        # Registrar evolução
        evolution = Evolution(
            timestamp=datetime.now().isoformat(),
            task_id=task_id,
            task_description=task_description[:100],
            agent_response=response_text[:500],
            success=success,
            learning_points=learning_points,
            version=self.version
        )
        
        self.evolution_history.append(evolution)
        self._save_evolution_history()
        
        # Atualizar knowledge base
        if success:
            self.knowledge_base[task_id] = response_text[:1000]
        
        elapsed_time = time.time() - start_time
        
        return {
            "task_id": task_id,
            "status": "success" if success else "error",
            "response": response_text,
            "learning_points": learning_points,
            "elapsed_time": round(elapsed_time, 2),
            "timestamp": datetime.now().isoformat(),
            "evolution_count": len(self.evolution_history)
        }
    
    def _build_system_prompt(self) -> str:
        """Constrói o prompt de sistema baseado em histórico"""
        base_prompt = """Você é o Prometheus, um agente evolutivo de IA que:
        
1. Converte dados em documentação estruturada (Formato Juniper)
2. Gerencia infraestrutura, cloud e versionamento
3. Garante compatibilidade cross-platform (Windows, Linux, macOS)
4. Evolui continuamente através de experiência documentada

Princípios:
- Código rigoroso e typed (type hints)
- Markdown estruturado para documentação
- 60% Inglês, 40% Português na documentação
- Máximo 10 arquivos ativos por vez
- Zero redundância, máxima clareza

Responda sempre em Markdown estruturado, com exemplos quando apropriado.
"""
        
        # Adicionar aprendizados do histórico
        if self.evolution_history:
            recent_learnings = set()
            for evo in self.evolution_history[-20:]:
                recent_learnings.update(evo.learning_points)
            
            if recent_learnings:
                base_prompt += f"\nAprendizados Recentes: {', '.join(recent_learnings)}\n"
        
        return base_prompt
    
    def _build_user_prompt(self, 
                          task_description: str,
                          context: Optional[str] = None,
                          files_context: Optional[List[str]] = None) -> str:
        """Constrói o prompt do usuário com contexto"""
        prompt = f"## Tarefa\n\n{task_description}\n"
        
        if context:
            prompt += f"\n## Contexto Adicional\n\n{context}\n"
        
        if files_context:
            prompt += "\n## Arquivos para Análise\n\n"
            for file_path in files_context:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()[:500]  # Primeiros 500 chars
                    prompt += f"- `{file_path}`: {content}\n"
        
        prompt += "\n## Formato de Resposta\n\nResponda estruturado em Markdown.\n"
        
        return prompt
    
    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """
        Chama a API do LLM baseado no provedor configurado
        
        Suporta: OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter
        """
        if not self.client:
            return f"⚠️ Cliente {self.provider} não configurado. Configure a API key no .env"
        
        try:
            if self.provider in ["openai", "deepseek", "openrouter"]:
                # OpenAI-compatible API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            
            elif self.provider == "anthropic":
                # Anthropic Claude API
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    temperature=0.7,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text
            
            elif self.provider == "gemini":
                # Google Gemini API
                model = self.client.GenerativeModel(self.model)
                prompt = f"{system_prompt}\n\n{user_prompt}"
                response = model.generate_content(prompt)
                return response.text
            
            else:
                raise ValueError(f"Provedor não suportado: {self.provider}")
            
        except Exception as e:
            raise Exception(f"Erro ao chamar {self.provider}: {str(e)}")
    
    def change_provider(self, provider: str, model: str, api_key: Optional[str] = None):
        """
        Troca o provedor de LLM dinamicamente
        
        Args:
            provider: Novo provedor (openai, anthropic, gemini, deepseek, openrouter)
            model: Modelo a usar no novo provedor
            api_key: API key opcional (se não fornecido, busca do .env)
        """
        self.provider = provider.lower()
        self.model = model
        self._init_provider_client(api_key)
        
        return {
            "status": "success" if self.client else "error",
            "provider": self.provider,
            "model": self.model,
            "client_initialized": bool(self.client)
        }
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do agente"""
        successful = sum(1 for e in self.evolution_history if e.success)
        failed = len(self.evolution_history) - successful
        
        return {
            "version": self.version,
            "created_at": self.created_at,
            "provider": self.provider,
            "model": self.model,
            "total_tasks": len(self.evolution_history),
            "successful": successful,
            "failed": failed,
            "success_rate": f"{(successful/len(self.evolution_history)*100):.1f}%" if self.evolution_history else "N/A",
            "knowledge_entries": len(self.knowledge_base),
            "learning_areas": list(set(lp for e in self.evolution_history for lp in e.learning_points))
        }
    
    def get_evolution_timeline(self, limit: int = 20) -> List[Dict]:
        """Retorna timeline de evolução"""
        return [
            {
                "timestamp": e.timestamp,
                "task_id": e.task_id,
                "task": e.task_description,
                "success": e.success,
                "learnings": e.learning_points
            }
            for e in self.evolution_history[-limit:]
        ]
    
    def export_knowledge(self, format: str = "json") -> str:
        """Exporta base de conhecimento"""
        if format == "json":
            return json.dumps(self.knowledge_base, indent=2, ensure_ascii=False)
        elif format == "markdown":
            md = "# Base de Conhecimento do Prometheus\n\n"
            for task_id, content in self.knowledge_base.items():
                md += f"## {task_id}\n\n{content}\n\n"
            return md
        else:
            raise ValueError(f"Formato desconhecido: {format}")


# Exemplo de uso
if __name__ == "__main__":
    agent = EvolutionaryAgent()
    
    # Primeira tarefa
    result = agent.process_task(
        task_description="Crie um exemplo de documentação no formato Juniper",
        context="Use Markdown estruturado com Python"
    )
    
    print("📊 Resultado:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n📈 Estatísticas do Agente:")
    print(json.dumps(agent.get_stats(), indent=2, ensure_ascii=False))
