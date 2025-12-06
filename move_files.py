import shutil
import os

def move_file(src, dst):
    try:
        if os.path.exists(src):
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            print(f"Moved: {src} -> {dst}")
        else:
            print(f"Not found: {src}")
    except Exception as e:
        print(f"Error moving {src}: {e}")

base_dir = os.getcwd()

# Mappings
moves = [
    ("Api kEy", "06_BACKUPS/Credenciais_Obsoletas/Api kEy"),
    ("Informação do cartão de pagamento (importante)", "06_BACKUPS/SENSIVEL/Informação do cartão de pagamento (importante)"),
    ("Google conexões", "02_DOCUMENTACAO_REFERENCIA/Google conexões"),
    ("Instalção do Juniper notebook.ipynb", "02_DOCUMENTACAO_REFERENCIA/Instalção do Juniper notebook.ipynb"),
    ("Novo Documento de Texto.txt", "04_OPERACIONAL/Rascunhos/Novo Documento de Texto.txt"),
    ("05-12-25", "05_ARQUIVO_HISTORICO/05-12-25"),
    ("Ideias.MD", "04_OPERACIONAL/Ideias_Raiz.MD"),
    ("Tarefas.MD", "04_OPERACIONAL/Tarefas_Raiz.MD"),
    ("COMECE_AQUI.md", "00_ENTRADA/COMECE_AQUI.md"),
    ("INDICE_DOCUMENTACAO.md", "00_ENTRADA/INDICE_DOCUMENTACAO.md"),
    ("RESUMO_FINAL.md", "01_DOCUMENTACAO_CONSOLIDADA/RESUMO_FINAL.md")
]

for src, dst in moves:
    move_file(os.path.join(base_dir, src), os.path.join(base_dir, dst))

print("Organization complete.")
