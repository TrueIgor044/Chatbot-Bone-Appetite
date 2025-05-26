

#Bone Appetite Restaurante e Pizzaria


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
* **Geração de comprovante em PDF** com detalhes do pedido para download.
* Interface em formato de **chatbot interativo** para o cliente.


## Estrutura do Projeto

restaurante_app/
├── .venv/ # Ambiente virtual
├── src/ # Código fonte da aplicação, dividido em módulos
│ ├── init.py # Torna 'src' um pacote Python
│ ├── db.py # Lógica de interação com o banco de dados SQLite
│ ├── models.py # Definições de modelos (Produto, Cliente, Pedido, ItemPedido, LinkedList)
│ ├── logic.py # Lógica de negócio (processamento de pedidos, recomendações, geração de PDF)
│ └── app.py # Aplicação principal e interface Gradio
├── data/ # Pasta para armazenar o arquivo do banco de dados SQLite e PDFs gerados
│ └── restaurante.db # (Será criado automaticamente na primeira execução)
│ └── *.pdf # (Comprovantes PDF serão salvos aqui)
├── .gitignore # Arquivos e pastas a serem ignorados pelo controle de versão (Git)
├── requirements.txt # Lista as dependências do projeto Python
└── README.md # Este arquivo, com instruções de uso


## Como Rodar a Aplicação


Siga os passos abaixo para configurar e executar a aplicação na sua máquina. **É crucial seguir a ordem e as instruções específicas para o seu sistema operacional.**


1.  **Pré-requisitos e Configurações Iniciais:**


    * **Python 3.x:** Certifique-se de ter o Python 3 instalado. **É CRUCIAL instalar o Python oficial (do [python.org/downloads/](https://www.python.org/downloads/)) e, DURANTE A INSTALAÇÃO, MARCAR A CAIXA "Add Python to PATH" na primeira tela do instalador.**
    * **Git:** Para clonar este repositório e usar controle de versão, o Git precisa estar instalado. Baixe em [git-scm.com/downloads](https://git-scm.com/downloads) e siga as instruções, certificando-se de que o Git seja adicionado ao PATH.
    * **VS Code (Recomendado):** Para uma melhor experiência de desenvolvimento.


2.  **Clone o Repositório:**


    * Abra seu Terminal/Prompt de Comando (ou o Terminal integrado do VS Code) e execute:
        ```bash
        git clone [https://github.com/TrueIgor044/Chatbot-Bone-Appetite.git](https://github.com/TrueIgor044/Chatbot-Bone-Appetite.git)
        ```
    * Navegue até a pasta do projeto:
        ```bash
        cd Chatbot-Bone-Appetite
        ```
    * *(Se você baixou os arquivos manualmente, apenas navegue até a pasta raiz do projeto no seu terminal: `cd C:\caminho\para\sua\pasta\Chatbot-Bone-Appetite`)*


3.  **Abra a Pasta Raiz do Projeto no VS Code:**


    * No VS Code, vá em `File` > `Open Folder...` e selecione a pasta `Chatbot-Bone-Appetite`.


4.  **Abra o Terminal Integrado do VS Code:**


    * No menu superior do VS Code, vá em `Terminal` > `Novo Terminal`. O terminal abrirá automaticamente na pasta raiz do seu projeto. **Você pode usar o PowerShell (padrão no Windows) sem problemas para todos os comandos.**


5.  **(Windows apenas) Ajuste a Política de Execução do PowerShell:**


    * **Este passo é essencial no Windows** para permitir a execução do script de ativação do ambiente virtual (`activate.ps1`).
    * Feche o terminal do VS Code que está aberto.
    * Abra o **PowerShell como Administrador** (Pesquise "PowerShell" no menu Iniciar, clique com o botão direito sobre ele > "Executar como administrador").
    * No PowerShell de administrador, digite o comando **exatamente como mostrado** e pressione Enter:
        ```powershell
        Set-ExecutionPolicy RemoteSigned
        ```
    * Digite `S` (Sim) e Enter para confirmar.
    * Feche o PowerShell de administrador.
    * Reabra o terminal no VS Code (Passo 4 novamente).


6.  **Crie o Ambiente Virtual:**


    * No terminal do VS Code, digite:
        ```bash
        python -m venv .venv
        ```


7.  **Ative o Ambiente Virtual:**


    * No terminal do VS Code, digite o comando de ativação apropriado para o seu sistema operacional:
        * **No Windows (PowerShell):**
            ```bash
            .\.venv\Scripts\activate
            ```
        * **No macOS/Linux:**
            ```bash
            source ./.venv/bin/activate
            ```
        * Você verá `(.venv)` no início da linha de comando, indicando que o ambiente está ativado.


8.  **Instale as Dependências:**


    * Com o ambiente virtual ativado, instale as bibliotecas necessárias listadas no `requirements.txt`.
        ```bash
        pip install -r requirements.txt
        ```


9.  **Execute a Aplicação:**


    * **IMPORTANTE:** Para que as importações relativas entre os módulos (`src/`) funcionem corretamente, execute a aplicação como um módulo Python:
        ```bash
        python -m src.app
        ```


        Após a execução, o Gradio iniciará um servidor local e fornecerá um link (geralmente `http://127.0.0.1:7860/`) que você pode abrir no seu navegador web. A aplicação estará pronta para uso!


## Solução de Problemas Comuns


Enfrentando outros problemas? Consulte estas soluções:


### 1. `Python não foi encontrado; executar sem argumentos para instalar do Microsoft Store...`


* **Causa:** O Python não está instalado corretamente ou não está no PATH do sistema.
* **Solução:** Siga o **Passo 1 dos Pré-requisitos** (instalação do Python oficial e adição ao PATH).


### 2. `ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements.txt'`


* **Causa:** O arquivo `requirements.txt` não está na pasta correta, ou o nome está incorreto (ex: `requirements.txt.txt`), ou o terminal não está na pasta raiz do projeto.
* **Solução:**
    1.  **Verifique a localização:** No seu explorador de arquivos (não no VS Code), vá até a pasta `Chatbot-Bone-Appetite`. O `requirements.txt` deve estar diretamente aqui.
    2.  **Verifique a extensão oculta:** No Explorador de Arquivos do Windows, vá em `Exibir` > marque `Extensões de nome de arquivo`. Certifique-se de que o arquivo se chama `requirements.txt` (sem extensão extra como `.txt`). Se não, renomeie-o.
    3.  **Recrie o arquivo (se necessário):** Se houver dúvidas, **exclua o `requirements.txt` atual** e **crie um novo arquivo** (clicando com o botão direito na pasta `Chatbot-Bone-Appetite` no VS Code Explorer > New File) chamado **exatamente** `requirements.txt`. Cole apenas `gradio` e `fpdf2` dentro e salve.
    4.  **Confirme o diretório do terminal:** No terminal do VS Code, o prompt deve ser `PS C:\caminho\para\sua\pasta\Chatbot-Bone-Appetite>`. Se não for, feche e reabra o terminal, ou use `cd C:\caminho\para\sua\pasta\Chatbot-Bone-Appetite`.
    5.  Tente `pip install -r requirements.txt` novamente.


### 3. `Fatal error in launcher: Unable to create process using "..." O sistema não pode encontrar o arquivo especificado.`


* **Causa:** Você moveu a pasta do projeto *depois* de criar o ambiente virtual, ou o `.venv` está corrompido. O ambiente virtual ainda "aponta" para o caminho antigo.
* **Solução:**
    1.  Feche o terminal do VS Code.
    2.  No explorador de arquivos do VS Code, **exclua a pasta `.venv`** (clicando com o botão direito > Excluir).
    3.  Abra um novo terminal no VS Code (ele deve estar na pasta raiz do projeto).
    4.  Recrie o ambiente virtual: `python -m venv .venv`.
    5.  Ative-o novamente: `.\.venv\Scripts\activate`.
    6.  Tente instalar as dependências.


### 4. `git : O termo 'git' não é reconhecido como nome de cmdlet...`


* **Causa:** O Git não está instalado no seu sistema, ou não foi adicionado ao PATH durante a instalação.
* **Solução:** Siga o **Passo 1 dos Pré-requisitos** (instalação do Git e adição ao PATH).


### 5. `Author identity unknown` ou `fatal: unable to auto-detect email address...`


* **Causa:** Você não configurou sua identidade Git (nome e e-mail) localmente.
* **Solução:**
    1.  No terminal, configure sua identidade (use o e-mail e nome da sua conta GitHub):
        ```bash
        git config --global user.email "seu@email.com"
        git config --global user.name "Seu Nome"
        ```
    2.  Tente o comando `git commit` novamente.


### 6. `error: src refspec main does not match any` (ao fazer `git push`)


* **Causa:** Não há commits na branch `main` local para serem enviados para o GitHub, ou você pulou o `git commit`.
* **Solução:**
    1.  Certifique-se de que todos os arquivos desejados estejam na área de preparação:
        ```bash
        git add .
        ```
    2.  Crie o commit (este passo é crucial):
        ```bash
        git commit -m "Sua mensagem de commit aqui"
        ```
    3.  Após o commit, se a branch local não for `main`, renomeie-a: `git branch -M main`.
    4.  Tente `git push -u origin main` novamente.

