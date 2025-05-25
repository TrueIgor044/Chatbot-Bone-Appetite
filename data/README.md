# Fredy Restaurante e Pizzaria

Esta é uma aplicação web simples para gerenciamento de pedidos de um restaurante/pizzaria, construída com Python, SQLite e Gradio.

## Funcionalidades

* Cadastro e identificação de clientes por telefone.
* Exibição de cardápio com itens e preços.
* Processamento de pedidos com seleção de múltiplos itens.
* Cálculo do valor total do pedido.
* Registro do último item de comida pedido pelo cliente para recomendações futuras.
* Sistema de recomendação básico baseado no último item pedido.
* Uso de **lista encadeada** para gerenciar itens de pedido internamente no objeto `Pedido`.
* Persistência de clientes e **histórico completo de pedidos** em um banco de dados SQLite local.

## Estrutura do Projeto

\`\`\`
restaurante\_app/
├── .venv/                  # Ambiente virtual
├── src/                    # Código fonte da aplicação, dividido em módulos
│   ├── \_\_init\_\_.py         # Torna 'src' um pacote Python
│   ├── db.py               # Lógica de interação com o banco de dados SQLite
│   ├── models.py           # Definições de modelos (Produto, Cliente, Pedido, ItemPedido, LinkedList)
│   ├── logic.py            # Lógica de negócio (processamento de pedidos, recomendações)
│   └── app.py              # Aplicação principal e interface Gradio
├── data/                   # Pasta para armazenar o arquivo do banco de dados SQLite
│   └── restaurante.db      # (Será criado automaticamente na primeira execução)
├── .gitignore              # Arquivos e pastas a serem ignorados pelo controle de versão (Git)
├── requirements.txt        # Lista as dependências do projeto Python
└── README.md               # Este arquivo, com instruções de uso
\`\`\`

## Como Rodar a Aplicação

Siga os passos abaixo para configurar e executar a aplicação na sua máquina:

1.  **Abra a pasta raiz do projeto (`restaurante_app`) no VS Code.**

2.  **Abra o Terminal Integrado do VS Code:**
    * No menu superior do VS Code, vá em `Terminal` > `Novo Terminal`.

3.  **Crie um Ambiente Virtual:**
    * No terminal do VS Code, digite:
        \`\`\`bash
        python -m venv .venv
        \`\`\`

4.  **Ative o Ambiente Virtual:**
    * No terminal do VS Code, digite o comando de ativação apropriado para o seu sistema operacional:
        * **No Windows (PowerShell):**
            \`\`\`bash
            .\\.venv\\Scripts\\activate
            \`\`\`
        * **No macOS/Linux:**
            \`\`\`bash
            source ./.venv/bin/activate
            \`\`\`
        * Você verá `(.venv)` no início da linha de comando, indicando que o ambiente está ativado.

5.  **Instale as Dependências:**
    * Com o ambiente virtual ativado, instale as bibliotecas necessárias listadas no `requirements.txt`.
        \`\`\`bash
        pip install -r requirements.txt
        \`\`\`

6.  **Execute a Aplicação:**
    * **IMPORTANTE:** Para que as importações relativas funcionem corretamente, execute a aplicação como um módulo:
        \`\`\`bash
        python -m src.app
        \`\`\`

        Após a execução, o Gradio iniciará um servidor local e fornecerá um link (geralmente `http://127.0.0.1:7860/`) que você pode abrir no seu navegador web. A aplicação estará pronta para uso!

## Observações Importantes

* **Banco de Dados Local:** Esta versão usa um banco de dados **SQLite local** (`restaurante.db` na pasta `data/`). Cada vez que você rodar a aplicação em uma nova máquina (sem copiar o arquivo `.db`), um novo banco de dados vazio será criado. Isso significa que os dados de clientes e pedidos **não serão compartilhados** entre diferentes máquinas.
* **Lista Encadeada:** A lista encadeada é usada internamente para gerenciar os `ItemPedido`s dentro de um objeto `Pedido` antes que ele seja salvo no banco de dados. Para persistência, os dados são salvos em tabelas relacionais (`pedidos` e `item_pedidos`).