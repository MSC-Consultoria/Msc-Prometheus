# Projeto: Demonstração da Linguagem Agêntica (AML)

> **Contexto:** Você é um Desenvolvedor Fullstack Sênior e especialista em UI/UX. Estamos criando um protótipo de um "Cartão de Perfil" (Profile Card) para demonstrar as capacidades desta linguagem de programação baseada em Markdown. O design deve ser moderno, "glassmorphism" e responsivo.

## 📘 Documentação da Sintaxe (Para o Humano)
*Isso é apenas para referência, o agente ignorará esta seção se não estiver nas tarefas.*

1.  **Tarefas:** Use `- [ ]` para criar uma instrução.
2.  **Criar Arquivos:** O agente deve usar ```lang:caminho/arquivo ... ```.
3.  **Ler Arquivos:** Use `{ler:pasta/arquivo.ext}` dentro da descrição da tarefa para dar contexto ao agente.
4.  **Logs:** O agente escreverá o resultado automaticamente abaixo de cada tarefa.

---

## 🚀 Fila de Execução

### Fase 1: Estrutura Inicial

- [ ] Crie a estrutura de pastas e um arquivo `demo/index.html`. Ele deve conter um container centralizado e importar uma fonte bonita do Google Fonts (Inter ou Poppins). Deixe o `body` com fundo preto por enquanto.
- [ ] Crie um arquivo CSS em `demo/style.css`. Adicione um reset básico e estilos para centralizar o conteúdo na tela usando Flexbox.

### Fase 2: Iteração e Design (O Teste de Leitura)

- [ ] Agora vamos estilizar o cartão. {ler:demo/index.html} {ler:demo/style.css}
    Com base nos arquivos lidos, atualize o `demo/style.css` para criar um efeito de "Glassmorphism" no container (fundo translúcido, borda sutil, sombra, blur). Mantenha o que já existia de layout.
    
- [ ] O cliente mudou de ideia sobre o fundo preto. {ler:demo/style.css}
    Atualize o `demo/style.css` mudando o `background` do body para um gradiente linear moderno (roxo para azul). **Não perca o efeito de glassmorphism criado anteriormente.**

### Fase 3: Scripting

- [ ] Crie um script `demo/script.js`. Ele deve adicionar um efeito de "tilt" (inclinação 3D) no cartão quando o mouse passa por cima. Use lógica matemática simples, sem bibliotecas externas.
- [ ] Conecte o script novo no HTML. {ler:demo/index.html}
    Reescreva o `demo/index.html` adicionando a tag `<script src="script.js"></script>` antes do fechamento do body.

## 📝 Logs do Sistema
*(O sistema preencherá abaixo automaticamente)*