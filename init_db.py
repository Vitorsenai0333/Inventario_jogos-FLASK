import sqlite3

conn = sqlite3.connect('estoque_papelaria.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")