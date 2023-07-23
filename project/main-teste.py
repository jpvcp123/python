from flask import Flask, render_template, url_for, redirect, request, flash
import psycopg2 
import psycopg2.extras
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = "caramelo-teste"

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

table_check_query = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'cliente');"

conn.autocommit = True
cursor = conn.cursor()

cursor.execute(table_check_query)
table_exists = cursor.fetchone()[0]

if not table_exists:
    sql = '''CREATE TABLE cliente (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(40) NOT NULL,
        telefone VARCHAR(40) NOT NULL,
        cpf VARCHAR(40) NOT NULL,
        email VARCHAR(40) NOT NULL
    );'''
    
    cursor.execute(sql)
    conn.commit()
    print("Table 'cliente' created successfully.")
else: 
    print("Table 'cliente' already exists.")


@app.route("/")
def index():
    return render_template("main.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("register.html")

@app.route("/cadastro", methods=['POST'])
def cadastro():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        nome = request.form["Nome"]
        telefone = request.form["Telefone"]
        cpf = request.form["CPF"]
        email = request.form["Email"]
        cur.execute("INSERT INTO cliente (Nome, Telefone, CPF, Email) VALUES (%s,%s,%s,%s)", (nome, telefone, cpf, email))
        
        conn.commit()
        flash('User Added successfully')
        
        return redirect(url_for("index"))

@app.route("/lista")
def lista():
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM cliente"
    cur.execute(s) 
    pessoas = cur.fetchall()
    
    return render_template("list.html",pessoas=pessoas)

@app.route("/excluir/<int:id>")
def excluir(id):
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM cliente WHERE id = {0}'.format(id))
    conn.commit()
    flash('Client Removed Successfully')

    return redirect(url_for('lista'))

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = "SELECT * FROM cliente"
    if request.method == 'POST':
        nome = request.form['Nome']
        telefone = request.form['Telefone']
        email = request.form['Email']
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE cliente
            SET Nome = %s,
                Telefone = %s,
                Email = %s
            WHERE id = %s
        """, (nome, telefone, email, id))
        flash('Student Updated Successfully')
        conn.commit()
        return redirect(url_for('lista'))
    return render_template("update.html", pessoa=pessoa)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    
