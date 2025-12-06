# 🔗 Integração Google Workspace - Guia de Setup

## 📋 Overview

Este documento guia a integração do Prometheus com Google Workspace para:
- ☁️ Armazenar backups em Google Drive
- 📧 Sincronizar tarefas com Google Tarefas
- 📅 Integrar calendário para agendamentos
- 📝 Sincronizar documentos para análise

---

## 🔑 Passo 1: Criar Credenciais Google Cloud

### 1.1 Acessar Google Cloud Console
```
URL: https://console.cloud.google.com
1. Login com conta Google
2. Criar novo projeto: "Prometheus-Space"
3. Ativar APIs necessárias
```

### 1.2 APIs a Ativar
- ✅ Google Drive API
- ✅ Google Tasks API
- ✅ Google Calendar API
- ✅ Gmail API (opcional)

### 1.3 Criar Service Account
```
1. Ir para: Credenciais → Criar Credencial
2. Escolher: "Service Account"
3. Nome: "prometheus-agent"
4. Criar e baixar JSON da chave privada
5. Salvar como: `.env.google.json`
```

---

## 🔐 Passo 2: Configurar Arquivo .env

Criar arquivo `.env` na raiz do projeto:

```env
# OpenAI
OPENAI_API_KEY="sk-proj-xxxxxxxxxxxx"
OPENAI_MODEL="gpt-4o-mini"

# Google Cloud
GOOGLE_APPLICATION_CREDENTIALS=".env.google.json"
GOOGLE_PROJECT_ID="prometheus-space-xxxxx"

# Google Drive
GOOGLE_DRIVE_BACKUP_FOLDER_ID="1A-xxxxx-folder-id"

# Google Tasks
GOOGLE_TASKLIST_ID="@default"

# Modo de operação
ENV="development"  # ou "production"
```

---

## 🛠️ Passo 3: Instalar Dependências Google

Atualizar `requirements.txt`:

```txt
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.28.0
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.0.0
```

Instalar:
```bash
pip install -r requirements.txt
```

---

## 📁 Passo 4: Script de Backup para Google Drive

Criar arquivo `backup_to_drive.py`:

```python
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from datetime import datetime

class GoogleDriveBackup:
    """Gerencia backups automáticos para Google Drive"""
    
    def __init__(self, credentials_path: str, folder_id: str):
        self.credentials_path = credentials_path
        self.folder_id = folder_id
        self.drive_service = self._authenticate()
    
    def _authenticate(self):
        """Autentica com Google Drive API"""
        SCOPES = ['https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES
        )
        return build('drive', 'v3', credentials=credentials)
    
    def upload_backup(self, local_path: str, file_name: str = None) -> str:
        """Upload de arquivo para Google Drive"""
        if not file_name:
            file_name = os.path.basename(local_path)
        
        # Adicionar timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{timestamp}_{file_name}"
        
        file_metadata = {
            'name': file_name,
            'parents': [self.folder_id]
        }
        
        media = MediaFileUpload(local_path, resumable=True)
        file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"✅ Arquivo enviado para Drive: {file_name} (ID: {file['id']})")
        return file['id']

# Exemplo de uso
if __name__ == "__main__":
    backup = GoogleDriveBackup(
        credentials_path=".env.google.json",
        folder_id="seu-folder-id-aqui"
    )
    backup.upload_backup("CONSOLIDADO_ESTRATEGICO.md")
```

---

## 📝 Passo 5: Sincronizar com Google Tasks

Criar arquivo `sync_google_tasks.py`:

```python
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import re

class GoogleTasksSync:
    """Sincroniza Tarefas.MD com Google Tasks"""
    
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.tasks_service = self._authenticate()
    
    def _authenticate(self):
        """Autentica com Google Tasks API"""
        SCOPES = ['https://www.googleapis.com/auth/tasks']
        credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES
        )
        return build('tasks', 'v1', credentials=credentials)
    
    def parse_tasks_from_markdown(self, file_path: str) -> list:
        """Extrai tarefas de arquivo Markdown"""
        tasks = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar por padrão "- [ ] Descrição da tarefa"
        pattern = r'- \[ \] (.+)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            tasks.append({
                'title': match.group(1).strip(),
                'status': 'needsAction'
            })
        
        return tasks
    
    def sync_to_google_tasks(self, tasks: list, task_list_id: str = "@default"):
        """Sincroniza tarefas para Google Tasks"""
        for task in tasks:
            self.tasks_service.tasks().insert(
                tasklist=task_list_id,
                body={
                    'title': task['title'],
                    'status': task['status']
                }
            ).execute()
        
        print(f"✅ {len(tasks)} tarefas sincronizadas para Google Tasks")

# Exemplo de uso
if __name__ == "__main__":
    sync = GoogleTasksSync(credentials_path=".env.google.json")
    tasks = sync.parse_tasks_from_markdown("Tarefas.MD")
    sync.sync_to_google_tasks(tasks)
```

---

## 📅 Passo 6: Integrar com Google Calendar

Adicionar ao agente para agendar consolidações automáticas:

```python
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class GoogleCalendarIntegration:
    """Agenda eventos de consolidação no Google Calendar"""
    
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.calendar_service = self._authenticate()
    
    def _authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        credentials = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=SCOPES
        )
        return build('calendar', 'v3', credentials=credentials)
    
    def schedule_consolidation(self, 
                              event_name: str = "Prometheus Consolidation",
                              days_ahead: int = 7) -> str:
        """Agenda próxima consolidação no calendário"""
        
        start_time = datetime.utcnow() + timedelta(days=days_ahead)
        end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': event_name,
            'description': 'Consolidar documentação e limpar base de conhecimento',
            'start': {'dateTime': start_time.isoformat() + 'Z'},
            'end': {'dateTime': end_time.isoformat() + 'Z'},
            'reminders': {
                'useDefault': True
            }
        }
        
        event_result = self.calendar_service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        print(f"✅ Consolidação agendada para {start_time.date()}")
        return event_result['id']
```

---

## 🔄 Passo 7: Automatizar Fluxo (main.py atualizado)

Integrar backups automáticos no `main.py`:

```python
# No final de cada execução bem-sucedida:

import os
from backup_to_drive import GoogleDriveBackup
from sync_google_tasks import GoogleTasksSync
from dotenv import load_dotenv

load_dotenv()

# Após processar tarefas com sucesso:

# 1. Fazer backup de documentação importante
backup = GoogleDriveBackup(
    credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    folder_id=os.getenv("GOOGLE_DRIVE_BACKUP_FOLDER_ID")
)
backup.upload_backup("CONSOLIDADO_ESTRATEGICO.md")

# 2. Sincronizar tarefas restantes
sync = GoogleTasksSync(
    credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)
tasks = sync.parse_tasks_from_markdown("Tarefas.MD")
sync.sync_to_google_tasks(tasks)

print("✅ Backup e sincronização completos")
```

---

## 🛡️ Segurança - Checklist

- [ ] `.env` adicionado ao `.gitignore`
- [ ] `.env.google.json` adicionado ao `.gitignore`
- [ ] Credenciais nunca commitar no repositório
- [ ] Usar variáveis de ambiente para produção
- [ ] Rotacionar credenciais a cada 3 meses
- [ ] Monitorar uso no Google Cloud Console

---

## 📊 Verificar Setup

Executar script de teste:

```python
# test_google_integration.py

import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Verificando setup Google...")

# 1. Arquivo .env existe?
if os.path.exists(".env"):
    print("✅ .env encontrado")
else:
    print("❌ .env não encontrado")

# 2. Credenciais JSON existe?
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if os.path.exists(creds_path):
    print(f"✅ Credenciais Google encontradas em {creds_path}")
else:
    print(f"❌ Credenciais não encontradas em {creds_path}")

# 3. Variáveis obrigatórias definidas?
required_vars = [
    "OPENAI_API_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GOOGLE_PROJECT_ID"
]

for var in required_vars:
    if os.getenv(var):
        print(f"✅ {var} definida")
    else:
        print(f"❌ {var} não definida")

print("\n✨ Setup validado!")
```

Executar:
```bash
python test_google_integration.py
```

---

## 🚀 Próximos Passos

1. ✅ Criar credenciais Google Cloud
2. ✅ Configurar `.env`
3. ✅ Instalar pacotes Google
4. ✅ Copiar scripts de backup/sync
5. ✅ Testar integração
6. ⏳ Ativar automação em main.py
7. ⏳ Agendar consolidações semanais

---

**Status:** Ready for implementation  
**Data:** 05-12-2025  
**Próxima revisão:** Após primeiro teste bem-sucedido
