@echo off
mkdir "06_BACKUPS\Credenciais_Obsoletas" 2>nul
mkdir "06_BACKUPS\SENSIVEL" 2>nul
mkdir "02_DOCUMENTACAO_REFERENCIA" 2>nul
mkdir "04_OPERACIONAL\Rascunhos" 2>nul
mkdir "05_ARQUIVO_HISTORICO" 2>nul
mkdir "04_OPERACIONAL" 2>nul
mkdir "00_ENTRADA" 2>nul
mkdir "01_DOCUMENTACAO_CONSOLIDADA" 2>nul

move /Y "Api kEy" "06_BACKUPS\Credenciais_Obsoletas\"
move /Y "Informação do cartão de pagamento (importante)" "06_BACKUPS\SENSIVEL\"
move /Y "Google conexões" "02_DOCUMENTACAO_REFERENCIA\"
move /Y "Instalção do Juniper notebook.ipynb" "02_DOCUMENTACAO_REFERENCIA\"
move /Y "Novo Documento de Texto.txt" "04_OPERACIONAL\Rascunhos\"
move /Y "05-12-25" "05_ARQUIVO_HISTORICO\"
move /Y "Ideias.MD" "04_OPERACIONAL\Ideias_Raiz.MD"
move /Y "Tarefas.MD" "04_OPERACIONAL\Tarefas_Raiz.MD"
move /Y "COMECE_AQUI.md" "00_ENTRADA\"
move /Y "INDICE_DOCUMENTACAO.md" "00_ENTRADA\"
move /Y "RESUMO_FINAL.md" "01_DOCUMENTACAO_CONSOLIDADA\"
echo Done.
