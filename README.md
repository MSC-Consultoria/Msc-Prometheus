# 🔥 Prometheus: Sistema Agêntico Evolutivo Familiar

> **Status**: 🟢 Online (Deploy Ativo) | **Versão**: 2025.12 | **Foco**: Evolução Contínua & Integração Familiar

## 👁️ Visão do Projeto

O **Prometheus** é um ecossistema de Inteligência Artificial projetado para servir toda a família, integrando aprendizado contínuo, automação de tarefas e agentes especializados. O sistema não é estático; ele é **evolutivo**, aprendendo com cada interação e atualizando sua própria base de conhecimento e código.

### 👨‍👩‍👧‍👦 Agentes Familiares (Planejados/Em Desenvolvimento)
*   **Moisés (Admin/Dev)**: Marketing, Criação de Sistemas, Orquestração.
*   **Rebeca**: Foco em estudos (Concurso Detran RJ), integração com sistema de aprendizado.
*   **Valéria**: Gerenciamento de entretenimento (Séries, Filmes, Livros) e trilhas de aprendizado.
*   **Isaias**: Estudos jurídicos (OAB Segunda Fase) e trilhas personalizadas.
*   **Naiara**: Estudos (Concurso Detran RJ) e gestão do "Recanto Estações".
*   **Gabriel**: Gestão "Festeja Kids", "Recanto Estações" e Consultoria MSC.

### 🧬 Agente Evolutivo MSC (Core)
O cérebro do sistema.
*   **Integração Total**: Conecta-se a OpenRouter, Copilot, GitHub.
*   **Formato Juniper**: Padrão de estruturação de conhecimento.
*   **Memória Persistente**: Acumula conhecimento a cada tarefa realizada.
*   **Autonomia**: Conhece e manipula a estrutura de arquivos do projeto.

---

## 🏗️ Arquitetura do Sistema

O sistema opera em uma arquitetura híbrida local/nuvem, com deploy automatizado em VPS.

### Componentes Principais
1.  **Backend (Flask)**: API RESTful localizada em `03_INFRAESTRUTURA/app/backend/api.py`. Gerencia a lógica dos agentes e comunicação com LLMs.
2.  **Frontend (Web)**: Interface moderna em `03_INFRAESTRUTURA/app/frontend/`. Permite interação visual com os agentes e monitoramento de tarefas.
3.  **Infraestrutura (VPS)**: Hospedado na Hostinger (IP: `72.62.9.90`).
4.  **Agentes (Python)**: Classes em `03_INFRAESTRUTURA/app/agents/`. O `EvolutionaryAgent` é a classe base que implementa o ciclo de aprendizado.
5.  **Base de Conhecimento (Markdown)**: O "cérebro" do sistema reside em arquivos Markdown estruturados (`00_ENTRADA`, `01_DOCUMENTACAO_CONSOLIDADA`, etc.), que são lidos e atualizados pelos agentes.

---

## 📂 Mapa de Diretórios

Uma visão detalhada da estrutura do workspace:

| Diretório | Descrição |
| :--- | :--- |
| **📂 Raiz** | Scripts de deploy (`deploy_vps.ps1`), automação Git (`git_setup.ps1`) e arquivos de Tarefas (`Tarefas 06.md`). |
| **📂 00_ENTRADA** | **Input de Dados**. Documentos brutos, novas ideias e especificações iniciais (`README.md` original, `VISUAL_DASHBOARD.md`). |
| **📂 01_DOCUMENTACAO_CONSOLIDADA** | **Memória de Longo Prazo**. Documentação processada e oficializada (`STATUS_PROJETO.md`, `RESUMO_FINAL.md`). |
| **📂 02_DOCUMENTACAO_REFERENCIA** | **Biblioteca**. Manuais, guias externos e definições do "Agente Markdown" e formato Juniper. |
| **📂 03_INFRAESTRUTURA** | **Código Fonte (App)**. Contém o `app/` (backend/frontend), `Dockerfile`, `requirements.txt` e scripts de execução (`run.py`, `main.py`). |
| **📂 04_OPERACIONAL** | **Gestão de Tarefas**. Listas de tarefas ativas, ideias raiz e rascunhos operacionais. |
| **📂 05_ARQUIVO_HISTORICO** | **Arquivo Morto**. Versões antigas e logs de execuções passadas. |
| **📂 06_BACKUPS** | **Segurança**. Backups de credenciais (obsoletas) e dados sensíveis. |
| **📂 07_RELEASES** | **Deployments**. Histórico de pacotes gerados para deploy na VPS. |
| **📂 08_BASES_CONHECIMENTO** | **Templates & Imports**. Modelos para novos documentos e dados importados da web. |
| **📂 09_Moisés** | **Arquivos Pessoais/Empresariais**. Documentos administrativos da Festeja e outros negócios (não faz parte do código do sistema). |

---

## ⚙️ Guia Operacional

### 🚀 Como Rodar Localmente
1.  Navegue até a pasta de infraestrutura:
    ```powershell
    cd 03_INFRAESTRUTURA
    ```
2.  Instale as dependências (se necessário):
    ```powershell
    pip install -r requirements.txt
    ```
3.  Execute o script de inicialização:
    ```powershell
    python run.py
    ```
    *Isso iniciará o Backend e abrirá o Frontend no navegador.*

### ☁️ Como Fazer Deploy (VPS)
O deploy é totalmente automatizado via PowerShell.
1.  Na raiz do projeto, execute:
    ```powershell
    .\deploy_vps.ps1
    ```
2.  O script irá:
    *   Criar um pacote de release em `07_RELEASES`.
    *   Conectar ao VPS (72.62.9.90).
    *   Atualizar a aplicação Dockerizada.
3.  **Acesso**: `http://72.62.9.90`

### 🧠 Como Gerenciar Tarefas
1.  Edite o arquivo `Tarefas XX.md` mais recente (atualmente `Tarefas 06.md`).
2.  Adicione tarefas no formato `- [ ] Descrição da tarefa`.
3.  O Agente Evolutivo lê este arquivo para decidir suas próximas ações.

---

## 📊 Status Atual

*   **✅ Infraestrutura**: Deploy automatizado funcional. VPS configurada.
*   **✅ Core**: Agente Evolutivo implementado (`evolutionary_agent.py`).
*   **✅ Interface**: Dashboard Web básico disponível.
*   **🚧 Agentes Familiares**: Em fase de definição e integração (ver `Tarefas 06.md`).
*   **🚧 Sistema de Aprendizado**: Integração com trilhas personalizadas em desenvolvimento.

---
*Gerado automaticamente pelo GitHub Copilot em 05/12/2025.*
