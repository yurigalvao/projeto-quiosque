import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# Carrega variaveis do arquivo .env para o ambiente
load_dotenv()

# Carregaa senhha do admin em uma constante no python
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


# Definimos o nome do arquivo do banco de dados como uma constante
DB_FILE = 'quiosque.db'


def create_tables():
    """
    FUnção para criar as tabelas iniciais do banco de dados,
    caso elas ainda não existam 
    """
    print('Verificando e criando tabelas, se necessario...')
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


def add_category(category_name):
    """Adiciona uma nova categoria ao banco de dados"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO categorias (nome_categoria) VALUES (?)
            """, (category_name,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao inserir dados na tebela categorias: {e}')
        return False


def list_categories():
    """Retorna uma lista de todas as categorias cadastradas"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_categoria, nome_categoria FROM categorias
            """)
            categorias_listadas = cursor.fetchall()
        return categorias_listadas
    except sqlite3.Error as e:
        print(f'Erro ao listar categorias: {e}')
        return []

def delete_category(category_id, provided_password):
    if provided_password != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
        # Liga a verificação de chaves estrangeiras para ESTA conexao
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM categorias
                WHERE id_categoria = (?)
            """, (category_id,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao deletar cateoria: {e}')
        return False
        
def update_category_name(category_id, new_name, provided_password):
    """Atualia o nome de uma categoria especifica"""
    if provided_password != ADMIN_PASSWORD:
        return False
    
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE categorias
                SET nome_categoria = (?)
                WHERE id_categoria = (?)
            """,(new_name, category_id,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao modificar nome da categoria: {e}')
        return False
    
def find_category_by_id(category_id):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            sql_query = f"""
                SELECT * FROM categorias WHERE id_categoria = (?)
            """
            cursor.execute(sql_query, (category_id,))
            result_query = cursor.fetchone()
        return result_query
    except sqlite3.Error as e:
        print(f'Erro ao buscar categoria por id: {e}')
        return None

# FUnções crud para 'produtos'
def add_product(product_data):
    """Adiciona um novo produto ao banco de dados"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            sql_query = ("""
                INSERT INTO produtos (nome_produto, preco, quantidade_estoque, id_categoria) VALUES (:nome_produto, :preco, :quantidade_estoque, :id_categoria)
            """)
            cursor.execute(sql_query, product_data)
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao inserir produto na tabela produtos: {e}')
        return False
    
def add_multiple_products(product_list):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            sql_query = ("""
                INSERT INTO produtos (nome_produto, preco, quantidade_estoque, id_categoria) VALUES (:nome_produto, :preco, :quantidade_estoque, :id_categoria)
            """)
            cursor.executemany(sql_query, product_list)
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao adicionar varios produtos: {e}')
        return False

def list_products():
    """Retorna uma lista de todos os produtos com o nome da categoria (usando JOIN)"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.id_produto, p.nome_produto, p.preco, p.quantidade_estoque, c.nome_categoria, c.id_categoria FROM produtos AS p
                JOIN categorias AS c
                ON p.id_categoria = c.id_categoria
            """)
            products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f'Erro ao listar produtos: {e}')
        return []
        
def list_products_by_category(category_id):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_produto, nome_produto, preco, quantidade_estoque FROM produtos
                WHERE id_categoria = (?)
            """, (category_id,))
            products = cursor.fetchall()
        return products
    except sqlite3.Error as e:
        print(f'Erro ao listar produtos: {e}')
        return []

def update_product_stock(product_id, new_quantity):
    """Atualiza o estoque de um produto especifico"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE produtos
                SET quantidade_estoque = (?)
                WHERE id_produto = (?)
            """,(new_quantity, product_id,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao modificar quantidade_estoque: {e}')
        return False

def update_product(product_id, provided_password, new_name=None, new_price=None):
    if provided_password != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            set_clausules = []
            values = []
            if new_name is not None:
                set_clausules.append('nome_produto = ?')
                values.append(new_name)
            if new_price is not None:
                set_clausules.append('preco = ?')
                values.append(new_price)

            if not set_clausules:
                return True
            set_statement = ', '.join(set_clausules)
            sql_query = f'UPDATE produtos SET {set_statement} WHERE id_produto = (?)'
            values.append(product_id)
            cursor.execute(sql_query, values)
            connection.commit()
        return True
    except sqlite3.Error as e:
        return False


def delete_product(product_id, provided_password):
    if provided_password != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            # Boa prática: manter o PRAGMA em todas as funções de escrita 
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM produtos
                WHERE id_produto = (?)
            """, (product_id,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao deletar produto: {e}')
        return False

def find_product_by_id(product_id):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            sql_query = ("""
                SELECT p.*, c.nome_categoria FROM produtos AS p JOIN
                categorias AS c ON p.id_categoria = c.id_categoria
                WHERE p.id_produto = (?)
            """)
            cursor.execute(sql_query, (product_id,))
            result = cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f'Nao foi possivel procurar produtos pelo id: {e}')
        return None

# Funções de crud para vendas
def register_sale(items):
    """
    Registra uma nova venda na tabela vendas e seus respectivos
    itens na tabela itens_da_venda, itens deve ser uma lista
    """
    total_price = 0
    items_to_register = []
    datetime_obj = datetime.now()
    datetime_str = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            for (product_id, quantity) in items:
                cursor.execute("""
                    SELECT preco, quantidade_estoque FROM produtos WHERE id_produto = (?)
                """, (product_id,))
                query_result = cursor.fetchone()
                if not query_result:
                    print(f'Erro: Produto com ID {product_id} não encontrado')
                    return False
                
                stock_quantity = query_result[1]
                if quantity > stock_quantity:
                    print(f'Erro: Estoque insuficiente para o produto ID {product_id}')
                    return False
                
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque - (?)
                    WHERE id_produto = (?)
                """, (quantity, product_id))
                unit_price = query_result[0]
                subtotal = unit_price * quantity
                total_price += subtotal
                items_to_register.append((product_id, quantity, unit_price))

            cursor.execute("""
                INSERT INTO vendas (data_hora, valor_total) VALUES (?, ?)
            """, (datetime_str, total_price))
            sale_id = cursor.lastrowid
            #print(f'ID VENDA: {id_venda}')

            for item in items_to_register:
                product_id, quantity, unit_price = item
                cursor.execute("""
                    INSERT INTO itens_da_venda (id_venda, id_produto, quantidade, preco_unitario) 
                    VALUES (?, ?, ?, ?)
                """, (sale_id, product_id, quantity, unit_price))
            connection.commit()
            print(f'ID VENDA: {sale_id}')
        return sale_id
    except sqlite3.Error as e:
        print(f'Erro ao registrar uma venda: {e}')
        return False

def list_sales_by_date(date_str):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM vendas WHERE DATE(data_hora) = (?)
            """, (date_str,))
            found_sales = cursor.fetchall()
        return found_sales
    except sqlite3.Error as e:
        print(f'Erro ao listar vendas por data: {e}')
        return []

def list_sales():
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM vendas
            """)
            sales = cursor.fetchall()
        return sales
    except sqlite3.Error as e:
        print(f'Erro ao listar todas as vendas: {e}')
        return []

def list_items_by_sale(sale_id):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.nome_produto, iv.quantidade, iv.preco_unitario FROM itens_da_venda as iv
                JOIN produtos as p
                ON iv.id_produto = p.id_produto
                WHERE iv.id_venda = (?)
            """, (sale_id,))
            items = cursor.fetchall()
        return items
    except sqlite3.Error as e:
        print(f'Erro ao listar produtos pelo id venda: {e}')
        return []

def delete_sale(sale_id, provided_password):
    if provided_password != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_produto, quantidade FROM itens_da_venda
                WHERE id_venda = (?)
            """,(sale_id,))
            sold_products = cursor.fetchall()
            
            for product in sold_products:
                product_id, quantity = product
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque + (?)
                    WHERE id_produto = (?)
                """, (quantity, product_id,))

            cursor.execute(""" 
                DELETE from itens_da_venda
                WHERE id_venda = (?)
            """,(sale_id,))

            cursor.execute("""
                DELETE from vendas
                WHERE id_venda = (?)
            """,(sale_id,))

            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False


if __name__ == '__main__':
    # --- STEP 0: ENSURE A CLEAN DATABASE FOR THE TEST ---
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Old database '{DB_FILE}' removed. Starting from scratch.")

    # --- STEP 1: STRUCTURE CREATION ---
    print("\n--- Testing: create_tables ---")
    if not create_tables():
        exit()

    # --- STEP 2: CATEGORY TESTS ---
    print("\n--- Testing: add_category and list_categories ---")
    add_category('Brincos')
    add_category('Colares')
    add_category('Tiaras')
    add_category('Brincos') # Expected failure (duplicate)
    
    print("Current categories in the database (accessing by name):")
    category_list = list_categories()
    if category_list:
        for category in category_list:
            print(f"  - ID: {category['id_categoria']}, Name: {category['nome_categoria']}")

    # --- STEP 3: PRODUCT TESTS ---
    print("\n--- Testing: add_product, list_products, and filters ---")
    product1 = {'nome_produto': 'Brinco de Prata', 'preco': 35.50, 'quantidade_estoque': 50, 'id_categoria': 1}
    product2 = {'nome_produto': 'Colar de Perolas', 'preco': 80.00, 'quantidade_estoque': 30, 'id_categoria': 2}
    product3 = {'nome_produto': 'Tiara de Festa', 'preco': 22.00, 'quantidade_estoque': 15, 'id_categoria': 3}
    add_product(product1)
    add_product(product2)
    add_product(product3)
    
    print("\nListing all products (with JOIN):")
    product_list = list_products()
    if product_list:
        for product in product_list:
            print(f"  - ID: {product['id_produto']}, Name: {product['nome_produto']}, Price: R${product['preco']:.2f}, Stock: {product['quantidade_estoque']}, Category: {product['nome_categoria']}")

    # --- STEP 4: STOCK UPDATE TEST ---
    print("\n--- Testing: update_product_stock ---")
    print("Updating stock for product ID 1 to 48...")
    update_product_stock(48, 1)

    # --- STEP 5: SALE REGISTRATION TEST ---
    print("\n--- Testing: register_sale and list_items_by_sale ---")
    cart = [(1, 2), (3, 1)] # Stock for product 1 (Brinco) -> 46. product 3 (Tiara) -> 14.
    
    new_sale_id = register_sale(cart)
    if new_sale_id:
        print(f"-> Sale {new_sale_id} registered successfully!")
        print(f"-> Verifying items for sale {new_sale_id}:")
        items = list_items_by_sale(new_sale_id)
        if items:
            for item in items:
                print(f"  - Product: {item['nome_produto']}, Qty: {item['quantidade']}, Unit Price: R${item['preco_unitario']:.2f}")
    else:
        print("-> Failed to register sale.")

    # --- STEP 6: SECURE CATEGORY DELETE TEST ---
    print("\n--- Testing: delete_category (secure) ---")
    print("\nAttempting to delete Category ID 3 (Tiaras) with correct password (should fail due to FK)...")
    delete_category(3, ADMIN_PASSWORD)
    
    # --- STEP 7: SECURE PRODUCT DELETE TEST ---
    print("\n--- Testing: delete_product (secure) ---")
    print("\nAttempting to delete Product ID 2 (Colar) with correct password...")
    delete_product(2, ADMIN_PASSWORD)
    print("Verifying if the product was removed:")
    for product in list_products():
        print(f"  - {product['nome_produto']}")

    # --- STEP 8: COMPLEX SALE DELETE TRANSACTION TEST ---
    print("\n--- Testing: delete_sale with stock refund ---")
    print("Attempting to delete Sale ID 1 with correct password...")
    delete_sale(1, ADMIN_PASSWORD)
    print("Verifying stock after delete (should be refunded):")
    for product in list_products():
        print(f"  - {product['nome_produto']}: Stock = {product['quantidade_estoque']}")


    # --- STEP 9: 'SUPER-FUNCTION' UPDATE_PRODUCT TEST ---
    print("\n--- Testing: the super-function update_product ---")
    update_product(1, ADMIN_PASSWORD, new_name="Brinco de Prata Esterlina", new_price=39.99)
    
    print("\n--- Final Verification ---")
    print("Final state of products after all updates:")
    final_product_list = list_products()
    if final_product_list:
        for product in final_product_list:
            print(f"  - ID: {product['id_produto']}, Name: {product['nome_produto']}, Price: R${product['preco']:.2f}, Stock: {product['quantidade_estoque']}, Category: {product['nome_categoria']}")

    print("\n--- ALL TESTS COMPLETED ---")