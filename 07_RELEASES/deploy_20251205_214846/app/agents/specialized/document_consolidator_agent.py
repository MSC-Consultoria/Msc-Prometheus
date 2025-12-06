"""
Agente Especializado: Consolidador de Documentação
Identifica e consolida documentos duplicados
"""

import os
import difflib
from typing import List, Dict, Tuple
from pathlib import Path


class DocumentConsolidatorAgent:
    """
    Agente responsável por consolidar documentos duplicados ou similares
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.similarity_threshold = 0.85  # 85% de similaridade
        
    def find_markdown_files(self, directory: str = None) -> List[str]:
        """Encontrar todos os arquivos .md no diretório"""
        if directory is None:
            directory = self.base_dir
        
        md_files = []
        for root, dirs, files in os.walk(directory):
            # Ignorar diretórios de backup
            if '06_BACKUPS' in root or '05_ARQUIVO_HISTORICO' in root:
                continue
                
            for file in files:
                if file.endswith('.md') or file.endswith('.MD'):
                    md_files.append(os.path.join(root, file))
        
        return md_files
    
    def read_file_content(self, file_path: str) -> str:
        """Ler conteúdo de um arquivo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler {file_path}: {e}"
    
    def calculate_similarity(self, content1: str, content2: str) -> float:
        """Calcular similaridade entre dois textos"""
        seq = difflib.SequenceMatcher(None, content1, content2)
        return seq.ratio()
    
    def find_similar_documents(self) -> List[Tuple[str, str, float]]:
        """
        Encontrar documentos similares
        Retorna: [(arquivo1, arquivo2, similaridade), ...]
        """
        files = self.find_markdown_files()
        similar_pairs = []
        
        # Comparar cada par de arquivos
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1 = files[i]
                file2 = files[j]
                
                content1 = self.read_file_content(file1)
                content2 = self.read_file_content(file2)
                
                similarity = self.calculate_similarity(content1, content2)
                
                if similarity >= self.similarity_threshold:
                    similar_pairs.append((file1, file2, similarity))
        
        return sorted(similar_pairs, key=lambda x: x[2], reverse=True)
    
    def consolidate_files(self, file1: str, file2: str, output_file: str) -> bool:
        """
        Consolidar dois arquivos em um único arquivo
        """
        try:
            content1 = self.read_file_content(file1)
            content2 = self.read_file_content(file2)
            
            # Criar conteúdo consolidado
            consolidated = f"""# Documento Consolidado

**Origem:**
- {os.path.basename(file1)}
- {os.path.basename(file2)}

**Data de Consolidação:** {self._get_timestamp()}

---

## Conteúdo de {os.path.basename(file1)}

{content1}

---

## Conteúdo de {os.path.basename(file2)}

{content2}

---

**Nota:** Este documento foi gerado automaticamente pelo Document Consolidator Agent.
Os arquivos originais foram movidos para a pasta de arquivo histórico.
"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(consolidated)
            
            return True
        except Exception as e:
            print(f"Erro ao consolidar: {e}")
            return False
    
    def move_to_archive(self, file_path: str) -> bool:
        """Mover arquivo para pasta de arquivo"""
        try:
            archive_dir = "05_ARQUIVO_HISTORICO"
            os.makedirs(archive_dir, exist_ok=True)
            
            filename = os.path.basename(file_path)
            archive_path = os.path.join(archive_dir, filename)
            
            # Se já existe, adicionar timestamp
            if os.path.exists(archive_path):
                name, ext = os.path.splitext(filename)
                archive_path = os.path.join(archive_dir, f"{name}_{self._get_timestamp()}{ext}")
            
            os.rename(file_path, archive_path)
            return True
        except Exception as e:
            print(f"Erro ao arquivar {file_path}: {e}")
            return False
    
    def _get_timestamp(self) -> str:
        """Obter timestamp formatado"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def generate_consolidation_report(self) -> Dict:
        """Gerar relatório de consolidação"""
        similar_docs = self.find_similar_documents()
        all_files = self.find_markdown_files()
        
        return {
            'total_files': len(all_files),
            'similar_pairs': len(similar_docs),
            'pairs': [
                {
                    'file1': os.path.basename(pair[0]),
                    'file2': os.path.basename(pair[1]),
                    'similarity': f"{pair[2]*100:.1f}%"
                }
                for pair in similar_docs
            ]
        }
    
    def suggest_consolidations(self) -> List[Dict]:
        """Sugerir consolidações baseadas em similaridade"""
        similar_docs = self.find_similar_documents()
        
        suggestions = []
        for file1, file2, similarity in similar_docs:
            suggestions.append({
                'action': 'consolidate',
                'files': [file1, file2],
                'similarity': similarity,
                'reason': f"Arquivos {similarity*100:.0f}% similares - consolidação recomendada"
            })
        
        return suggestions


# ==========================================
# EXEMPLO DE USO
# ==========================================

if __name__ == "__main__":
    agent = DocumentConsolidatorAgent()
    
    print("=" * 60)
    print("DOCUMENT CONSOLIDATOR AGENT - RELATÓRIO")
    print("=" * 60)
    
    report = agent.generate_consolidation_report()
    
    print(f"\n📄 Total de Arquivos .md: {report['total_files']}")
    print(f"🔍 Pares Similares Encontrados: {report['similar_pairs']}")
    
    if report['pairs']:
        print("\n📋 Documentos Similares:")
        for pair in report['pairs']:
            print(f"  • {pair['file1']} ⟷ {pair['file2']}")
            print(f"    Similaridade: {pair['similarity']}")
    
    print("\n💡 Sugestões de Consolidação:")
    suggestions = agent.suggest_consolidations()
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n  {i}. {suggestion['reason']}")
        print(f"     Arquivos: {', '.join([os.path.basename(f) for f in suggestion['files']])}")
