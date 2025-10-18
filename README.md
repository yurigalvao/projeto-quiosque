# Kiosk Manager - Sistema de Gestão para Quiosque

## 🎯 Objetivo

Desenvolver um sistema de gestão completo e robusto para pequenos comércios, como quiosques, utilizando Python. O objetivo é criar uma ferramenta para controle de produtos, categorias, estoque e registro de vendas, com uma arquitetura profissional e escalável.

---

## ✨ Status Atual: Backend V2.0 - Funcionalidades Concluídas

A fundação do sistema (backend) está 100% funcional, implementada e testada, pronta para ser conectada a uma interface de usuário.

### Funcionalidades Implementadas:
- [x] **Gestão de Categorias:** CRUD completo (Criar, Listar, Atualizar, Deletar).
- [x] **Gestão de Produtos:** CRUD completo, incluindo uma "super-função" para atualizações flexíveis de nome e preço.
- [x] **Gestão de Vendas:**
    - [x] Registro de vendas complexas com múltiplos itens.
    - [x] **Controle de Estoque Ativo:** Baixa automática no estoque ao vender.
    - [x] Cancelamento de vendas com **estorno** automático de estoque.
- [x] **Segurança:** Operações críticas de "Gerente" (deletar, alterar preços) protegidas por senha.
- [x] **Integridade de Dados:** Validação de estoque e uso de `FOREIGN KEY`s para garantir a consistência do banco de dados.

---

## 🏗️ Arquitetura

O backend foi construído seguindo um padrão de arquitetura em **3 camadas** para garantir organização, flexibilidade e manutenibilidade.

**`Interface (Futuro Django)` <--> `repository.py` <--> `database.py`**

* **`models.py` (As "Plantas de Engenharia"):** Define as classes de negócio (`Product`, `Category`, `Sale`) com suas regras e comportamentos, usando princípios de Programação Orientada a Objetos.

* **`database.py` (O "Armazém de Peças"):** A camada de mais baixo nível. É o **único** arquivo que se comunica diretamente com o banco de dados SQLite3. Ele é responsável por executar os comandos SQL e lidar com a conexão, trabalhando apenas com dados brutos.

* **`repository.py` (A "Fábrica"):** A camada intermediária e a **única porta de entrada** para a interface. Ele age como um "tradutor", convertendo os objetos do `models.py` em dados brutos para o `database.py` (operações de escrita) e convertendo os dados brutos do `database.py` em objetos para a interface (operações de leitura).

---

## 🛠️ Tecnologias e Conceitos Aplicados

-   **Linguagem:** Python 3
-   **Banco de Dados:** SQLite3
-   **Princípios:** Programação Orientada a Objetos (POO), Arquitetura em Camadas (Repository Pattern), Separação de Responsabilidades (SoC).
-   **Bibliotecas:** `python-dotenv` para gerenciamento de segredos.

---

## 🧪 Como Executar a Suíte de Testes

O projeto possui uma suíte de testes integrada que valida toda a funcionalidade do backend.

1.  Clone o repositório.
2.  Crie e ative um ambiente virtual (`venv`).
3.  Instale as dependências: `pip install python-dotenv`.
4.  Crie um arquivo `.env` na raiz do projeto e defina a `ADMIN_PASSWORD`.
5.  Execute o arquivo `repository.py` para rodar os testes de integração:
    ```bash
    python3 repository.py
    ```
A saída do terminal demonstrará o ciclo de vida completo das operações para todas as entidades.

---

## 🗺️ Próximos Passos

Com a arquitetura de backend definida e as funcionalidades do MVP implementadas, os próximos grandes passos para a evolução do projeto são:

- [ ] **Desenvolvimento de Novas Features de Negócio:**
    - [ ] Implementar um sistema de **Relatórios** de vendas (diários, semanais, mensais).
    - [ ] Implementar a funcionalidade de **Abertura e Fechamento de Caixa**.
- [ ] **Fase 3 - Interface com Django:** Iniciar os estudos e o desenvolvimento da interface web para o sistema.