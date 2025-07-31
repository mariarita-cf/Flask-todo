from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('tarefas.db')
    conn.row_factory = sqlite3.Row
    return conn

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

    # Listar tarefas do banco (corrigido: sem "criada_em")
    conn = get_db_connection()
    tarefas = conn.execute('SELECT * FROM tarefas ORDER BY id DESC').fetchall()
    conn.close()

    return render_template('index.html', tarefas=tarefas)

# Rota para remover uma tarefa
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Rota para alternar o status de conclusão
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

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)






