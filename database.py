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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_categoria, nome_categoria FROM categorias
            """)
            categorias_listadas = cursor.fetchall()
        return categorias_listadas
    except sqlite3.Error as e:
        print(f'Erro ao listar categorias: {e}')
        return []

def deletar_categoria(id_categoria, senha_fornecida):
    if senha_fornecida != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
        # Liga a verificação de chaves estrangeiras para ESTA conexao
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM categorias
                WHERE id_categoria = (?)
            """, (id_categoria,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao deletar cateoria: {e}')
        return False
        
def atualizar_nome_categoria(novo_nome, id_categoria, senha_fornecida):
    """Atualia o nome de uma categoria especifica"""
    if senha_fornecida != ADMIN_PASSWORD:
        return False
    
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE categorias
                SET nome_categoria = (?)
                WHERE id_categoria = (?)
            """,(novo_nome, id_categoria,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao modificar nome da categoria: {e}')
        return False


# FUnções crud para 'produtos'
def adicionar_produto(nome_produto, preco, quantidade_estoque, id_categoria):
    """Adiciona um novo produto ao banco de dados"""
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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

def atualizar_produto(id_produto, senha_fornecida, novo_nome=None, novo_preco=None):
    if senha_fornecida != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            partes_do_set = []
            valores = []
            if novo_nome is not None:
                partes_do_set.append('nome_produto = ?')
                valores.append(novo_nome)
            if novo_preco is not None:
                partes_do_set.append('preco = ?')
                valores.append(novo_preco)

            if not partes_do_set:
                return True
            clausula_set = ', '.join(partes_do_set)
            query_sql = f'UPDATE produtos SET {clausula_set} WHERE id_produto = (?)'
            valores.append(id_produto)
            cursor.execute(query_sql, valores)
            connection.commit()
        return True
    except sqlite3.Error as e:
        return False


def deletar_produto(id_produto, senha_fornecida):
    if senha_fornecida != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            # Boa prática: manter o PRAGMA em todas as funções de escrita 
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM produtos
                WHERE id_produto = (?)
            """, (id_produto,))
            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Erro ao deletar produto: {e}')
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            for (id_produto, quantidade) in itens:
                cursor.execute("""
                    SELECT preco, quantidade_estoque FROM produtos WHERE id_produto = (?)
                """, (id_produto,))
                resultado_query = cursor.fetchone()
                quantidade_lista = resultado_query[1]
                if quantidade > quantidade_lista:
                    return False
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque - (?)
                    WHERE id_produto = (?)
                """, (quantidade, id_produto))
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
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM vendas WHERE DATE(data_hora) = (?)
            """, (data,))
            vendas_encontradas = cursor.fetchall()
        return vendas_encontradas
    except sqlite3.Error as e:
        print(f'Erro ao listar vendas por data: {e}')
        return []

def listar_vendas():
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM vendas
            """)
            vendas_listadas = cursor.fetchall()
        return vendas_listadas
    except sqlite3.Error as e:
        print(f'Erro ao listar todas as vendas: {e}')
        return []

def listar_itens_por_venda(id_venda):
    try:
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
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

def deletar_venda(id_venda, senha_fornecida):
    if senha_fornecida != ADMIN_PASSWORD:
        return False
    try:
        with sqlite3.connect(DB_FILE) as connection:
            connection.execute('PRAGMA foreign_keys = ON;')

            cursor = connection.cursor()
            cursor.execute("""
                SELECT id_produto, quantidade FROM itens_da_venda
                WHERE id_venda = (?)
            """,(id_venda,))
            produtos_da_venda = cursor.fetchall()
            
            for produto in produtos_da_venda:
                id_do_produto, quantidade = produto
                cursor.execute("""
                    UPDATE produtos
                    SET quantidade_estoque = quantidade_estoque + (?)
                    WHERE id_produto = (?)
                """, (quantidade, id_do_produto,))

            cursor.execute(""" 
                DELETE from itens_da_venda
                WHERE id_venda = (?)
            """,(id_venda,))

            cursor.execute("""
                DELETE from vendas
                WHERE id_venda = (?)
            """,(id_venda,))

            connection.commit()
        return True
    except sqlite3.Error as e:
        print(f'Error: {e}')
        return False


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

    # --- PASSO 6: TESTES DE DELETE SEGURO ---
    print("\n--- Testando: deletar_categoria (seguro) ---")
    
    # Teste 1: Senha incorreta
    print("\nTentando deletar a categoria ID 3 (Tiaras) com a senha errada...")
    id_para_deletar = 3
    senha_errada = "senha-incorreta-123"
    resultado_falha = deletar_categoria(id_para_deletar, senha_errada)
    print(f"Resultado da operação (falha): {resultado_falha}")
    print("Verificando se as categorias ainda estão intactas:")
    print(listar_categorias())

    # Teste 2: Senha correta
    print("\nTentando deletar a categoria ID 3 (Tiaras) com a senha CORRETA...")
    resultado_sucesso = deletar_categoria(id_para_deletar, ADMIN_PASSWORD)
    print(f"Resultado da operação (sucesso): {resultado_sucesso}")
    print("Verificando se a categoria foi removida:")
    print(listar_categorias())

    # --- PASSO 7: TESTES DE DELETE SEGURO DE PRODUTO ---
    print("\n--- Testando: deletar_produto (seguro) ---")

    print(listar_produtos())
    
    # Teste 1: Senha incorreta
    print("\nTentando deletar o produto ID 2 (Colar) com a senha errada...")
    id_produto_para_deletar = 2
    resultado_falha_produto = deletar_produto(id_produto_para_deletar, "senha-errada-999")
    print(f"Resultado da operação (falha): {resultado_falha_produto}")
    print("Verificando se a lista de produtos não foi alterada:")
    # Imprime apenas os nomes para a lista ficar mais curta
    print([produto[1] for produto in listar_produtos()]) 

    # Teste 2: Senha correta
    print("\nTentando deletar o produto ID 2 (Colar) com a senha CORRETA...")
    resultado_sucesso_produto = deletar_produto(id_produto_para_deletar, ADMIN_PASSWORD)
    print(f"Resultado da operação (sucesso): {resultado_sucesso_produto}")
    print("Verificando se o produto foi removido:")
    # Imprime apenas os nomes para a lista ficar mais curta
    print([produto[1] for produto in listar_produtos()])

    # --- PASSO 8: TESTANDO A TRANSAÇÃO COMPLEXA DE DELETAR VENDA ---
    print("\n--- Testando: deletar_venda com estorno de estoque ---")

    # A venda que vamos deletar é a de ID 1.
    # Itens: 2x Brinco (ID 1), 1x Tiara (ID 3)
    # Estoque inicial: Brinco=50, Tiara=10.
    # Após a venda: Brinco=48, Tiara=9.
    # Após o delete: Brinco deve voltar para 50, Tiara para 10.
    
    id_venda_para_deletar = 1
    
    print("\nVerificando estoque ANTES do delete da venda:")
    # Vamos pegar o estoque de todos os produtos para comparar
    estoque_antes = {p[1]: p[3] for p in listar_produtos()}
    print(estoque_antes)
    
    print(f"\nTentando deletar a Venda ID {id_venda_para_deletar} com a senha correta...")
    resultado_delete_venda = deletar_venda(id_venda_para_deletar, ADMIN_PASSWORD)
    print(f"Resultado da operação: {resultado_delete_venda}")
    
    print("\nVerificando se a venda foi removida:")
    vendas_atuais = listar_vendas()
    print(f"Vendas atuais no sistema: {vendas_atuais}")
    if not any(v[0] == id_venda_para_deletar for v in vendas_atuais):
        print(f"-> Sucesso! Venda {id_venda_para_deletar} não encontrada.")
    else:
        print(f"-> FALHA! Venda {id_venda_para_deletar} ainda existe.")

    print("\nVerificando estoque DEPOIS do delete (esperamos o estorno):")
    estoque_depois = {p[1]: p[3] for p in listar_produtos()}
    print(estoque_depois)

    # --- PASSO FINAL: TESTANDO A SUPER-FUNÇÃO ATUALIZAR_PRODUTO ---
    print("\n--- Testando: a super-função atualizar_produto ---")
    
    id_alvo_brinco = 1 # Nosso alvo será o 'Brinco'
    
    print("\nEstado inicial dos produtos:")
    print(listar_produtos())

    # Cenário 1: Falha (senha errada)
    print("\n1. Testando falha com senha errada...")
    resultado_falha = atualizar_produto(id_alvo_brinco, "senha-ruim", novo_nome="NOME NAO DEVE MUDAR")
    print(f"Resultado: {resultado_falha}")

    # Cenário 2: Sucesso (só o nome)
    print("\n2. Testando atualização apenas do NOME...")
    resultado_nome = atualizar_produto(id_alvo_brinco, ADMIN_PASSWORD, novo_nome="Brinco de Prata")
    print(f"Resultado: {resultado_nome}")

    # Cenário 3: Sucesso (só o preço)
    print("\n3. Testando atualização apenas do PREÇO...")
    resultado_preco = atualizar_produto(id_alvo_brinco, ADMIN_PASSWORD, novo_preco=35.50)
    print(f"Resultado: {resultado_preco}")
    
    # Cenário 4: Sucesso (nome e preço juntos)
    print("\n4. Testando atualização de NOME e PREÇO simultaneamente...")
    id_alvo_tiara = 3 # Agora vamos na Tiara
    resultado_ambos = atualizar_produto(id_alvo_tiara, ADMIN_PASSWORD, novo_nome="Tiara de Festa", novo_preco=22.0)
    print(f"Resultado: {resultado_ambos}")

    print("\n--- Verificação Final ---")
    print("Estado final dos produtos após todas as atualizações:")
    print(listar_produtos())


    print("\n--- TODOS OS TESTES (INCLUINDO DELETE) CONCLUÍDOS ---")

    print("\n--- TODOS OS TESTES CONCLUÍDOS ---")