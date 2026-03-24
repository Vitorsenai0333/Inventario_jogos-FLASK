import sqlite3

try:
    # Conecta (ou cria) o banco de dados
    conn = sqlite3.connect('estoque_papelaria.db')
    
    # Cria o cursor para executar comandos SQL
    cursor = conn.cursor()

    # Cria a tabela se ela não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL
    )
    """)

    # Salva as alterações
    conn.commit()

    print("Banco e tabela criados com sucesso!")

except Exception as erro:
    print("Erro ao criar o banco:", erro)

finally:
    # Garante que a conexão será fechada
    conn.close()