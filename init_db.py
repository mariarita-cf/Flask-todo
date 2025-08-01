import psycopg2
import os

db_url = os.getenv("DATABASE_URL", "postgresql://tarefas_db_aw40_user:ScEtNdQZYgL8Ug0WFJqhcj2bVjfk0u3j@dpg-d26005ali9vc73a16p90-a/tarefas_db_aw40")

conn = psycopg2.connect(db_url)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id SERIAL PRIMARY KEY,
        conteudo TEXT NOT NULL,
        concluida BOOLEAN DEFAULT FALSE
    );
''')

conn.commit()
cursor.close()
conn.close()
print("Tabela criada com sucesso.")
