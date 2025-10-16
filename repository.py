from models import Category
import database as db 

def get_all_categories():
    """"
    Busca todas as categorias no banco de dados e as retorna 
    como uma lista de objetos Category.
    """
    raw_categories = db.list_categories()
    category_objects = []

    for raw_category in raw_categories:
        new_category = Category(name=raw_category['nome_categoria'])
        category_objects.append(new_category)
    return category_objects


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