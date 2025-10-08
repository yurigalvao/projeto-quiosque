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

    except sqlite3.Error as e:
        print(f'Ocorreu um erro ao criar tabelas: {e}')


def adicionar_categoria(nome_categoria):
    """Adiciona uma nova categoria ao banco de dados"""
    with sqlite3.connect(DB_FILE) as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO categorias (nome_categoria) VALUES (?)
            """, (nome_categoria,))
            connection.commit()
        except sqlite3.Error as e:
            print(f'Erro ao inserir dados na tebela categorias: {e}')


def listar_categorias():
    """Retorna uma lista de todas as categorias cadastradas"""
    pass

# FUnções crud para 'produtos'
def adicionar_produto(nome, preco, estoque, id_categoria):
    """Adiciona um novo produto ao banco de dados"""
    pass

def listar_produtos():
    """Retorna uma lista de todos os produtos com o nome da categoria (usando JOIN)"""
    pass

def atualizar_estoque(id_produto, nova_quantidade):
    """Atualiza o estoque de um produto especifico"""
    pass

# Funções de crud para vendas
def registrar_venda(valor_total, itens):
    """
    Registra uma nova venda na tabela vendas e ses respectivos
    itens na tabela itens_da_venda, itens deve ser uma lista
    """
    pass

if __name__ == '__main__':
    criar_tabelas()

    print('Adicionando categorias para testar função')

    adicionar_categoria('Brincos')
    adicionar_categoria('Colares')
    adicionar_categoria('Tiaras')

    # adicionando uma categoria existente para gerar um erro
    adicionar_categoria('Brincos')

    print()

    print('Testes finalizados')