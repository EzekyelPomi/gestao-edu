import os
import sqlite3
from flask import Flask,render_template,request,redirect,url_for

app = Flask(__name__)
os.makedirs(app.instance_path,exist_ok=True)

DATABASE = os.path.join(app.instance_path,"escola.db")

def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    with conectar_banco() as conexao:
        conexao.execute(""" CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, turma TEXT NOT NULL) """)
        conexao.execute(""" CREATE TABLE IF NOT EXISTS turma (id INTEGER PRIMARY KEY AUTOINCREMENT, nomeTurma TEXT NOT NULL UNIQUE, nivelEns TEXT NOT NULL, turno TEXT NOT NULL) """)

criar_tabela()

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/consultar")
def consultar():
    busca = request.args.get("busca","").strip()
    with conectar_banco() as conexao:
            if busca:
                dados_alunos = conexao.execute("""SELECT id, nome,turma FROM alunos WHERE nome LIKE ? OR turma LIKE ? ORDER BY id DESC""",(f"%{busca}%", f"%{busca}%")).fetchall()
            else:
                dados_alunos = conexao.execute("SELECT id,nome,turma FROM alunos ORDER BY id DESC").fetchall()
    return render_template("listagem.html", alunos = dados_alunos, busca = busca)

@app.route("/cadastrar", methods = ["GET","POST"])
def cadastrar():
    with conectar_banco() as conexao:
        turmas = conexao.execute("SELECT nomeTurma FROM turma ORDER BY nomeTurma DESC").fetchall()
    if request.method == "POST":
        nome = request.form["nome"].strip().upper()
        turma = request.form["turma"].strip().upper()
        if not nome or not turma:
            return "Nome e turma são obrigatorios.", 400
        with conectar_banco() as conexao:
            conexao.execute("INSERT INTO alunos (nome, turma) VALUES (?,?)",(nome,turma))
        return redirect(url_for("consultar"))
    return render_template("cadastro.html", turmas = turmas)

@app.route("/cadastrarTurma", methods = ["GET", "POST"])
def cadastrarTurma():
    if request.method == "POST":
        turma = request.form["nomeT"].strip().upper()
        nivelEns = request.form["nivel"].strip().upper()
        turno = request.form["turno"].strip().upper()
        if not turma or not nivelEns or not turno:
            return "Nome da turma necessário", 400
        with conectar_banco() as conexao:
            conexao.execute("INSERT INTO turma (nomeTurma, nivelEns, turno) VALUES (?,?,?)", (turma, nivelEns, turno))
            return redirect(url_for("cadastrar"))
    return render_template("cadastrarTurma.html")

if __name__ == "__main__":
    app.run(debug=True)