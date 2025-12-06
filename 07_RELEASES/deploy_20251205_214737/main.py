import re
import os
import shutil
import time
from openai import OpenAI

# ==========================================
# CONFIGURAÇÃO
# ==========================================
# Insira sua chave API aqui ou use variáveis de ambiente
API_KEY = "SUA_CHAVE_API_AQUI" 
MODELO = "gpt-4o-mini" # Use "gpt-4o" para tarefas muito complexas

client = OpenAI(api_key=API_KEY)

class AgenticMarkdown:
    def __init__(self, filepath):
        self.filepath = filepath
        # Define o diretório de trabalho como o local do arquivo .md
        self.workdir = os.path.dirname(os.path.abspath(filepath))
        self.backup_dir = os.path.join(self.workdir, ".backups")
        self.recarregar_conteudo()

    def recarregar_conteudo(self):
        """Lê o arquivo Markdown do disco para a memória."""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
        self.lines = self.content.split('\n')

    def obter_historico(self, linha_atual_idx):
        """
        Pega o texto do início do arquivo até a tarefa atual.
        Isso dá ao agente a 'Memória de Curto Prazo' do projeto.
        """
        return "\n".join(self.lines[:linha_atual_idx])

    def encontrar_proxima_tarefa(self):
        """Encontra a primeira linha contendo uma tarefa pendente '- [ ]'."""
        for i, line in enumerate(self.lines):
            if "- [ ]" in line:
                return i, line.replace("- [ ]", "").strip()
        return None, None

    # --- FEATURE: BACKUP AUTOMÁTICO ---
    def criar_backup(self, caminho_arquivo):
        """Cria uma cópia do arquivo antes de sobrescrevê-lo."""
        if not os.path.exists(caminho_arquivo):
            return
        
        os.makedirs(self.backup_dir, exist_ok=True)
        nome_arquivo = os.path.basename(caminho_arquivo)
        timestamp = int(time.time())
        # Ex: style.css -> .backups/style.css_17150021.bak
        caminho_backup = os.path.join(self.backup_dir, f"{nome_arquivo}_{timestamp}.bak")
        
        shutil.copy2(caminho_arquivo, caminho_backup)
        print(f"    🛡️ Backup de segurança criado: {os.path.basename(caminho_backup)}")

    # --- FEATURE: LEITURA DE ARQUIVOS ---
    def resolver_leituras(self, texto_tarefa):
        """
        Procura pela sintaxe {ler:caminho/arquivo} e carrega o conteúdo.
        """
        padrao = r'\{ler:([^}]+)\}'
        matches = re.finditer(padrao, texto_tarefa)
        
        contexto_arquivos = ""
        arquivos_lidos = []
        
        for match in matches:
            caminho_rel = match.group(1).strip()
            caminho_full = os.path.join(self.workdir, caminho_rel)
            
            if os.path.exists(caminho_full):
                with open(caminho_full, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                contexto_arquivos += f"\n=== ARQUIVO LIDO: '{caminho_rel}' ===\n{conteudo}\n==============================\n"
                arquivos_lidos.append(caminho_rel)
                print(f"    📖 Lendo contexto: {caminho_rel}")
            else:
                contexto_arquivos += f"\n(AVISO DO SISTEMA: O arquivo solicitado '{caminho_rel}' não existe no disco.)\n"
        
        return contexto_arquivos, arquivos_lidos

    # --- FEATURE: GERAÇÃO DE ARQUIVOS ---
    def processar_escrita_arquivos(self, texto_resposta):
        """
        Procura pela sintaxe ```lang:caminho/arquivo ... ``` e salva no disco.
        """
        padrao = r'```[\w\-\+]+:([^\n]+)\n(.*?)```'
        matches = re.finditer(padrao, texto_resposta, re.DOTALL)
        arquivos_criados = []
        
        for match in matches:
            caminho_relativo = match.group(1).strip()
            conteudo_novo = match.group(2)
            caminho_completo = os.path.join(self.workdir, caminho_relativo)
            
            # 1. Cria backup se o arquivo já existir
            self.criar_backup(caminho_completo)
            
            # 2. Cria diretórios necessários
            os.makedirs(os.path.dirname(caminho_completo), exist_ok=True)
            
            # 3. Escreve o arquivo
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                f.write(conteudo_novo)
            
            arquivos_criados.append(caminho_relativo)
            print(f"    💾 Arquivo salvo: {caminho_relativo}")
            
        return arquivos_criados

    def executar_tarefa(self, historico, tarefa):
        print(f"\n🤖 Analisando tarefa: '{tarefa[:60]}...'")
        
        # 1. Resolve leituras de arquivos solicitadas na tarefa
        contexto_extra, arquivos_lidos = self.resolver_leituras(tarefa)
        
        system_prompt = (
            "Você é um Engenheiro de Software Autônomo operando via Markdown."
            "\n\nREGRAS CRÍTICAS:"
            "\n1. Se for pedido para criar ou editar código, use SEMPRE este formato:"
            "\n```linguagem:caminho/do/arquivo.ext\n[CONTEÚDO DO ARQUIVO]\n```"
            "\n2. Se for editar um arquivo, REESCREVA O ARQUIVO INTEIRO no bloco de código."
            "\n3. Seja conciso nos comentários."
        )

        user_prompt = f"""
        === HISTÓRICO DE EXECUÇÃO (O que já foi feito) ===
        {historico}
        
        === ARQUIVOS CARREGADOS PARA CONTEXTO ===
        {contexto_extra}
        
        === TAREFA ATUAL A SER EXECUTADA ===
        {tarefa}
        """
        
        print("    ⏳ Aguardando resposta da IA...")
        try:
            response = client.chat.completions.create(
                model=MODELO,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            resposta_agente = response.choices[0].message.content
            
            # Processar a resposta para extrair e salvar arquivos
            arquivos_criados = self.processar_escrita_arquivos(resposta_agente)
            
            return resposta_agente, arquivos_criados
            
        except Exception as e:
            print(f"❌ Erro na API: {e}")
            return f"Erro ao executar tarefa: {e}", []

def main():
    print("🚀 Iniciando Agente Markdown...")
    # Placeholder para execução principal
    pass

if __name__ == "__main__":
    main()