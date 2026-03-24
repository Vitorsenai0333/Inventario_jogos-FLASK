from flask import Flask, jsonify, request
import sqlite3

# Inicializa a aplicação Flask (responsável por gerenciar rotas e requisições)
app = Flask(__name__)

# Função genérica para executar comandos no banco de dados
# Essa função centraliza toda a comunicação com o banco de dados,
# evitando repetição de código nas rotas (reutilização)
def executar_query(query, *args, fetch=False, commit=False):
    # Conecta ao banco SQLite
    conn = sqlite3.connect('estoque_papelaria.db')
    
    # Permite acessar colunas pelo nome (ex: item['nome'])
    conn.row_factory = sqlite3.Row
    
    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()
    
    resultado = None

    # O try garante execução da query, e o finally garante que a conexão será fechada
    try:
        # Executa a query com segurança usando placeholders (?)
        # Os valores são passados separadamente para evitar SQL Injection
        # (não concatena strings diretamente na query)
        cursor.execute(query, args)
        
        # Se for INSERT, UPDATE ou DELETE → salva as alterações
        if commit:
            conn.commit()
        
        # Se for SELECT → busca os dados
        if fetch:
            resultado = cursor.fetchall()
    
    finally:
        # Fecha a conexão mesmo se ocorrer erro
        conn.close()
    
    # Retorna o resultado (ou None)
    return resultado


# Rota para listar todos os produtos OU buscar por ID
# Essa função atende duas rotas: uma lista todos e outra busca por ID
@app.route('/produtos', methods=['GET'])
@app.route('/produtos/<int:id>', methods=['GET'])
def gerenciar_produtos(id=None):
    
    # Se um ID foi passado → busca um produto específico
    if id:
        produto = executar_query("SELECT * FROM produtos WHERE id = ?", id, fetch=True)
        
        # Se encontrou, retorna o produto
        if produto:
            return jsonify(dict(produto[0])), 200
        
        # Se não encontrou, retorna erro 404
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Se não passou ID → lista todos os produtos
    dados = executar_query("SELECT id, nome, quantidade, preco FROM produtos", fetch=True)
    
    # Converte todos os registros retornados em uma lista de dicionários
    lista_produtos = [dict(item) for item in dados]
    
    return jsonify(lista_produtos), 200


# Rota para inserir um novo produto
@app.route('/insert', methods=['POST'])
def criar_produto():
    
    # Recebe os dados enviados pelo cliente no corpo da requisição (JSON)
    dados = request.get_json()
    
    # Insere no banco usando os valores recebidos
    executar_query(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'),
        commit=True  # Salva no banco
    )
    
    # Retorna uma resposta em formato JSON confirmando a criação do produto
    return jsonify({"mensagem": "Produto criado com sucesso!"}), 201


# Rota para atualizar um produto existente
# PUT é usado para atualizar completamente os dados de um recurso existente
@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    
    # Recebe os dados enviados pelo cliente no corpo da requisição (JSON)
    dados = request.get_json()
    
    # Verifica se o produto existe no banco
    existe = executar_query("SELECT id FROM produtos WHERE id = ?", id, fetch=True)
    
    # Se não existir, retorna erro
    if not existe:
        # Código HTTP indica o resultado da operação (404 = não encontrado)
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Atualiza os dados do produto
    executar_query(
        "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'), id,
        commit=True  # Salva alteração
    )
    
    # Retorna sucesso (204 = operação realizada sem necessidade de retornar dados)
    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 204


# Rota para deletar um produto
# DELETE remove um registro do banco com base no ID informado
@app.route('/delete/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    
    # Verifica se o produto existe
    produto = executar_query("SELECT nome FROM produtos WHERE id = ?", id, fetch=True)
    
    # Se não existir, retorna erro
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Deleta o produto
    executar_query("DELETE FROM produtos WHERE id = ?", id, commit=True)
    
    # Retorna mensagem com o nome do produto removido
    return jsonify({"mensagem": f"Produto '{produto[0]['nome']}' removido!"}), 200


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)  # Ativa modo debug (mostra erros e reinicia automaticamente)