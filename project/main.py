from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__= 'cliente'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)

    def __init__ (self, nome, telefone, cpf, email): 
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/cadastrar")
def cadastrar():
    return render_template("register.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("Nome")
        telefone = request.form.get("Telefone")
        cpf = request.form.get("CPF")
        email = request.form.get("Email")

        if nome and telefone and cpf and email:
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("list.html",pessoas=pessoas)

@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("list.html",pessoas=pessoas)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("Nome")
        telefone = request.form.get("Telefone")
        cpf = request.form.get("CPF")
        email = request.form.get("Email")

        if nome and telefone and email:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.email = email

            db.session.commit()

            return redirect(url_for("lista"))
    
    return render_template("update.html", pessoa=pessoa)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug = True)