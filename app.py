from flask import Flask, render_template, request, redirect
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Função para conectar ao PostgreSQL
def get_db_connection():
    db_url = os.getenv("DATABASE_URL") or "postgresql://tarefas_db_aw40_user:ScEtNdQZYgL8Ug0WFJqhcj2bVjfk0u3j@dpg-d26005ali9vc73a16p90-a.oregon-postgres.render.com/tarefas_db_aw40"
    conn = psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

# Página principal: listar e adicionar tarefas
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nova_tarefa = request.form.get('tarefa')
        if nova_tarefa:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO tarefas (conteudo) VALUES (%s)', (nova_tarefa,))
            conn.commit()
            cur.close()
            conn.close()
        return redirect('/')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM tarefas ORDER BY id DESC')
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', tarefas=tarefas)

# Marcar ou desmarcar uma tarefa como concluída
@app.route('/toggle/<int:id>', methods=['POST'])
def toggle_tarefa(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT concluida FROM tarefas WHERE id = %s', (id,))
    tarefa = cur.fetchone()
    if tarefa:
        novo_status = not tarefa['concluida']
        cur.execute('UPDATE tarefas SET concluida = %s WHERE id = %s', (novo_status, id))
        conn.commit()
    cur.close()
    conn.close()
    return redirect('/')


# Editar o conteúdo de uma tarefa
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    novo_conteudo = request.form.get('novo_conteudo')
    if novo_conteudo:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE tarefas SET conteudo = %s WHERE id = %s', (novo_conteudo, id))
        conn.commit()
        cur.close()
        conn.close()
    return redirect('/')

# Deletar uma tarefa
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tarefas WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

# Iniciar o servidor Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
