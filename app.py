from flask import Flask, jsonify, request
import sqlite3

# Cria a aplicação Flask
app = Flask(__name__)

# Nome do banco de dados
DATABASE = 'estoque_papelaria.db'


# -------------------------------
# FUNÇÃO DE CONEXÃO COM O BANCO
# -------------------------------
def conectar_bd():
    # Abre conexão com o banco
    conn = sqlite3.connect(DATABASE)
    
    # Permite acessar colunas pelo nome (ex: produto['nome'])
    conn.row_factory = sqlite3.Row
    
    return conn


# -----------------------------------------
# FUNÇÃO GENÉRICA PARA EXECUTAR SQL
# -----------------------------------------
def executar_query(sql, parametros=(), buscar=False, salvar=False):
    """
    Essa função serve para executar QUALQUER comando SQL.
    
    Parâmetros:
    - sql: comando SQL (SELECT, INSERT, UPDATE, DELETE)
    - parametros: valores da query (evita SQL Injection)
    - buscar: True se for SELECT
    - salvar: True se for INSERT, UPDATE ou DELETE
    """

    conn = conectar_bd()
    cursor = conn.cursor()

    resultado = None

    try:
        # Executa o comando SQL com parâmetros seguros
        cursor.execute(sql, parametros)

        # Se for modificação (INSERT/UPDATE/DELETE), salva no banco
        if salvar:
            conn.commit()

        # Se for consulta (SELECT), pega os resultados
        if buscar:
            resultado = cursor.fetchall()

    finally:
        # Sempre fecha a conexão (boa prática)
        conn.close()

    return resultado


# -----------------------------------------
# ROTA: LISTAR TODOS OU BUSCAR POR ID
# -----------------------------------------
@app.route('/produtos', methods=['GET'])
@app.route('/produtos/<int:id>', methods=['GET'])
def listar_produtos(id=None):

    # Se foi passado um ID → busca apenas um produto
    if id:
        produto = executar_query(
            "SELECT * FROM produtos WHERE id = ?",
            (id,),
            buscar=True
        )

        # Se não encontrou
        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404

        # Retorna o produto encontrado
        return jsonify(dict(produto[0])), 200

    # Se não passou ID → lista todos
    produtos = executar_query(
        "SELECT * FROM produtos",
        buscar=True
    )

    # Converte lista de objetos para JSON
    lista = [dict(p) for p in produtos]

    return jsonify(lista), 200


# -----------------------------------------
# ROTA: CRIAR PRODUTO (POST)
# -----------------------------------------
@app.route('/produtos', methods=['POST'])
def criar_produto():

    # Recebe os dados em JSON
    dados = request.get_json()

    # Insere no banco
    executar_query(
        "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
        (dados['nome'], dados['quantidade'], dados['preco']),
        salvar=True
    )

    return jsonify({"mensagem": "Produto criado com sucesso"}), 201


# -----------------------------------------
# ROTA: ATUALIZAR PRODUTO (PUT)
# -----------------------------------------
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):

    dados = request.get_json()

    # Verifica se o produto existe
    produto = executar_query(
        "SELECT id FROM produtos WHERE id = ?",
        (id,),
        buscar=True
    )

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Atualiza os dados
    executar_query(
        "UPDATE produtos SET nome = ?, quantidade = ?, preco = ? WHERE id = ?",
        (dados['nome'], dados['quantidade'], dados['preco'], id),
        salvar=True
    )

    return jsonify({"mensagem": "Produto atualizado com sucesso"}), 200


# -----------------------------------------
# ROTA: DELETAR PRODUTO (DELETE)
# -----------------------------------------
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):

    # Verifica se existe
    produto = executar_query(
        "SELECT nome FROM produtos WHERE id = ?",
        (id,),
        buscar=True
    )

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # Remove do banco
    executar_query(
        "DELETE FROM produtos WHERE id = ?",
        (id,),
        salvar=True
    )

    return jsonify({"mensagem": f"Produto '{produto[0]['nome']}' removido"}), 200


# -----------------------------------------
# INICIAR SERVIDOR
# -----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)