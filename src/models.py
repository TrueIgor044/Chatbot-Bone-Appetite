# src/models.py

class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

# Lista de produtos (cardápio fixo, em memória)
produtos = [
    Produto(1, "Pizza Margherita", 30.0),
    Produto(2, "Pizza Calabresa", 35.0),
    Produto(3, "Refrigerante", 8.0),
    Produto(4, "Água", 5.0),
    Produto(5, "Pizza Quatro Queijos", 40.0),
    Produto(6, "Batata Frita", 7.0)
]

# --- Implementação da Lista Encadeada ---

class Node:
    """Representa um nó na lista encadeada."""
    def __init__(self, data):
        self.data = data  # O dado armazenado no nó
        self.next = None  # Ponteiro para o próximo nó

class LinkedList:
    """
    Implementação de uma Lista Encadeada Simples.
    Usada para gerenciar os itens dentro de um pedido antes de serem persistidos.
    """
    def __init__(self):
        self.head = None  # O primeiro nó da lista
        self.tail = None  # O último nó da lista (otimiza inserção no final para O(1))
        self.size = 0     # Tamanho da lista

    def append(self, data):
        """
        Adiciona um novo nó ao final da lista (Algoritmo de Inserção no Final).
        Complexidade: O(1) se mantivermos o ponteiro `tail`.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def __iter__(self):
        """Permite iterar sobre a lista encadeada (ex: for item in lista_encadeada)."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        """Retorna o número de elementos na lista (len(lista_encadeada))."""
        return self.size

    def to_list(self):
        """Converte a lista encadeada para uma lista Python nativa."""
        return list(self)

class ItemPedido:
    """Representa um item individual dentro de um pedido."""
    def __init__(self, produto_id, nome_produto, preco_unitario, quantidade=1):
        self.produto_id = produto_id
        self.nome_produto = nome_produto
        self.preco_unitario = preco_unitario
        self.quantidade = quantidade
        self.subtotal = preco_unitario * quantidade

    def __repr__(self):
        return f"ItemPedido(ID: {self.produto_id}, Nome: {self.nome_produto}, Preço: {self.preco_unitario:.2f}, Qtd: {self.quantidade})"

class Pedido:
    """Representa um pedido completo de um cliente."""
    def __init__(self, cliente_id, forma_pagamento):
        self.cliente_id = cliente_id
        self.forma_pagamento = forma_pagamento
        self.itens = LinkedList()  # Usa a lista encadeada para os itens do pedido
        self.total = 0.0
        # data_pedido será preenchido automaticamente pelo DB ou no momento da criação
        # Ex: self.data_pedido = datetime.datetime.now() se não for do DB

    def add_item(self, produto_id, nome_produto, preco_unitario, quantidade=1):
        """Adiciona um ItemPedido à lista encadeada de itens do pedido e atualiza o total."""
        item = ItemPedido(produto_id, nome_produto, preco_unitario, quantidade)
        self.itens.append(item)
        self.total += item.subtotal

    def __repr__(self):
        return f"Pedido(Cliente ID: {self.cliente_id}, Total: R$ {self.total:.2f}, Itens: {len(self.itens)})"