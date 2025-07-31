from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Caminho do banco de dados no diretório temporário (Render só permite escrita em /tmp)
DB_PATH = '/tmp/tarefas.db'

# Função para conectar e garantir que a tabela existe
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

# Página principal: listar e adicionar tarefas
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

# Marcar ou desmarcar uma tarefa como concluída
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

# Editar o conteúdo de uma tarefa
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    novo_conteudo = request.form.get('novo_conteudo')
    if novo_conteudo:
        conn = get_db_connection()
        conn.execute('UPDATE tarefas SET conteudo = ? WHERE id = ?', (novo_conteudo, id))
        conn.commit()
        conn.close()
    return redirect('/')

# Deletar uma tarefa
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Iniciar o servidor Flask corretamente no Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

