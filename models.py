from datetime import datetime

class Categoria:
    """ Representa uma categoria para agrupar produtos. Ex: Brincos, Colares."""
    def __init__(self, nome: str):
        """
        Construtor da classe Categoria.

        Args:
            nome (str): O nome da categoria a ser criada.
        """
        self.nome = nome



class Produto:
    """ Representa um item específico e vendável do estoque."""
    def __init__(self, nome: str, preco: float, categoria: Categoria, quantidade_estoque: int):
        """
        Construtor da classe Produto.

        Args:
            nome (str): O nome descritivo do produto.
            preco (float): O preço de venda do produto.
            categoria (Categoria): O objeto da categoria à qual o produto pertence.
            quantidade_estoque (int): A quantidade inicial de unidades em estoque.
        """
        self.nome = nome
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.categoria = categoria



class ItemVenda:
    """Representa uma linha de item dentro de uma Venda completa."""
    def __init__(self, quantidade: int, produto: Produto):
        """
        Construtor da classe ItemVenda.

        Args:
            quantidade (int): A quantidade de unidades vendadas deste produto.
            produto (Produto): O objeto do produto que está sendo vendido.
        """
        # Guarda a quantidade de itens vendidos
        self.quantidade = quantidade

        # Gurada a referência para o objeto Produto completo.
        self.produto = produto

        # Calcula o subtotal automaticamente no momento da criação
        self.subtotal = produto.preco * self.quantidade



class Venda:
    """Representa uma transação completa, contendo um ou mais itens."""
    def __init__(self):
        """
        Contrutor da classe Venda. Inicia um 'carrinho de compras' novo.
        """
        # Registra o momento exato em que a venda foi criada
        self.data_hora = datetime.now()

        # A lista de itens começa vazia. Ela guardará objetos da classe ItemVenda.
        self.itens = []

        # O valor total da venda começa, logicamente, em zero.
        self.valor_total = 0.0

    def adicionar_item(self, produto: Produto, quantidade: int):
        """
        Adiciona um novo item (Produto e quantidade) à lista da venda.
        
        Args:
            produto (Produto): O objeto do produto a ser adicionado.
            quantidade (int): A quantidade de unidades a ser adicionada.
        """
        # Cria um novo objeto ItemVenda para representar esta linha de transação
        novo_item = ItemVenda(quantidade=quantidade, produto=produto)

        # Adiciona o novo item à lista 'itens' da venda
        self.itens.append(novo_item)

        # Sempre que um novo item é adicionado, o valor total da venda é recalculado
        self.atualizar_valor_total()

    def atualizar_valor_total(self):
        """
        Soma os subtotais de todos os itens na lista para obter o valor total da venda.
        Este método é chamado internamente sempre que um item é adicionado.
        """
        total = 0.0
        # Itera sobre cada objeto 'ItemVenda' na lista 'self.itens'
        for item in self.itens:
            # Soma o subtotal de cada item à variável 'total'
            total += item.subtotal

        # Atualiza o atributo 'valor_total' da venda com a soma calculada    
        self.valor_total = total