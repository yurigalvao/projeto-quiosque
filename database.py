import sqlite3

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
def registrar_venda(valor_total, itens):
    """
    Registra uma nova venda na tabela vendas e ses respectivos
    itens na tabela itens_da_venda, itens deve ser uma lista
    """
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            return True
        except sqlite3.Error as e:
            return False


if __name__ == '__main__':
    criar_tabelas()

    print('Adicionando categorias para testar função')

    adicionar_categoria('Brincos')
    adicionar_categoria('Colares')
    adicionar_categoria('Tiaras')

    # adicionando uma categoria existente para gerar um erro
    adicionar_categoria('Brincos')

    print()

    print('Testanto função listar_categorias (VERIFICAÇÃO)')

    # Etapa de verificação
    #Chamamos a função que busca os dados
    lista_de_categorias = listar_categorias()

    #verificamos se a lista não esta vazia 
    if lista_de_categorias:
        print('Ctegorias atualmente no banco de dados:')
        #Fazemos o loop para exibir os dados de forma limpa 
        for categoria in lista_de_categorias:
            print(f'ID: {categoria[0]}, Nome: {categoria[1]}')
    else:
        print('Nenhuma categoria encontrada')
    #-- FIM DA VERIFICAÇÃo

    print()

    print('TESTANDO adcionar novo produto')
    
    # Teste de sucesso
    adicionar_produto('Brinco_de_29_90', 29.9, 30, 1)
    adicionar_produto('Colar_de_35_90', 35.9, 20, 2)
    adicionar_produto('Tiara_de_19_90', 19.9, 10, 3)

    # Teste de falha
    adicionar_produto('Brinco_de_29_90', 29.9, 30, 1)

    print()

    print('TESTANDO função de listar produtos')
    lista_de_produtos = listar_produtos()

    if lista_de_produtos:
        print('Produtos encontrados no banco')
        for produto in lista_de_produtos:
            id_produto, nome_produto, preco_produto, estoque, categoria_nome = produto
            print(f'ID:{id_produto} | Produto:{nome_produto} | Preço: R${preco_produto:.2f} | Estoque:{estoque} | Categoria:{categoria_nome}')
    else:
        print('Nenhum Produto encontrado')

    print()

    print('Testando a função de listar produtos por categoria')
    produtos_filtrados = listar_produtos_por_categoria(1)
    if produtos_filtrados:
        for produto in produtos_filtrados:
            id_produto, nome_produto, preco_produto, estoque = produto
            print(f' -{nome_produto} (ID: {id_produto} | Preço: R${preco_produto:.2f} | Estoque: {estoque})')
    else:
        print('Nenhum produto encontrado para esta categoria')

    print()

    print('Testando função de atualizar estoque do produto')

    print('Estoque antes da atualização')
    produtos_antes = listar_produtos_por_categoria(1)
    if produtos_antes:
        print(f' - Produto: {produtos_antes[0][1]} | Estoque atual: {produtos_antes[0][3]}')

    #Executando a atualização no produto de ID 1 para 45 unidades
    id_para_atualizar = 1
    novo_estoque = 45
    if atualizar_estoque_produto(novo_estoque, id_para_atualizar):
        print(f'Tentativa de atualizar estoque do produto do ID {id_para_atualizar} para {novo_estoque}')
        print('Função rtornou True')
    else:
        print(f' Falha ao atualizar o estoque do produto ID {id_para_atualizar}')

    print('Estoque Depois de atualizar')
    produtos_depois = listar_produtos_por_categoria(1)
    if produtos_depois:
        print(f'  - Produto: {produtos_depois[0][1]} | Novo Estoque: {produtos_depois[0][3]}')

    print('Testes finalizados')