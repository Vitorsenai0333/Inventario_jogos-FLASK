from flask import Flask, jsonify, request
import sqlite3

# Cria a aplicação Flask
app = Flask(__name__)

# Função genérica para executar comandos no banco de dados
def executar_query(query, *args, fetch=False, commit=False):
    # Conecta ao banco SQLite
    conn = sqlite3.connect('estoque_papelaria.db')
    
    # Permite acessar colunas pelo nome (ex: item['nome'])
    conn.row_factory = sqlite3.Row
    
    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()
    
    resultado = None
    
    try:
        # Executa a query com segurança usando placeholders (?)
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
    
    # Converte cada linha do banco em dicionário
    lista_produtos = [dict(item) for item in dados]
    
    return jsonify(lista_produtos), 200


# Rota para inserir um novo produto
@app.route('/insert', methods=['POST'])
def criar_produto():
    
    # Pega os dados enviados em JSON
    dados = request.get_json()
    
    # Insere no banco usando os valores recebidos
    executar_query(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'),
        commit=True  # Salva no banco
    )
    
    # Retorna mensagem de sucesso
    return jsonify({"mensagem": "Produto criado com sucesso!"}), 201


# Rota para atualizar um produto existente
@app.route('/update/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    
    # Recebe os novos dados
    dados = request.get_json()
    
    # Verifica se o produto existe no banco
    existe = executar_query("SELECT id FROM produtos WHERE id = ?", id, fetch=True)
    
    # Se não existir, retorna erro
    if not existe:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Atualiza os dados do produto
    executar_query(
        "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
        dados.get('nome'), dados.get('quantidade'), dados.get('preco'), id,
        commit=True  # Salva alteração
    )
    
    # Retorna sucesso (sem conteúdo)
    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 204


# Rota para deletar um produto
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
    app.run(debug=True)  # Debug mostra erros e reinicia automaticamente