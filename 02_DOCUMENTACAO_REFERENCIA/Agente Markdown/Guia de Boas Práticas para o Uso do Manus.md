# Guia de Boas Práticas para o Uso do Manus

## Introdução

Este guia apresenta um conjunto de boas práticas e recomendações para utilizar a plataforma Manus de forma eficiente e econômica. Adotar estas estratégias permitirá que você maximize a produtividade, otimize o consumo de créditos e aproveite ao máximo os recursos disponíveis. As práticas aqui descritas foram compiladas a partir da documentação oficial e de artigos técnicos publicados pela equipe do Manus.

## Gestão de Créditos e Custos

A plataforma Manus opera com um sistema baseado em créditos, onde o consumo está atrelado à complexidade de cada tarefa. Uma gestão consciente dos créditos é fundamental para um uso sustentável e econômico da ferramenta.

### Otimizando o Consumo de Créditos

Para garantir o uso mais eficiente dos seus créditos, é crucial adotar uma abordagem estratégica ao definir e executar tarefas. A tabela abaixo resume as principais táticas que podem ser empregadas para reduzir o consumo de créditos sem comprometer a qualidade dos resultados.

| Estratégia | Descrição |
| :--- | :--- |
| **Ser Específico** | Instruções claras e detalhadas diminuem a necessidade de iterações, economizando créditos. Em vez de "Pesquise sobre IA", use "Crie um relatório sobre as 5 principais tendências de IA na saúde em 2024". [1] |
| **Agrupar Tarefas** | Combine tarefas similares em uma única solicitação para reduzir a sobrecarga e o consumo de créditos. [2] |
| **Revisar Resultados** | Em projetos complexos com múltiplas fases, revise os resultados intermediários antes de prosseguir para evitar desperdício de créditos em trabalhos que precisam de ajuste. [1] |
| **Simplificar Instruções** | Forneça instruções concisas e diretas, evitando elaborações desnecessárias ou frases duplicadas. [2] |

É igualmente importante **monitorar o uso de créditos** através do painel de controle da sua conta. A plataforma oferece ferramentas para visualizar o saldo atual, o histórico de consumo e um detalhamento dos gastos por tipo de tarefa, além de alertas para níveis baixos de crédito. [1]

## Eficiência e Produtividade

Além da gestão de custos, a forma como você interage com o Manus impacta diretamente a eficiência e a qualidade do trabalho realizado. Boas práticas de "engenharia de prompt" e o uso correto das ferramentas são essenciais.

### Maximizando a Eficácia das Solicitações

O sucesso de uma tarefa no Manus começa com a qualidade da sua solicitação. Prompts bem elaborados e o uso adequado dos modos de operação podem acelerar a conclusão das tarefas e melhorar os resultados.

| Prática | Descrição |
| :--- | :--- |
| **Escolher o Agente Certo** | Utilize o **Modo Chat** para perguntas rápidas e tarefas simples, que consomem menos créditos. Reserve o **Modo Agente** para tarefas complexas que exigem autonomia e múltiplos passos. [1] |
| **Combinar Perguntas** | Agrupe questões relacionadas em uma única tarefa. Por exemplo, em vez de perguntar separadamente sobre formatação e salvamento de um arquivo, combine tudo em uma única consulta. [2] |
| **Reduzir Tentativas** | Evite perguntar variações da mesma questão repetidamente. Se um resultado não for o esperado, refine a pergunta com base na resposta inicial em vez de simplesmente reformulá-la. [2] |

## Práticas Técnicas Avançadas

Para usuários que buscam otimizar o desempenho em um nível mais técnico, a **engenharia de contexto** é um conceito crucial. Ela se refere à maneira como as informações são estruturadas e enviadas ao modelo de linguagem para maximizar a eficiência do cache e a consistência das respostas.

> A engenharia de contexto é a prática de estruturar o histórico de interações de forma a maximizar a reutilização de computação (cache) e guiar o modelo de forma mais eficaz em direção ao objetivo desejado. [3]

As práticas a seguir são especialmente relevantes para desenvolvedores e usuários avançados que interagem com a API do Manus ou constroem agentes sobre a plataforma.

| Prática Técnica | Descrição |
| :--- | :--- |
| **Prefixo de Prompt Estável** | Mantenha a parte inicial do seu prompt (system prompt) consistente entre as chamadas. A inclusão de dados dinâmicos, como um timestamp, pode invalidar o cache e aumentar o custo computacional. [3] |
| **Contexto Append-Only** | Evite modificar ações ou observações anteriores no histórico da conversa. Adicione novas informações ao final do contexto para preservar a integridade do cache. [3] |
| **Serialização Determinística** | Garanta que a ordem das chaves em objetos JSON seja estável durante a serialização, pois inconsistências podem quebrar o cache silenciosamente. [3] |

## Conclusão

O uso eficiente e econômico do Manus é alcançado através de uma combinação de planejamento cuidadoso, interações claras e o aproveitamento das ferramentas de monitoramento. Ao ser específico em suas solicitações, agrupar tarefas relacionadas e revisar os resultados intermediários, você pode reduzir significativamente o consumo de créditos. Para usuários avançados, a aplicação de técnicas de engenharia de contexto oferece uma camada adicional de otimização, garantindo o máximo de desempenho e economia.

## Referências

[1] Manus. (s.d.). *Plans and Pricing*. Documentação Oficial. Recuperado de https://manus.im/docs/introduction/plans
[2] Manus. (s.d.). *How to optimize my credit usage?*. Manus Help Center. Recuperado de https://help.manus.im/en/articles/12087847-how-to-optimize-my-credit-usage
[3] Manus. (2025, 18 de julho). *Context Engineering for AI Agents: Lessons from Building Manus*. Blog. Recuperado de https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
