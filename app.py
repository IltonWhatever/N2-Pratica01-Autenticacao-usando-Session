from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from flask_session import Session

app = Flask(__name__, template_folder='templates')
app.secret_key = 'asasdeazazel'

# Config de Sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def init_db():
    conn = sqlite3.connect('users.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('pages/index.html',titulo_pagina='Sistema de Cadastro')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.sqlite3')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (username, password) VALUES (?,?)', (username, password))
        conn.commit()
        conn.close()

        # Lógica para criar o usuário no banco de dados (veja Etapa 6)
        flash('Usuário criado com sucesso!')
        return redirect(url_for('index'))
    
    return render_template('pages/register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if username:
            # Aqui você pode criar uma sessão para manter o usuário logado
            session["username"] = request.form.get("username") # Salvando a sessão
            flash('Login realizado com sucesso!')
            return redirect(url_for('userpage'))
        else:
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('index'))


@app.route('/userpage')
def userpage():
    if not session.get("username"):
        return redirect(url_for('index'))
    return render_template('pages/userpage.html')

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
    init_db()