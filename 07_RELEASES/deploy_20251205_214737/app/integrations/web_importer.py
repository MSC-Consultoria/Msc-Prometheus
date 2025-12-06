"""
Web Importer - Converter páginas web em Markdown
Transforma conteúdo HTML de URLs em documentos estruturados
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import json
import re
from typing import Optional, Dict, List


class WebImporter:
    """Importar e converter páginas web para Markdown"""
    
    def __init__(self, output_dir: str = None):
        """
        Inicializar importer
        
        Args:
            output_dir: Diretório para salvar docs (padrão: app/data/imported_docs)
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / 'data' / 'imported_docs'
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.output_dir / 'index.json'
        self._load_index()
    
    def _load_index(self):
        """Carregar índice de documentos importados"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = []
    
    def _save_index(self):
        """Salvar índice de documentos"""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fazer download da página
        
        Args:
            url: URL da página
            
        Returns:
            Conteúdo HTML ou None
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Erro ao baixar página: {str(e)}")
    
    def _extract_content(self, html: str) -> Dict[str, str]:
        """
        Extrair conteúdo relevante do HTML
        
        Args:
            html: HTML da página
            
        Returns:
            Dict com title e content
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remover scripts e styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extrair título
        title = "Sem Título"
        if soup.title:
            title = soup.title.string
        elif soup.h1:
            title = soup.h1.get_text().strip()
        
        # Extrair conteúdo principal
        content = ""
        
        # Tentar encontrar main content
        main_content = soup.find(['main', 'article'])
        if main_content:
            content = main_content.get_text()
        else:
            # Fallback: usar body
            body = soup.find('body')
            if body:
                content = body.get_text()
        
        # Limpar espaços em branco excessivos
        content = re.sub(r'\n\s*\n', '\n\n', content).strip()
        
        return {
            "title": title.strip(),
            "content": content,
            "url": ""  # Será preenchido depois
        }
    
    def _html_to_markdown(self, html: str, title: str) -> str:
        """
        Converter HTML para Markdown estruturado
        
        Args:
            html: HTML da página
            title: Título do documento
            
        Returns:
            Conteúdo em Markdown
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remover scripts e styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        markdown = f"# {title}\n\n"
        markdown += f"> Importado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        # Extrair headers
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = int(heading.name[1])
            text = heading.get_text().strip()
            if text and text.lower() != title.lower():
                markdown += f"{'#' * (level + 1)} {text}\n\n"
        
        # Extrair parágrafos
        for para in soup.find_all('p'):
            text = para.get_text().strip()
            if text:
                markdown += f"{text}\n\n"
        
        # Extrair listas
        for ul in soup.find_all('ul'):
            for li in ul.find_all('li', recursive=False):
                text = li.get_text().strip()
                if text:
                    markdown += f"- {text}\n"
            markdown += "\n"
        
        # Extrair código
        for code_block in soup.find_all(['pre', 'code']):
            code_text = code_block.get_text().strip()
            if code_text:
                if code_block.name == 'pre':
                    markdown += f"```\n{code_text}\n```\n\n"
                else:
                    markdown += f"`{code_text}`\n\n"
        
        # Extrair links
        markdown += "\n## 🔗 Links Referenciados\n\n"
        links_found = False
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip()
            if href.startswith('http'):
                markdown += f"- [{text or href}]({href})\n"
                links_found = True
        
        if not links_found:
            markdown = markdown.replace("## 🔗 Links Referenciados\n\n", "")
        
        return markdown
    
    def import_and_save(self, url: str, custom_title: Optional[str] = None) -> Dict:
        """
        Importar URL e salvar como Markdown
        
        Args:
            url: URL da página
            custom_title: Título customizado (opcional)
            
        Returns:
            Dict com informações do arquivo salvo
        """
        # Validar URL
        if not url.startswith('http'):
            raise ValueError("URL deve começar com http:// ou https://")
        
        # Fazer download
        html = self._fetch_page(url)
        
        # Extrair informações
        extracted = self._extract_content(html)
        title = custom_title or extracted['title']
        
        # Converter para Markdown
        markdown = self._html_to_markdown(html, title)
        
        # Gerar nome do arquivo
        filename = re.sub(r'[^a-z0-9_-]', '_', title.lower())
        filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Salvar arquivo
        filepath = self.output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        # Atualizar índice
        doc_info = {
            "title": title,
            "filename": filename,
            "url": url,
            "date": datetime.now().isoformat(),
            "size": len(markdown),
            "path": str(filepath)
        }
        self.index.append(doc_info)
        self._save_index()
        
        return {
            "filename": filename,
            "title": title,
            "path": str(filepath),
            "size": len(markdown),
            "url": url
        }
    
    def list_docs(self) -> List[Dict]:
        """
        Listar documentos importados
        
        Returns:
            Lista de documentos com metadados
        """
        docs = []
        for doc in self.index:
            docs.append({
                "title": doc['title'],
                "filename": doc['filename'],
                "date": doc['date'],
                "size": f"{doc['size']} bytes",
                "url": doc['url']
            })
        return docs
    
    def get_doc(self, filename: str) -> Optional[str]:
        """
        Obter conteúdo de um documento
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            Conteúdo do arquivo ou None
        """
        filepath = self.output_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def delete_doc(self, filename: str) -> bool:
        """
        Deletar um documento
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            True se deletado, False se não encontrado
        """
        filepath = self.output_dir / filename
        if filepath.exists():
            filepath.unlink()
            self.index = [d for d in self.index if d['filename'] != filename]
            self._save_index()
            return True
        return False


# ==========================================
# EXEMPLO DE USO
# ==========================================

if __name__ == '__main__':
    importer = WebImporter()
    
    # Importar uma página
    result = importer.import_and_save(
        'https://www.example.com',
        'Meu Documento'
    )
    
    print(f"✅ Documento importado: {result['filename']}")
    
    # Listar documentos
    docs = importer.list_docs()
    print(f"\n📚 {len(docs)} documentos importados:")
    for doc in docs:
        print(f"  - {doc['title']} ({doc['size']})")
