from models import Category, Product
import database as db 
from database import ADMIN_PASSWORD

def get_all_categories():
    """
    Busca todas as categorias no banco de dados e as retorna 
    como uma lista de objetos Category.
    """
    raw_categories = db.list_categories()
    category_objects = []

    for raw_category in raw_categories:
        new_category = Category(
            name=raw_category['nome_categoria']
            )
        category_objects.append(new_category)
    return category_objects

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

def add_category(category_object):
    category_name = category_object.name
    success = db.add_category(category_name)
    return success

def add_product(product_object):
    product_data_dict = {
        'nome_produto' : product_object.name,
        'preco' : product_object.price,
        'quantidade_estoque' : product_object.stock_quantity,
        'id_categoria' : product_object.category.id
    }
    
    success = db.add_product(product_data_dict)
    return success

def delete_product(product_id, provided_password):
    success = db.delete_product(product_id, provided_password)
    return success
    

if __name__ == '__main__':
    print('--- Testando a camada do Repositorio---')

    print('\nBuscando todas as categorias como OBJETOS...')
    lista_de_objetos_categoria = get_all_categories()
    
    # Verificamos se a lista não está vazia
    if lista_de_objetos_categoria:
        # Pegamos o PRIMEIRO objeto da lista para inspecionar
        primeira_categoria = lista_de_objetos_categoria[0]
        
        print(f"\nO que a função retornou? Uma lista de {len(lista_de_objetos_categoria)} itens.")
        
        print("\nInspecionando o primeiro item da lista:")
        print(f"  - O tipo do objeto é: {type(primeira_categoria)}")
        print(f"  - Acessando o atributo .name do objeto: {primeira_categoria.name}")
        
        print("\nImprimindo todos os objetos da lista:")
        # O __str__ da sua classe Category vai deixar a impressão bonita
        for categoria in lista_de_objetos_categoria:
            print(f"  - {categoria}")
    else:
        print("Nenhuma categoria foi encontrada.")

    print("\n" + "="*30) # Separador visual

    print("\nBuscando todos os produtos como OBJETOS...")
    lista_de_objetos_produto = get_all_products()

    if lista_de_objetos_produto:
        # Pegamos o PRIMEIRO produto da lista para uma inspeção detalhada
        primeiro_produto = lista_de_objetos_produto[0]
        
        print(f"\nO que a função retornou? Uma lista de {len(lista_de_objetos_produto)} itens.")
        
        print("\nInspecionando o primeiro item da lista:")
        print(f"  - O tipo do objeto principal é: {type(primeiro_produto)}")
        print(f"  - Acessando o atributo .name: {primeiro_produto.name}")
        print(f"  - Acessando o atributo .price: R${primeiro_produto.price:.2f}")

        # Aqui está a prova da montagem complexa!
        print(f"  - O tipo do objeto aninhado (categoria) é: {type(primeiro_produto.category)}")
        print(f"  - Acessando o atributo .name do objeto categoria: {primeiro_produto.category.name}")

        print("\nImprimindo todos os objetos da lista (usando o __str__ da sua classe):")
        for produto in lista_de_objetos_produto:
            print(f"  - {produto}")
    else:
        print("Nenhum produto foi encontrado.")

    print("\n" + "="*30) # Separador

    print("\nTestando a função de adicionar categoria...")
    
    # 1. Crie o objeto que queremos adicionar
    nova_categoria_obj = Category(name='Pulseiras')
    print(f"Tentando adicionar a categoria: '{nova_categoria_obj.name}'")
    
    # 2. Chame a função do repositório
    sucesso = add_category(nova_categoria_obj)
    print(f"--> Operação bem-sucedida? {sucesso}")
    
    # 3. Verifique o resultado final
    print("\nLista de categorias após a adição:")
    categorias_finais = get_all_categories()
    for categoria in categorias_finais:
        print(f"  - {categoria.name}")

    print("\n" + "="*30) # Separador

    print("\nTestando a função add_product (com objetos)...")

    # 1. Primeiro, criamos os OBJETOS que vamos usar como entrada.
    # Criamos um objeto para uma categoria que sabemos que existe no banco (Colares, ID=2)
    categoria_do_produto = Category(id=2, name='Colares')

    # Agora, criamos o novo objeto Produto, usando o objeto Categoria acima.
    novo_produto_obj = Product(
        name='Colar de Diamante',
        price=999.99,
        stock_quantity=10,
        category=categoria_do_produto
    )
    print(f"Tentando adicionar o produto: '{novo_produto_obj.name}'")

    # 2. Chamamos a função do repositório, passando o OBJETO completo
    sucesso = add_product(novo_produto_obj)
    print(f"--> Operação bem-sucedida? {sucesso}")

    # 3. Verificamos o resultado final, listando tudo de novo
    print("\nLista de produtos após a adição:")
    produtos_finais = get_all_products()
    for produto in produtos_finais:
        print(f"  - {produto.name} (Categoria: {produto.category.name})")

    print("\n" + "="*30) # Separador

    print("\nTestando a função delete_product do repositório...")

    # Nosso alvo será o 'Colar de Diamante', que foi o último a ser adicionado
    # Vamos precisar descobrir o ID dele primeiro
    produtos_antes_delete = get_all_products()
    id_para_deletar = None
    for p in produtos_antes_delete:
        if p.name == 'Colar de Diamante':
            id_para_deletar = p.id # Precisamos garantir que a classe Product tenha o 'id'

    if id_para_deletar:
        print(f"Tentando deletar o produto: 'Colar de Diamante' (ID: {id_para_deletar})")
        
        # Chamamos a função do repositório
        sucesso = delete_product(id_para_deletar, ADMIN_PASSWORD)
        print(f"--> Operação bem-sucedida? {sucesso}")

        # Verificamos o resultado final
        print("\nLista de produtos após a deleção:")
        produtos_finais = get_all_products()
        for produto in produtos_finais:
            print(f"  - {produto.name}")
    else:
        print("Produto 'Colar de Diamante' não encontrado para o teste.")