#  kiosk-manager (Sistema de Gestão para Quiosque)

## 🎯 Objetivo

Desenvolver um sistema de gestão simples e funcional para pequenos comércios, como quiosques, utilizando Python e os princípios da Programação Orientada a Objetos. O objetivo é criar uma ferramenta para controle de produtos, estoque e vendas.

## ✨ Status do MVP V1.0 (Lógica Implementada)

A lógica central do sistema foi modelada e implementada, aplicando conceitos avançados de POO.

-   [x] **Gestão de Produtos:**
    -   [x] Modelagem de **Categorias** de produtos.
    -   [x] Modelagem de **Produtos** com nome, preço, estoque e categoria associada, incluindo validações.
-   [x] **Gestão de Vendas:**
    -   [x] Registro de **Vendas** com múltiplos itens por transação.
    -   [x] Lógica para **atualização automática do estoque** ao finalizar uma venda.
-   [x] **Robustez do Sistema:**
    -   [x] Implementação de **Exceções Customizadas** para tratamento de erros (ex: `EstoqueInsuficienteError`).

## 🛠️ Conceitos e Tecnologias Aplicadas

-   **Linguagem:** Python 3
-   **Paradigma Principal:** Programação Orientada a Objetos (POO)
-   **Conceitos Chave Utilizados:**
    -   `@dataclasses` para classes de dados limpas e eficientes.
    -   Encapsulamento com `@property` e `@setter` para validações de dados.
    -   Composição para modelar a relação entre `Venda` e `ItemVenda`.
    -   Dunder Methods como `__str__` e `__repr__` para representação de objetos.
    -   Tratamento de Erros com Exceções Customizadas (`try...except`, `raise`).

## 🗺️ Próximos Passos

-   [ ] **Profissionalização:** Refatoração completa do código para o Inglês, seguindo as melhores práticas da indústria.
-   [ ] **Persistência de Dados:** Integração com um banco de dados (provavelmente SQLite ou MySQL) para armazenar produtos, vendas e estoque.
-   [ ] **Interface com o Usuário:** Desenvolvimento de uma Interface de Linha de Comando (CLI) para permitir a interação com o sistema.

## 🚀 Como Executar (Instruções Futuras)

*(Esta seção será preenchida no futuro com as instruções de como instalar e rodar o projeto.)*