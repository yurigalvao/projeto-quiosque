from models import Categoria, Produto, Venda, EstoqueCompleto

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

print()

print('Resumo da venda')
print(f'Valr total da venda: R${venda1.valor_total:.2f}')
print('Itens vendidos:')
for item in venda1.itens:
    print(f'{item.quantidade}x {item.produto.nome} (Subtotal: R$ {item.subtotal:.2f})')

print()

print('Finalizando a venda e atualizando o estoque')
for item in venda1.itens:
    sucesso_na_remocao = item.produto.remover_estoque(item.quantidade)

    if sucesso_na_remocao:
        print(f'-> Baixa no estoque de "{item.produto.nome}" realizada!')
    else:
        print(f'-> FALHA na baixa de estoque de "{item.produto.nome}". Estoque insuficiente!')

print()

print('Estoque final')
print(f' - Estoque de "{produto1.nome}": {produto1.quantidade_estoque}')
print(f' - Estoque de "{produto2.nome}": {produto2.quantidade_estoque}')

print()

estoque = EstoqueCompleto()
estoque.adicionar_produto(produto1)
estoque.adicionar_produto(produto2)

print('Mostrando estoque completo')
print(estoque.produtos_por_categoria)


print('TESTES FINALIZADOS COM SUCESSO!')
