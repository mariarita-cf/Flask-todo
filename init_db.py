import sqlite3

# Conecta (ou cria) o banco
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Cria a tabela de tarefas, se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conteudo TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Banco de dados e tabela criados com sucesso!")
