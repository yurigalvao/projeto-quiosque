from models import Category, Product, Sale, SaleItem
import database as db 
from database import ADMIN_PASSWORD
import os
from datetime import datetime

def add_category(category_object):
    """
    Recebe um objeto Category, extrai seu nome e o passa para a camada de banco de dados para ser salvo.

    Args:
        category_object (Category): O objeto da categoria a ser adicionada.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    category_name = category_object.name
    success = db.add_category(category_name)
    return success

def get_all_categories():
    """
    Busca todos os dados brutos de categorias no banco e os transforma em uma lista de objetos Category.

    Returns:
        list[Category]: Uma lista de objetos Category.
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
    """
    Busca uma única categoria pelo ID e a transforma em um objeto Category.

    Args:
        category_id (int): O ID da categoria a ser buscada.

    Returns:
        Category or None: O objeto Category correspondente se encontrado, senão None.
    """
    raw_category = db.find_category_by_id(category_id)

    if raw_category is None:
        return None
    
    category_object = Category(
        id=raw_category['id_categoria'],
        name=raw_category['nome_categoria']
    )
    return category_object

def update_category_name(category_id, new_name, provided_password):
    """
    Repassa a solicitação para atualizar o nome de uma categoria para a camada de banco de dados.

    Args:
        category_id (int): O ID da categoria a ser atualizada.
        new_name (str): O novo nome para a categoria.
        provided_password (str): A senha de administrador para autorização.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.update_category_name(category_id, new_name, provided_password)

def delete_category(category_id, provided_password):
    """
    Repassa a solicitação para deletar uma categoria para a camada de banco de dados.

    Args:
        category_id (int): O ID da categoria a ser deletada.
        provided_password (str): A senha de administrador para autorização.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.delete_category(category_id, provided_password)

def get_all_products():
    """
    Busca todos os dados brutos de produtos no banco e os transforma em uma lista de objetos Product.

    Returns:
        list[Product]: Uma lista de objetos Product, cada um contendo um objeto Category aninhado.
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
    """
    Busca os produtos de uma categoria específica e os retorna como uma lista de objetos Product.

    Args:
        category_id (int): O ID da categoria pela qual filtrar os produtos.

    Returns:
        list[Product]: Uma lista de objetos Product pertencentes à categoria.
    """
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
    """
    Recebe um objeto Product, o 'desmonta' em um dicionário de dados brutos e o passa
    para a camada de banco de dados para ser salvo.

    Args:
        product_object (Product): O objeto Product a ser adicionado.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    product_data_dict = {
        'nome_produto' : product_object.name,
        'preco' : product_object.price,
        'quantidade_estoque' : product_object.stock_quantity,
        'id_categoria' : product_object.category.id
    }
    
    success = db.add_product(product_data_dict)
    return success

def get_product_by_id(product_id):
    """
    Busca um produto específico pelo seu ID e o retorna como um objeto Product completo.

    Args:
        product_id (int): O ID do produto a ser buscado.

    Returns:
        Product or None: O objeto Product correspondente se encontrado, senão None.
    """
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
    """
    Recebe uma lista de objetos Product, os traduz para uma lista de dicionários
    e os salva no banco de dados em uma única operação otimizada.

    Args:
        product_object_list (list[Product]): Uma lista de objetos Product a serem adicionados.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
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
    """
    Repassa a solicitação para atualizar o estoque de um produto.

    Args:
        product_id (int): O ID do produto a ser atualizado.
        new_quantity (int): A nova quantidade em estoque.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.update_product_stock(product_id, new_quantity)

def update_product(product_id, provided_password, new_name=None, new_price=None):
    """
    Repassa a solicitação para a 'super-função' de atualização de produto.

    Args:
        product_id (int): O ID do produto.
        provided_password (str): A senha de administrador.
        new_name (str, optional): O novo nome. Defaults to None.
        new_price (float, optional): O novo preço. Defaults to None.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.update_product(product_id, provided_password, new_name, new_price)

def delete_product(product_id, provided_password):
    """
    Repassa a solicitação para deletar um produto.

    Args:
        product_id (int): O ID do produto.
        provided_password (str): A senha de administrador.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.delete_product(product_id, provided_password)

def register_sale(sale_object):
    """
    Recebe um objeto Sale, o 'desmonta' no formato esperado pela camada de banco de dados
    e repassa a solicitação para registrar a venda.

    Args:
        sale_object (Sale): O objeto Sale completo a ser registrado.

    Returns:
        int or bool: O ID da nova venda em caso de sucesso, senão False.
    """
    items_for_db = []
    try:
        for item_obj in sale_object.items:
            id_product = item_obj.product.id
            quantity_product = item_obj.quantity
            tuple_items = (id_product, quantity_product)
            items_for_db.append(tuple_items)
        new_sale_id = db.register_sale(items_for_db)
        return new_sale_id
    except Exception as e:
        print(f'Erro ao resgistrar vendas: {e}')
        return False

def get_all_sales():
    """
    Busca um resumo de todas as vendas e retorna uma lista de objetos Sale (sem os itens).

    Returns:
        list[Sale]: Uma lista de objetos Sale simplificados.
    """
    raw_sales = db.list_sales()
    sales = []

    for raw_sale in raw_sales:
        sale_obj = Sale(
            id = raw_sale['id_venda'],
            date_hour = raw_sale['data_hora'],
            total_value = raw_sale['valor_total']
        )
        sales.append(sale_obj)
    return sales

def get_sales_by_date(date):
    """

    Busca um resumo das vendas de uma data específica e retorna uma lista de objetos Sale.

    Args:
        date (str): A data para a busca, no formato 'YYYY-MM-DD'.

    Returns:
        list[Sale]: Uma lista de objetos Sale simplificados da data especificada.
    """
    raw_sales_date = db.list_sales_by_date(date)
    sales_date = []

    for raw_sale in raw_sales_date:
        sale_obj = Sale(
            id = raw_sale['id_venda'],
            date_hour = raw_sale['data_hora'],
            total_value = raw_sale['valor_total']
        )
        sales_date.append(sale_obj)
    return sales_date

def get_sales_by_id(sale_id):
    """

    Busca uma venda completa pelo ID, incluindo todos os seus itens, e a retorna
    como um único e complexo objeto Sale.

    Args:
        sale_id (int): O ID da venda a ser buscada.

    Returns:
        Sale or None: O objeto Sale completo se encontrado, senão None.
    """
    raw_sale = db.find_sale_by_id(sale_id)
    if raw_sale is None:
        return None
    
    sale_obj = Sale(
        id = raw_sale['id_venda'],
        date_hour = raw_sale['data_hora'],
        total_value = raw_sale['valor_total']
    )

    raw_items = db.list_items_by_sale(sale_id)

    for raw_item in raw_items:
        product_obj = get_product_by_id(raw_item['id_produto'])
        sale_item_obj = SaleItem(
            product = product_obj,
            quantity = raw_item['quantidade']
        )
        sale_obj.items.append(sale_item_obj)
    return sale_obj

def delete_sale(sale_id, provided_password):
    """
    Repassa a solicitação para deletar uma venda (e estornar o estoque).

    Args:
        sale_id (int): O ID da venda a ser deletada.
        provided_password (str): A senha de administrador.

    Returns:
        bool: True se a operação for bem-sucedida, False caso contrário.
    """
    return db.delete_sale(sale_id, provided_password)
    

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

    print("\n" + "="*30) # Separador

    print("\n--- Testando o Ciclo de Vida Completo de Vendas (Register, Get All, Delete) ---")

    # === ETAPA 1: SETUP - Montar um objeto de Venda completo ===
    print("\n--- Etapa 1: Preparando o objeto de Venda ---")
    
    # Buscamos os objetos Product que queremos vender para simular a interface
    produto_1 = get_product_by_id(1)
    produto_3 = get_product_by_id(3)
    
    id_venda_criada = None # Variavel para guardar o ID da venda que vamos criar

    if produto_1 and produto_3:
        # Criamos uma nova instância de Venda
        nova_venda_obj = Sale()
        
        # Adicionamos os itens à venda, como a interface faria
        nova_venda_obj.add_item(produto_1, 2) # 2 unidades do Produto 1
        nova_venda_obj.add_item(produto_3, 1) # 1 unidade do Produto 3
        
        print("Objeto de Venda criado e pronto para ser registrado.")

        # === ETAPA 2: TESTE - Chamar a função register_sale do repositório ===
        print("\n--- Etapa 2: Testando register_sale ---")
        id_venda_criada = register_sale(nova_venda_obj)
        
        if isinstance(id_venda_criada, int):
            print(f"--> SUCESSO! Venda registrada com o ID: {id_venda_criada}")
        else:
            print("--> FALHA! O registro da venda no repositório falhou.")

    # === ETAPA 3: TESTE - Chamar a get_all_sales para verificar ===
    if id_venda_criada:
        print("\n--- Etapa 3: Testando get_all_sales (após registro) ---")
        vendas_no_banco = get_all_sales()
        if vendas_no_banco and len(vendas_no_banco) == 1:
            print(f"--> SUCESSO! A função encontrou {len(vendas_no_banco)} venda.")
            print(f"    Inspecionando a venda: ID={vendas_no_banco[0].id}, Total=R${vendas_no_banco[0].total_value:.2f}")
        else:
            print("--> FALHA! A lista de vendas está incorreta.")

    # === ETAPA 4: TESTE - Chamar a delete_sale para limpar ===
    if id_venda_criada:
        print("\n--- Etapa 4: Testando delete_sale ---")
        print(f"Estoque ANTES do delete da venda:")
        print(f"  - {get_product_by_id(1).name}: {get_product_by_id(1).stock_quantity}")
        print(f"  - {get_product_by_id(3).name}: {get_product_by_id(3).stock_quantity}")

        sucesso_delete = delete_sale(id_venda_criada, ADMIN_PASSWORD)
        print(f"--> Operação de deleção bem-sucedida? {sucesso_delete}")

        # === ETAPA 5: VERIFICAÇÃO FINAL ===
        print("\n--- Etapa 5: Verificação Final ---")
        vendas_finais = get_all_sales()
        if not vendas_finais:
            print("--> SUCESSO! A lista de vendas está vazia, como esperado.")
        else:
            print(f"--> FALHA! Ainda existem {len(vendas_finais)} vendas no sistema.")

        print("Estoque DEPOIS do delete da venda (verificando estorno):")
        produto_1_final = get_product_by_id(1)
        produto_3_final = get_product_by_id(3)
        print(f"  - {produto_1_final.name}: {produto_1_final.stock_quantity}")
        print(f"  - {produto_3_final.name}: {produto_3_final.stock_quantity}")

    print("\n" + "="*30) # Separador

    print("\nTestando a função get_sales_by_date...")
    
    # Primeiro, vamos registrar uma venda para ter o que buscar
    print("\nCriando uma nova venda para o teste de data...")
    produto_teste = get_product_by_id(1)
    if produto_teste:
        venda_teste_data = Sale()
        venda_teste_data.add_item(produto_teste, 5)
        id_nova_venda = register_sale(venda_teste_data)
        if id_nova_venda:
            print(f"--> Venda de teste (ID: {id_nova_venda}) criada com sucesso.")

            # Agora, buscamos pela data de hoje
            data_de_hoje = datetime.now().strftime('%Y-%m-%d')
            print(f"\nBuscando vendas para a data: {data_de_hoje}")
            vendas_encontradas = get_sales_by_date(data_de_hoje)

            if vendas_encontradas:
                print(f"--> Sucesso! {len(vendas_encontradas)} venda(s) encontrada(s) para hoje.")
                for venda in vendas_encontradas:
                    print(f"    - Venda ID: {venda.id}, Total: R${venda.total_value:.2f}")
            else:
                print("--> FALHA! Nenhuma venda encontrada para a data de hoje.")
    else:
        print("--> FALHA no setup do teste: Produto de teste não encontrado.")

    print("\n" + "="*30) # Separador

    print("\nTestando a função get_sale_by_id (Montagem Mestra)...")

    # --- Setup do Teste: Criando uma venda completa para buscar ---
    print("\nCriando uma venda de teste completa...")
    
    produto_1 = get_product_by_id(1)
    produto_3 = get_product_by_id(3)
    id_venda_alvo = None

    if produto_1 and produto_3:
        venda_para_teste = Sale()
        venda_para_teste.add_item(produto_1, 3) # 3 Brincos
        venda_para_teste.add_item(produto_3, 2) # 2 Tiaras
        
        id_venda_alvo = register_sale(venda_para_teste)
        if id_venda_alvo:
            print(f"--> Venda de teste (ID: {id_venda_alvo}) criada com sucesso.")
    
    # --- Execução e Verificação do Teste ---
    if id_venda_alvo:
        print(f"\nBuscando o objeto completo da Venda ID {id_venda_alvo}...")
        
        # Chamamos a nossa Montagem Mestra
        sale_obj_completo = get_sales_by_id(id_venda_alvo)

        # Verificamos se o objeto principal foi montado
        if sale_obj_completo and isinstance(sale_obj_completo, Sale):
            print("--> SUCESSO! Objeto Sale completo foi retornado.")
            print(f"    - ID da Venda: {sale_obj_completo.id}")
            print(f"    - Valor Total: R${sale_obj_completo.total_value:.2f}")

            # Verificamos se os itens foram montados
            if sale_obj_completo.items and len(sale_obj_completo.items) == 2:
                print("--> SUCESSO! A lista de itens da venda foi montada corretamente.")
                
                # Inspecionamos o primeiro item para a prova final
                primeiro_item = sale_obj_completo.items[0]
                print("\n    Inspecionando o primeiro item da venda:")
                print(f"    - Tipo do item: {type(primeiro_item)}")
                print(f"    - Quantidade: {primeiro_item.quantity}")
                print(f"    - Tipo do produto dentro do item: {type(primeiro_item.product)}")
                print(f"    - Nome do produto: {primeiro_item.product.name}")

            else:
                print("--> FALHA! A lista de itens dentro da venda está incorreta.")
        else:
            print("--> FALHA! A função não retornou um objeto Sale válido.")
    else:
        print("--> FALHA no setup do teste.")