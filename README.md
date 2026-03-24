# FireAlert-FLASK
# API CRUD - Sistema de Biblioteca

Este projeto consiste no desenvolvimento de uma API REST utilizando Flask, com o objetivo de gerenciar um sistema de biblioteca. A aplicação permite realizar operações de cadastro, consulta, atualização e remoção de livros armazenados em um banco de dados SQLite.

## Objetivo

Implementar um sistema CRUD (Create, Read, Update, Delete) utilizando Python, Flask e SQLite, seguindo os padrões de requisições HTTP e manipulação de dados em formato JSON.

## Execução do Projeto

Para executar o projeto, siga os passos abaixo:

1. Clonar o repositório:
   git clone URL_DO_REPOSITORIO

2. Acessar a pasta do projeto:
   cd PYFLASK2

3. Criar o ambiente virtual:
   python -m venv venv

4. Ativar o ambiente virtual (Windows):
   venv\Scripts\activate

5. Instalar as dependências:
   pip install flask

## Inicialização do Banco de Dados

O banco de dados é criado por meio de um script de inicialização.

Execute o comando:

python init_db.py

Esse script cria o banco de dados "estoque_papelaria.db" e a tabela "produtos", que armazena os livros.

## Execução da Aplicação

Para iniciar a aplicação, execute:

python app.py

A API ficará disponível em:
http://127.0.0.1:5000/

## Funcionamento da API

A aplicação funciona como um servidor que recebe requisições HTTP e responde com dados em formato JSON.

As operações são realizadas por meio das seguintes rotas:

GET /produtos
Retorna todos os livros cadastrados.

GET /produtos/<id>
Retorna um livro específico com base no ID.

POST /insert
Insere um novo livro no banco de dados. Os dados devem ser enviados em formato JSON.

PUT /update/<id>
Atualiza os dados de um livro existente.

DELETE /delete/<id>
Remove um livro do banco de dados.

## Testes da API

Os testes da aplicação foram realizados utilizando o terminal, por meio da ferramenta curl, que permite simular requisições HTTP.

Exemplo de inserção de um jogo:

curl -X POST http://127.0.0.1:5000/insert -H "Content-Type: application/json" -d "{\"nome\":\"Spider Man Miles Morales\",\"quantidade\":7,\"preco\":179.90}"

Exemplo de listagem dos jogos cadastrados:

curl http://127.0.0.1:5000/produtos

Exemplo de busca por ID:

curl http://127.0.0.1:5000/produtos/1

Exemplo de atualização de um registro:

curl -X PUT http://127.0.0.1:5000/update/1 -H "Content-Type: application/json" -d "{\"nome\":\"God of War Ragnarok\",\"quantidade\":3,\"preco\":249.90}"

Exemplo de remoção de um registro:

curl -X DELETE http://127.0.0.1:5000/delete/1

## Observações

Como se trata de uma API, não há interface gráfica. A interação com o sistema ocorre por meio de requisições HTTP, podendo ser realizadas via terminal, ferramentas como Postman ou aplicações externas.

## Tecnologias Utilizadas

Python
Flask
SQLite

## Considerações Finais

O sistema desenvolvido atende aos requisitos de um CRUD completo, permitindo a manipulação de dados de forma estruturada, utilizando boas práticas de desenvolvimento de APIs REST.

