import sqlite3

conn = sqlite3.connect('tarefas.db')
cursor = conn.cursor()

cursor.execute('''
    DROP TABLE IF EXISTS tarefas
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conteudo TEXT NOT NULL,
        concluida INTEGER NOT NULL DEFAULT 0,
        criada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("Banco de dados recriado com sucesso com campo 'concluida' e 'criada_em'!")
