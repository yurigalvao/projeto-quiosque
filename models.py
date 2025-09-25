from datetime import datetime
from dataclasses import dataclass, field

class InsufficientStockError(Exception):
    pass

@dataclass
class Category:
    name: str

    def __str__(self):
        return f'{self.name}'
    
    def __repr__(self):
        return f"Category(name='{self.name}')"

class Product:
    """ Representa um item específico e vendável do estoque."""
    def __init__(self, name: str, price: float, category: Category, stock_quantity: int):
        """
        Construtor da classe Produto.

        Args:
            nome (str): O nome descritivo do produto.
            preco (float): O preço de venda do produto.
            categoria (Categoria): O objeto da categoria à qual o produto pertence.
            quantidade_estoque (int): A quantidade inicial de unidades em estoque.
        """
        self.name = name
        self._price = price
        self._stock_quantity = stock_quantity
        self.category = category

    def remove_from_stock(self, quantity):
        if quantity <= self.stock_quantity:
            self.stock_quantity -= quantity
        else:
            raise InsufficientStockError(f'Attempt to remove {quantity} from product "{self.name}" failed. Insufficient stock!')
        
    def __str__(self):
        # Dentro do método __str__
        return f"{self.name} [Estoque: {self.stock_quantity}] - R$ {self.price:.2f}"
    
    def __repr__(self):
        return f"Product(name='{self.name}', price={self.price}, category={self.category!r}, stock_quantity={self.stock_quantity})"
    
    @classmethod
    def from_string(cls, text):
        product_parts = text.split('-')
        name = product_parts[0]
        price = float(product_parts[1])
        category = Category(product_parts[2])
        quantity = int(product_parts[3])
        return cls(name, price, category, quantity)
    
    @staticmethod
    def format_currency(value): #formatar moeda 
        return f'R${value:.2f}'
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price >= 0:
            self._price = new_price
        else:
            raise ValueError('Price cannot be negative!')

    @property
    def stock_quantity(self):
        return self._stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):
        if value > 0:
            self._stock_quantity = value
        else:
            raise ValueError('Invalid stock quantity!')

@dataclass
class SaleItem:
    """Representa uma linha de item dentro de uma Venda completa."""
    product: Product
    quantity: int
    subtotal: float = field(init=False)

    def __post_init__(self):
        self.subtotal = self.product.price * self.quantity





class Sale:
    """Representa uma transação completa, contendo um ou mais itens."""
    def __init__(self):
        """
        Contrutor da classe Venda. Inicia um 'carrinho de compras' novo.
        """
        # Registra o momento exato em que a venda foi criada
        self.date_hour = datetime.now()

        # A lista de itens começa vazia. Ela guardará objetos da classe ItemVenda.
        self.items = []

        # O valor total da venda começa, logicamente, em zero.
        self.total_value = 0.0

    def add_item(self, product: Product, quantity: int):
        """
        Adiciona um novo item (Produto e quantidade) à lista da venda.
        
        Args:
            produto (Produto): O objeto do produto a ser adicionado.
            quantidade (int): A quantidade de unidades a ser adicionada.
        """
        # Cria um novo objeto ItemVenda para representar esta linha de transação
        new_item = SaleItem(quantity=quantity, product=product)

        # Adiciona o novo item à lista 'itens' da venda
        self.items.append(new_item)

        # Sempre que um novo item é adicionado, o valor total da venda é recalculado
        self.update_total_value()

    def update_total_value(self):
        """
        Soma os subtotais de todos os itens na lista para obter o valor total da venda.
        Este método é chamado internamente sempre que um item é adicionado.
        """
        total = 0.0
        # Itera sobre cada objeto 'ItemVenda' na lista 'self.itens'
        for item in self.items:
            # Soma o subtotal de cada item à variável 'total'
            total += item.subtotal

        # Atualiza o atributo 'valor_total' da venda com a soma calculada    
        self.total_value = total

    def finish_sale(self):
            for item in self.items:
                try:
                    item.product.remove_from_stock(item.quantity)
                except InsufficientStockError:
                    print('Erro de estoque! Estoque insuficiente!')


class Stock:
    def __init__(self):
        self.products_by_category = {}

    def add_product(self, product: Product):
        category_name = product.category.name
        if category_name not in self.products_by_category:
            self.products_by_category[category_name] = [product]
        else:
            self.products_by_category[category_name].append(product)


    def list_products_by_category(self, category_name: str):
        """
        Retorna uma lista de produtos de uma categoria especifica.
        Se a categoria não for encontrada, retorna uma lista vazia
        """
        if category_name in self.products_by_category:
            return self.products_by_category[category_name]
        else:
            return []
        
