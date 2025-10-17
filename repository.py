from models import Category, Product, Sale
import database as db 
from database import ADMIN_PASSWORD
import os

def add_category(category_object):
    category_name = category_object.name
    success = db.add_category(category_name)
    return success

def get_all_categories():
    """
    Busca todas as categorias no banco de dados e as retorna 
    como uma lista de objetos Category.
    """
    raw_categories = db.list_categories()
    category_objects = []

    for raw_category in raw_categories:
        new_category = Category(
            id=raw_category['id_categoria'],
            name=raw_category['nome_categoria']
            )
        category_objects.append(new_category)
    return category_objects

def get_category_by_id(category_id):
    raw_category = db.find_category_by_id(category_id)

    if raw_category is None:
        return None
    
    category_object = Category(
        id=raw_category['id_categoria'],
        name=raw_category['nome_categoria']
    )
    return category_object

def update_category_name(category_id, new_name, provided_password):
    return db.update_category_name(category_id, new_name, provided_password)

def delete_category(category_id, provided_password):
    return db.delete_category(category_id, provided_password)

def get_all_products():
    """
    Busca todos os produtos no banco de dados e os retorna
    como uma lista de objetos Product
    """
    raw_products = db.list_products()
    products_object = []

    for raw_product in raw_products:
        category_obj = Category(
            id=raw_product['id_categoria'],
            name=raw_product['nome_categoria']
            )
        product_object = Product(
            id=raw_product['id_produto'],
            name = raw_product['nome_produto'],
            price = raw_product['preco'],
            stock_quantity = raw_product['quantidade_estoque'],
            category = category_obj
        )
        products_object.append(product_object)
    return products_object

def get_products_by_category(category_id):
    category_obj = get_category_by_id(category_id)

    if not category_obj:
        return []

    raw_products = db.list_products_by_category(category_id)
    objects = []
    

    for raw_product in raw_products:
        product_obj = Product(
            id=raw_product['id_produto'],
            name= raw_product['nome_produto'],
            price = raw_product['preco'],
            stock_quantity = raw_product['quantidade_estoque'],
            category = category_obj
        )
        objects.append(product_obj)
    return objects

def add_product(product_object):
    product_data_dict = {
        'nome_produto' : product_object.name,
        'preco' : product_object.price,
        'quantidade_estoque' : product_object.stock_quantity,
        'id_categoria' : product_object.category.id
    }
    
    success = db.add_product(product_data_dict)
    return success

def get_product_by_id(product_id):
    raw_product = db.find_product_by_id(product_id)

    if raw_product is None:
        return None
    

    category_obj = Category(
        id=raw_product['id_categoria'],
        name=raw_product['nome_categoria']
        )
    product_object = Product(
        id=raw_product['id_produto'],
        name = raw_product['nome_produto'],
        price = raw_product['preco'],
        stock_quantity = raw_product['quantidade_estoque'],
        category = category_obj
    )
    return product_object

def add_multiples_products(product_object_list):
    
    try:
        product_data_list = []
        for product_object in product_object_list:
            product_data_dict = {
                'nome_produto' : product_object.name,
                'preco' : product_object.price,
                'quantidade_estoque' : product_object.stock_quantity,
                'id_categoria' : product_object.category.id
            }
            product_data_list.append(product_data_dict)

        success = db.add_multiple_products(product_data_list)
        #print('n\[DEPURACAO] Lista de dicionarios sendo enviada para o DB: ')
        #print(product_data_list)
        return success
    except Exception as e:
        print(f'Um erro ocorreu ao adicionar multiplos produtos: {e}')
        return False

    
def update_product_stock(product_id, new_quantity):
    return db.update_product_stock(product_id, new_quantity)

def update_product(product_id, provided_password, new_name=None, new_price=None):
    return db.update_product(product_id, provided_password, new_name, new_price)

def delete_product(product_id, provided_password):
    return db.delete_product(product_id, provided_password)
    

if __name__ == '__main__':
    # --- Bloco de Setup do Teste ---
    print("--- Preparando ambiente de teste do Repositório ---")
    # Garante que o banco de dados esteja zerado
    if os.path.exists(db.DB_FILE):
        os.remove(db.DB_FILE)
    
    # Recria as tabelas e os dados de teste iniciais
    db.create_tables()
    db.add_category('Brincos')
    db.add_category('Colares')
    db.add_category('Tiaras')
    db.add_product({'nome_produto': 'Brinco de Prata Esterlina', 'preco': 39.99, 'quantidade_estoque': 50, 'id_categoria': 1})
    db.add_product({'nome_produto': 'Tiara de Festa', 'preco': 22.00, 'quantidade_estoque': 15, 'id_categoria': 3})
    print("--- Ambiente de teste pronto. Iniciando testes do repositório... ---")
    
    # --- Teste get_all_categories ---
    print("\n--- Testando: get_all_categories ---")
    print("Buscando todas as categorias como OBJETOS...")
    lista_de_objetos_categoria = get_all_categories()
    if lista_de_objetos_categoria:
        print(f"--> Sucesso! Encontrados {len(lista_de_objetos_categoria)} objetos Category.")
        # Inspecionando o primeiro para confirmar
        print(f"    Tipo do primeiro objeto: {type(lista_de_objetos_categoria[0])}")

    print("\n" + "="*30)

    # --- Teste get_all_products ---
    print("\n--- Testando: get_all_products ---")
    print("Buscando todos os produtos como OBJETOS...")
    lista_de_objetos_produto = get_all_products()
    if lista_de_objetos_produto:
        primeiro_produto = lista_de_objetos_produto[0]
        print(f"--> Sucesso! Encontrados {len(lista_de_objetos_produto)} objetos Product.")
        print(f"    Inspecionando o primeiro: {primeiro_produto.name} (Categoria: {primeiro_produto.category.name})")

    print("\n" + "="*30)

    # --- Teste add_category ---
    print("\n--- Testando: add_category ---")
    nova_categoria_obj = Category(name='Pulseiras')
    print(f"Tentando adicionar a categoria: '{nova_categoria_obj.name}'")
    sucesso_add_cat = add_category(nova_categoria_obj)
    print(f"--> Operação bem-sucedida? {sucesso_add_cat}")
    print("Lista de categorias após a adição:")
    for categoria in get_all_categories():
        print(f"  - {categoria.name}")

    print("\n" + "="*30)

    # --- Teste add_product ---
    print("\n--- Testando: add_product ---")
    cat_colares = get_category_by_id(2)
    novo_produto_obj = Product(name='Colar de Diamante', price=999.99, stock_quantity=10, category=cat_colares)
    print(f"Tentando adicionar o produto: '{novo_produto_obj.name}'")
    sucesso_add_prod = add_product(novo_produto_obj)
    print(f"--> Operação bem-sucedida? {sucesso_add_prod}")

    print("\n" + "="*30)

    # --- Teste get_category_by_id ---
    print("\n--- Testando: get_category_by_id ---")
    print("Buscando categoria com ID existente (ID=2)...")
    categoria_encontrada = get_category_by_id(2)
    print(f"--> Encontrado: {categoria_encontrada.name if categoria_encontrada else 'None'}")
    print("Buscando categoria com ID inexistente (ID=99)...")
    categoria_nao_encontrada = get_category_by_id(99)
    print(f"--> Encontrado: {categoria_nao_encontrada} (Esperado: None)")
    
    print("\n" + "="*30)

    # --- Teste update_category_name ---
    print("\n--- Testando: update_category_name ---")
    print("Tentando atualizar a categoria ID 3 para 'Tiaras de Luxo'...")
    sucesso_update_cat = update_category_name(3, "Tiaras de Luxo", ADMIN_PASSWORD)
    print(f"--> Operação bem-sucedida? {sucesso_update_cat}")
    categoria_atualizada = get_category_by_id(3)
    print(f"Novo nome da categoria ID 3: {categoria_atualizada.name}")

    print("\n" + "="*30)

    # --- Teste get_products_by_category ---
    print("\n--- Testando: get_products_by_category ---")
    print("Buscando produtos da Categoria ID 1 (Brincos)...")
    produtos_encontrados = get_products_by_category(1)
    print(f"--> {len(produtos_encontrados)} produto(s) encontrado(s).")
    for produto in produtos_encontrados:
        print(f"    - {produto.name}")

    print("\n" + "="*30)

    # --- Teste get_product_by_id ---
    print("\n--- Testando: get_product_by_id ---")
    print("Buscando produto com ID existente (ID=1)...")
    produto_encontrado = get_product_by_id(1)
    print(f"--> Encontrado: {produto_encontrado.name}")

    print("\n" + "="*30)

    # --- Teste update_product_stock ---
    print("\n--- Testando: update_product_stock ---")
    print("Atualizando estoque do Produto ID 1 para 99 unidades...")
    update_product_stock(1, 99)
    produto_atualizado = get_product_by_id(1)
    print(f"--> Novo Estoque: {produto_atualizado.stock_quantity} (Esperado: 99)")

    print("\n" + "="*30)

    # --- Teste update_product ---
    print("\n--- Testando: update_product ---")
    print("Atualizando nome e preço do produto ID 1...")
    update_product(1, ADMIN_PASSWORD, new_name="Brinco de Ouro", new_price=150.0)
    produto_super_atualizado = get_product_by_id(1)
    print(f"--> Novo Nome: {produto_super_atualizado.name}, Novo Preço: {produto_super_atualizado.price}")

    print("\n" + "="*30)

    # --- Teste add_multiple_products ---
    print("\n--- Testando: add_multiple_products ---")
    novos_produtos_lote = [
        Product(name='Brinco de Pena', price=55.0, stock_quantity=100, category=get_category_by_id(1)),
        Product(name='Colar Branco', price= 110.0, stock_quantity=55, category=get_category_by_id(2))
    ]
    print(f"Tentando adicionar {len(novos_produtos_lote)} novos produtos em lote...")
    sucesso_lote = add_multiples_products(novos_produtos_lote)
    print(f"--> Operação bem-sucedida? {sucesso_lote}")

    print("\n--- Verificação Final ---")
    print("Estado final de todos os produtos no banco:")
    for produto in get_all_products():
        print(f"  - {produto.name} (Categoria: {produto.category.name})")