# src/db.py
import sqlite3
import os
from .models import Pedido, ItemPedido # Importa os novos modelos de Pedido e ItemPedido

# Define o caminho para o arquivo do banco de dados na pasta data/
# os.path.dirname(__file__) -> src/
# os.path.dirname(os.path.dirname(__file__)) -> restaurante_app/
# os.path.join(...) -> restaurante_app/data/restaurante.db
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'restaurante.db')

def get_connection():
    """Retorna uma nova conexão com o banco, permitindo uso em múltiplas threads."""
    # Garante que a pasta 'data' exista antes de tentar criar o DB
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela clientes (existente)
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT,
            telefone TEXT UNIQUE,
            ultima_comida TEXT
        )
        '''
    )
    
    # Nova tabela para Pedidos
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            forma_pagamento TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
        '''
    )
    
    # Nova tabela para Itens de Pedido
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS item_pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome_produto TEXT NOT NULL,
            preco_unitario REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
        '''
    )
    conn.commit()
    conn.close()

# Cria o banco de dados e as tabelas assim que o módulo é carregado
init_db()

# --------- Funções de Acesso ao Cliente ---------
def get_client_by_phone(telefone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, endereco, telefone, ultima_comida FROM clientes WHERE telefone = ?",
        (telefone,)
    )
    cliente = cursor.fetchone()
    conn.close()
    return cliente

def create_client(nome, endereco, telefone):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (nome, endereco, telefone) VALUES (?, ?, ?)",
            (nome, endereco, telefone)
        )
        conn.commit()
        cliente_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Se o telefone já existe, retorna o ID do cliente existente
        cliente = get_client_by_phone(telefone)
        cliente_id = cliente[0] if cliente else None
    finally:
        conn.close()
    return cliente_id

def update_last_food(cliente_id, comida):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clientes SET ultima_comida = ? WHERE id = ?",
        (comida, cliente_id)
    )
    conn.commit()
    conn.close()

# --------- Funções de Acesso ao Pedido ---------
def save_pedido(pedido: Pedido):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Insere o pedido principal na tabela 'pedidos'
        cursor.execute(
            "INSERT INTO pedidos (cliente_id, total, forma_pagamento) VALUES (?, ?, ?)",
            (pedido.cliente_id, pedido.total, pedido.forma_pagamento)
        )
        pedido_id = cursor.lastrowid # Pega o ID do pedido recém-inserido

        # Insere os itens do pedido na tabela 'item_pedidos'
        # A iteração é feita sobre a lista encadeada 'pedido.itens'
        for item in pedido.itens:
            cursor.execute(
                "INSERT INTO item_pedidos (pedido_id, produto_id, nome_produto, preco_unitario, quantidade) VALUES (?, ?, ?, ?, ?)",
                (pedido_id, item.produto_id, item.nome_produto, item.preco_unitario, item.quantidade)
            )
        conn.commit()
        return pedido_id
    except sqlite3.Error as e:
        print(f"Erro ao salvar pedido: {e}")
        conn.rollback() # Desfaz todas as operações se houver erro
        return None
    finally:
        conn.close()