import sqlite3
from datetime import datetime

# Definimos o nome do arquivo do banco de dados como uma constante
DB_FILE = 'quiosque.db'


def criar_tabelas():
    """
    FUnção para criar as tabelas iniciais do banco de dados,
    caso elas ainda não existam 
    """
    print('Verificando e criando tabelas, se necessari...')
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categorias  
                (
                id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_categoria TEXT UNIQUE NOT NULL
                );
            """)

            print('Tabela categoria pronta')

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos 
                (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome_produto TEXT UNIQUE NOT NULL, 
                preco REAL NOT NULL,
                quantidade_estoque INTEGER NOT NULL, 
                id_categoria INTEGER NOT NULL,
                FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vendas
                (
                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora DATETIME,
                valor_total REAL NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS itens_da_venda
                (
                id_venda INTEGER NOT NULL,
                id_produto INTEGER NOT NULL,
                quantidade INTEGER,
                preco_unitario REAL,
                FOREIGN KEY (id_venda) REFERENCES vendas(id_venda),
                FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
                PRIMARY KEY (id_venda, id_produto)
                )
            """)
            connection.commit()
            return True

    except sqlite3.Error as e:
        print(f'Ocorreu um erro ao criar tabelas: {e}')
        return False


def adicionar_categoria(nome_categoria):
    """Adiciona uma nova categoria ao banco de dados"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO categorias (nome_categoria) VALUES (?)
            """, (nome_categoria,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao inserir dados na tebela categorias: {e}')
            return False


def listar_categorias():
    """Retorna uma lista de todas as categorias cadastradas"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT id_categoria, nome_categoria FROM categorias
            """)
            categorias_listadas = cursor.fetchall()
            return categorias_listadas
        except sqlite3.Error as e:
            print(f'Erro ao listar categorias: {e}')
            return []


# FUnções crud para 'produtos'
def adicionar_produto(nome_produto, preco, quantidade_estoque, id_categoria):
    """Adiciona um novo produto ao banco de dados"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO produtos (nome_produto, preco, quantidade_estoque, id_categoria) VALUES (?, ?, ?, ?)
            """, (nome_produto, preco, quantidade_estoque, id_categoria,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao inserir produto na tabela produtos: {e}')
            return False

def listar_produtos():
    """Retorna uma lista de todos os produtos com o nome da categoria (usando JOIN)"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT p.id_produto, p.nome_produto, p.preco, p.quantidade_estoque, c.nome_categoria FROM produtos AS p
                JOIN categorias AS c
                ON p.id_categoria = c.id_categoria
            """)
            produtos_listados = cursor.fetchall()
            return produtos_listados
        except sqlite3.Error as e:
            print(f'Erro ao listar produtos: {e}')
            return []
        
def listar_produtos_por_categoria(id_categoria):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT id_produto, nome_produto, preco, quantidade_estoque FROM produtos
                WHERE id_categoria = (?)
            """, (id_categoria,))
            produtos_listados_por_categoria = cursor.fetchall()
            return produtos_listados_por_categoria
        except sqlite3.Error as e:
            print(f'Erro ao listar produtos: {e}')
            return []

def atualizar_estoque_produto(nova_quantidade, id_produto):
    """Atualiza o estoque de um produto especifico"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE produtos
                SET quantidade_estoque = (?)
                WHERE id_produto = (?)
            """,(nova_quantidade, id_produto,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao modificar quantidade_estoque: {e}')
            return False

def atualizar_preco_produto(novo_preco, id_produto):
    """Atualia o preço do produto especifico"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE produtos
                SET preco = (?)
                WHERE id_produto = (?)
            """,(novo_preco, id_produto,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao modificar preco: {e}')
            return False

def atualizar_nome_produto(novo_nome, id_produto):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                UPDATE produtos
                SET nome_produto = (?)
                WHERE id_produto = (?)
            """,(novo_nome, id_produto,))
            connection.commit()
            return True
        except sqlite3.Error as e:
            print(f'Erro ao modificar nome_produto: {e}')
            return False

# Funções de crud para vendas
def registrar_venda(itens):
    """
    Registra uma nova venda na tabela vendas e seus respectivos
    itens na tabela itens_da_venda, itens deve ser uma lista
    """
    valor_total = 0
    itens_para_registrar = []
    data_hora_obj = datetime.now()
    data_hora_str = data_hora_obj.strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            for (id_produto, quantidade) in itens:
                cursor.execute("""
                    SELECT preco FROM produtos WHERE id_produto = (?)
                """, (id_produto,))
                resultado_query = cursor.fetchone()
                preco_unitario = resultado_query[0]
                subtotal = preco_unitario * quantidade
                valor_total += subtotal
                itens_para_registrar.append((id_produto, quantidade, preco_unitario))

            cursor.execute("""
                INSERT INTO vendas (data_hora, valor_total) VALUES (?, ?)
            """, (data_hora_str, valor_total))
            id_venda = cursor.lastrowid
            #print(f'ID VENDA: {id_venda}')

            for item in itens_para_registrar:
                id_produto, quantidade, preco_unitario = item
                cursor.execute("""
                    INSERT INTO itens_da_venda (id_venda, id_produto, quantidade, preco_unitario) 
                    VALUES (?, ?, ?, ?)
                """, (id_venda, id_produto, quantidade, preco_unitario))
            connection.commit()
            print(f'ID VENDA: {id_venda}')
            return id_venda
        except sqlite3.Error as e:
            print(f'Erro ao registrar uma venda: {e}')
            return False

def listar_vendas_por_data(data):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT * FROM vendas WHERE DATE(data_hora) = (?)
            """, (data,))
            vendas_encontradas = cursor.fetchall()
            return vendas_encontradas
        except sqlite3.Error as e:
            print(f'Erro ao listar vendas por data: {e}')
            return []

def listar_vendas():
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT * FROM vendas
            """)
            vendas_listadas = cursor.fetchall()
            return vendas_listadas
        except sqlite3.Error as e:
            print(f'Erro ao listar todas as vendas: {e}')
            return []

def listar_itens_por_venda(id_venda):
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT p.nome_produto, iv.quantidade, iv.preco_unitario FROM itens_da_venda as iv
                JOIN produtos as p
                ON iv.id_produto = p.id_produto
                WHERE iv.id_venda = (?)
            """, (id_venda,))
            produtos_listados_por_idvenda = cursor.fetchall()
            return produtos_listados_por_idvenda
        except sqlite3.Error as e:
            print(f'Erro ao listar produtos pelo id venda: {e}')
            return []


if __name__ == '__main__':
    # --- PASSO 0: GARANTIR UM BANCO DE DADOS LIMPO PARA O TESTE ---
    # Isso garante que cada vez que rodamos o teste, começamos do zero.
    import os
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Banco de dados antigo '{DB_FILE}' removido. Começando do zero.")

    # --- PASSO 1: CRIAÇÃO DA ESTRUTURA ---
    print("\n--- Testando: criar_tabelas ---")
    if not criar_tabelas():
        # Se as tabelas não puderem ser criadas, o programa para.
        exit()

    # --- PASSO 2: TESTES DE CATEGORIAS ---
    print("\n--- Testando: adicionar_categoria e listar_categorias ---")
    adicionar_categoria('Brincos')
    adicionar_categoria('Colares')
    adicionar_categoria('Tiaras')
    adicionar_categoria('Brincos') # Teste de falha (duplicata)
    
    print("Categorias atuais no banco:")
    print(listar_categorias())

    # --- PASSO 3: TESTES DE PRODUTOS ---
    print("\n--- Testando: adicionar_produto, listar_produtos e filtros ---")
    # Adicionando produtos para as categorias 1, 2 e 3
    adicionar_produto('Brinco_de_29.90', 29.90, 50, 1)
    adicionar_produto('Colar_de_29.90', 29.90, 30, 2)
    adicionar_produto('Tiara_de_10.00', 10.00, 10, 3)
    
    print("\nListando todos os produtos (com JOIN):")
    print(listar_produtos())

    print("\nListando apenas produtos da categoria 2 (Colares):")
    print(listar_produtos_por_categoria(2))

    # --- PASSO 4: TESTE DE UPDATE ---
    print("\n--- Testando: atualizar_estoque_produto ---")
    print("Atualizando estoque do produto ID 1 para 45...")
    atualizar_estoque_produto(1, 45)

    # --- PASSO 5: O GRANDE TESTE DE VENDA ---
    print("\n--- Testando: registrar_venda e listar_itens_por_venda ---")
    # Carrinho: 2x Brincos de 29,90 (ID 1), 1x Tiara de 10.00 (ID 3)
    carrinho = [(1, 2), (3, 1)] 
    
    novo_id_venda = registrar_venda(carrinho)
    if novo_id_venda:
        print(f"-> Venda {novo_id_venda} registrada com sucesso!")
        print(f"-> Verificando itens da venda {novo_id_venda}:")
        itens = listar_itens_por_venda(novo_id_venda)
        print(itens)
    else:
        print("-> Falha ao registrar venda.")

    print("\n--- TODOS OS TESTES CONCLUÍDOS ---")