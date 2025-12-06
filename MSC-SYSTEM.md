# 🏢 MSC SYSTEM - Prometheus

**Visão Corporativa do Sistema Prometheus**
**Organização:** MSC Consultoria
**Data:** Dezembro 2025

---

## 🎯 O que é o MSC System?

O **MSC System** (Moisés Santos Consultoria System) é a plataforma de inteligência artificial desenvolvida para suportar todas as operações da MSC e suas empresas associadas. O **Prometheus** é o núcleo central deste ecossistema.

---

## 🌐 Ecossistema MSC

```
                    ┌─────────────────┐
                    │   PROMETHEUS    │
                    │  (Núcleo IA)    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼────┐         ┌────▼────┐
   │ FAMÍLIA │         │ NEGÓCIOS │         │ PESSOAL │
   └────┬────┘         └────┬─────┘         └────┬────┘
        │                   │                    │
   ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
   │ Valéria │         │ Festeja │         │ Moisés  │
   │ Rebeca  │         │ Recanto │         │ Admin   │
   │ Isaias  │         │   MSC   │         │ Dev     │
   │ Naiara  │         └─────────┘         └─────────┘
   │ Gabriel │
   └─────────┘
```

---

## 🏛️ Pilares Estratégicos

### 1. 🏠 Família Primeiro
O sistema foi desenhado para servir toda a família Santos, oferecendo:

| Membro | Foco Principal | Agente Dedicado |
|--------|----------------|-----------------|
| **Moisés** | Gestão, Tecnologia | Admin/Dev |
| **Valéria** | Entretenimento, Cultura | Curador |
| **Isaias** | Direito, OAB | Jurídico |
| **Rebeca** | Concurso Detran RJ | Estudos |
| **Naiara** | A definir | Assistente |
| **Gabriel** | A definir | Assistente |

### 2. 💼 Negócios Integrados

#### Festeja Kids 🎉
- **Objetivo:** Gestão de eventos infantis
- **Integração:** CRM, Calendário, Pagamentos
- **Status:** Planejado

#### Recanto Estações 🌿
- **Objetivo:** Gestão do espaço de eventos
- **Integração:** Reservas, Manutenção, Financeiro
- **Status:** Planejado

#### MSC Consultoria 📊
- **Objetivo:** Consultoria em TI e processos
- **Integração:** Portal do cliente, Projetos
- **Status:** Em desenvolvimento

### 3. 📚 Ensino Gamificado

Sistema inspirado nos melhores cursos online (Alura, Estratégia):

```
┌─────────────────────────────────────────────────┐
│                 SISTEMA DE ENSINO               │
├─────────────────────────────────────────────────┤
│  📊 Níveis     │  🔥 Streaks    │  ⭐ XP       │
│  Beginner      │  Dias seguidos │  Pontos por  │
│  Intermediate  │  de estudo     │  atividade   │
│  Advanced      │                │              │
├─────────────────────────────────────────────────┤
│  🎯 Trilhas Personalizadas por Objetivo         │
│  📈 Métricas de Progresso                       │
│  🏆 Conquistas e Badges                         │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Arquitetura Técnica

### Componentes Core

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                       │
│  ┌─────────────────────────────────────────┐    │
│  │ Dashboard │ Login │ Família │ Agentes   │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                   BACKEND                        │
│  ┌─────────────────────────────────────────┐    │
│  │ Flask API │ Auth │ OpenRouter │ Deploy  │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              LLM PROVIDERS (OpenRouter)          │
│  ┌─────────────────────────────────────────┐    │
│  │ Claude │ GPT-4o │ DeepSeek │ Llama 3    │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Infraestrutura

| Recurso | Especificação | Custo/mês |
|---------|---------------|-----------|
| VPS Hostinger | Ubuntu 24.04, 2GB RAM | ~R$30 |
| Domínio (futuro) | .com.br | ~R$40/ano |
| OpenRouter | Pay-per-use | ~$10 |

---

## 📊 Métricas de Sucesso MSC

### KPIs Operacionais

| Métrica | Atual | Meta Q1/26 |
|---------|-------|------------|
| Uptime | 95% | 99.5% |
| Usuários Familiares | 7 | 7 |
| Tarefas IA/dia | 5 | 50 |
| Deploys automáticos | 10 | 100 |

### KPIs de Negócio

| Métrica | Status | Meta |
|---------|--------|------|
| Economia de tempo (horas/mês) | - | 20h |
| Automações ativas | 2 | 10 |
| Integrações externas | 1 | 5 |

---

## 🔐 Governança e Segurança

### Níveis de Acesso

| Nível | Usuário | Permissões |
|-------|---------|------------|
| Admin | Moisés | Tudo |
| User | Família | Dashboard, Agentes |
| API | Serviços | Endpoints específicos |

### Políticas

1. **Dados Sensíveis:** Armazenados em `/06_BACKUPS/SENSIVEL/`
2. **Credenciais:** Nunca em código, sempre em `.env`
3. **Backups:** Diários para documentação
4. **Logs:** Rotação semanal

---

## 🗓️ Roadmap MSC

### 2025 Q4 (Dezembro) ✅ Em progresso
- [x] Deploy inicial Prometheus
- [x] Sistema de login familiar
- [x] Integração OpenRouter
- [ ] Testes completos do agente

### 2026 Q1 (Janeiro-Março)
- [ ] Agentes especializados (Rebeca, Valéria, Isaias)
- [ ] Integração Festeja/Recanto
- [ ] Mobile responsivo

### 2026 Q2 (Abril-Junho)
- [ ] Sistema de ensino gamificado
- [ ] API pública MSC
- [ ] Dashboards de negócio

---

## 📞 Suporte e Contato

### Desenvolvimento
- **Repositório:** GitHub (privado)
- **Deploy:** Automatizado via PowerShell

### Produção
- **VPS:** 72.62.9.90
- **Acesso:** Dashboard web

---

## 📜 Histórico de Decisões

| Data | Decisão | Motivo |
|------|---------|--------|
| 2025-12-05 | Escolha Hostinger | Custo-benefício, facilidade |
| 2025-12-06 | OpenRouter como gateway | Multi-provider, flexibilidade |
| 2025-12-06 | Senha padrão família | Simplicidade inicial |
| 2025-12-06 | Flask over FastAPI | Familiaridade, rapidez |

---

## 🌟 Visão de Futuro

> "O MSC System é mais do que software - é a ponte entre tecnologia e vida familiar, conectando aprendizado, trabalho e lazer em uma experiência única."

**Objetivo 2026:** Cada membro da família com seu agente personalizado, automações que economizam tempo, e um sistema que cresce junto com a família.

---

**Documento Confidencial - MSC Consultoria**
**Versão 1.0 - Dezembro 2025**
