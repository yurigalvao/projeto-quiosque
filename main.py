from models import Categoria, Produto, ItemVenda, Venda

# Criamos a nossa "etiqueta"
cat_brincos = Categoria(nome='Brincos')

produto1 = Produto(
    nome='Argola Simples',
    preco=25.00,
    categoria=cat_brincos,
    quantidade_estoque=15
    )

produto2 = Produto(
    nome='Colar de Pérola',
    preco=80.00,
    categoria=Categoria(nome='Colares'),
    quantidade_estoque=10
    )




venda1 = Venda()
print(f'Carrinho criado. Valor total inicial: R${venda1.valor_total}')

venda1.adicionar_item(produto=produto1, quantidade=2)
print(f'Adicionando 2x "Argola Simples". Novo valor total: R${venda1.valor_total}')

venda1.adicionar_item(produto=produto2, quantidade=1)
print(f'Adicionando 1x "Colar de Pérolas". Novo valor total: R${venda1.valor_total}')

