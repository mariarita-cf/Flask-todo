import sqlite3

# Conecta (ou cria) o banco
conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

# Cria a tabela com os novos campos: concluida e criada_em
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conteudo TEXT NOT NULL,
        concluida INTEGER DEFAULT 0,
        criada_em DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("Banco de dados e tabela criados com sucesso!")
