from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Usa o caminho certo no Render: /tmp
DB_PATH = '/tmp/tarefas.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Cria a tabela se ainda não existir
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Executa ao iniciar
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nova_tarefa = request.form.get('tarefa')
        if nova_tarefa:
            conn = get_db_connection()
            conn.execute('INSERT INTO tarefas (conteudo) VALUES (?)', (nova_tarefa,))
            conn.commit()
            conn.close()
        return redirect('/')

    conn = get_db_connection()
    tarefas = conn.execute('SELECT * FROM tarefas ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', tarefas=tarefas)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    novo_conteudo = request.form.get('novo_conteudo')
    if novo_conteudo:
        conn = get_db_connection()
        conn.execute('UPDATE tarefas SET conteudo = ? WHERE id = ?', (novo_conteudo, id))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_tarefa(id):
    conn = get_db_connection()
    tarefa = conn.execute('SELECT concluida FROM tarefas WHERE id = ?', (id,)).fetchone()
    if tarefa:
        novo_status = 0 if tarefa['concluida'] else 1
        conn.execute('UPDATE tarefas SET concluida = ? WHERE id = ?', (novo_status, id))
        conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)







