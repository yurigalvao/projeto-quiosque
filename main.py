from models import Category, Product, Sale, Stock

# Criamos a nossa "etiqueta"
cat_brincos = Category(name='Brincos')
#cat_teste = Categoria(nome='teste')

#print(cat_teste)
produto1 = Product(
    name='Argola Simples',
    price=25.00,
    category=cat_brincos,
    stock_quantity=15
    )

produto2 = Product(
    name='Colar de Pérola',
    price=80.00,
    category=Category(name='Colares'),
    stock_quantity=10
    )




venda1 = Sale()
print(f'Carrinho criado. Valor total inicial: R${venda1.total_value}')

venda1.add_item(product=produto1, quantity=2)
print(f'Adicionando 2x "Argola Simples". Novo valor total: R${venda1.total_value}')

venda1.add_item(product=produto2, quantity=1)
print(f'Adicionando 1x "Colar de Pérolas". Novo valor total: R${venda1.total_value}')

print()

print('Resumo da venda')
print(f'Valr total da venda: R${venda1.total_value:.2f}')
print('Itens vendidos:')
for item in venda1.items:
    print(f'{item.quantity}x {item.product.name} (Subtotal: R$ {item.subtotal:.2f})')

print()

print('Finalizando a venda e atualizando o estoque')
venda1.finish_sale()
print()

print('Estoque final')
print(f' - Estoque de "{produto1.name}": {produto1.stock_quantity}')
print(f' - Estoque de "{produto2.name}": {produto2.stock_quantity}')

print()

estoque = Stock()
estoque.add_product(produto1)
estoque.add_product(produto2)

print('Mostrando estoque completo')
print(estoque.products_by_category)


print('TESTES FINALIZADOS COM SUCESSO!')

print()
print('Testes ')

produto3 = Product.from_string('Brinco-12-Brincos-10')
print(produto3)

try:
    produto4 = Product.from_string('Colar-30')
except Exception:
    print('Erro de atribuição de objeto')
#produto3 = Produto(
#   nome='Brinco',
#   preco= 12.00,
#   categoria= Categoria(nome='Brincos'),
#   quantidade_estoque= 10
#)

#produto3.preco = 15
#print(produto3)

#try:
#    produto3.preco = -2
#except Exception:
#    print('Valor inválido')

#produto3.quantidade_estoque = 20
#print(produto3.quantidade_estoque)

#try:
#    produto3.quantidade_estoque = -10
#except Exception:
#    print('Quantidade Inválida!')
