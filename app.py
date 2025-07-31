from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Caminho do banco no ambiente Render (escrita permitida)
DB_PATH = '/tmp/tarefas.db'

# Função para conectar ao banco
def get_db_connection():
    # Cria o banco se não existir
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Cria a tabela, se ainda não existir
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    return conn








