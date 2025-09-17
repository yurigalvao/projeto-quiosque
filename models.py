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
        self._preco = preco
        self._quantidade_estoque = quantidade_estoque
        self.categoria = categoria


    def remover_estoque(self, quantidade):
        if quantidade <= self.quantidade_estoque:
            self.quantidade_estoque -= quantidade
            print(f'Estoque do produto "{self.nome}" atualizado para {self.quantidade_estoque}')
            return True
        else:
            print(f'Tentativa de remover {quantidade} do produto "{self.nome}" falhou. Estoque insuficiente!')
            return False
        
    def __str__(self):
        # Dentro do método __str__
        return f"{self.nome} [Estoque: {self.quantidade_estoque}] - R$ {self.preco:.2f}"
    
    def __repr__(self):
        return self.__str__()
    
    @classmethod
    def from_string(cls, texto):
        partes_produto = texto.split('-')
        nome = partes_produto[0]
        preco = float(partes_produto[1])
        categoria = Categoria(partes_produto[2])
        quantidade = int(partes_produto[3])
        return cls(nome, preco, categoria, quantidade)
    
    @staticmethod
    def formatar_moeda(valor):
        return f'R${valor:.2f}'
    
    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, novo_preco):
        if novo_preco >= 0:
            self._preco = novo_preco
        else:
            raise ValueError('O preço não pode ser negativo!')

    @property
    def quantidade_estoque(self):
        return self._quantidade_estoque
    
    @quantidade_estoque.setter
    def quantidade_estoque(self, valor):
        if valor > 0:
            self._quantidade_estoque = valor
        else:
            raise ValueError('Quantidade de estoque inválida!')


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

class EstoqueCompleto:
    def __init__(self):
        self.produtos_por_categoria = {}

    def adicionar_produto(self, produto: Produto):
        categoria_nome = produto.categoria.nome
        if categoria_nome not in self.produtos_por_categoria:
            self.produtos_por_categoria[categoria_nome] = [produto]
        else:
            self.produtos_por_categoria[categoria_nome].append(produto)


    def listar_produtos_por_categoria(self, categoria_nome: str):
        """
        Retorna uma lista de produtos de uma categoria especifica.
        Se a categoria não for encontrada, retorna uma lista vazia
        """
        if categoria_nome in self.produtos_por_categoria:
            return self.produtos_por_categoria[categoria_nome]
        else:
            return []
        
