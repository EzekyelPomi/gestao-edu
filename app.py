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

criar_tabela()

@app.route("/")
def inicio():
    busca = request.args.get("busca","").strip()
    with conectar_banco() as conexao:
        if busca:
            dados_alunos = conexao.execute("""SELECT id, nome,turma FROM alunos WHERE nome LIKE ? OR turma LIKE ? ORDER BY id DESC""",(f"%{busca}%", f"%{busca}%")).fetchall()
        else:
            dados_alunos = conexao.execute("SELECT id,nome,turma FROM alunos ORDER BY id DESC").fetchall()
    return render_template("index.html", alunos = dados_alunos, busca = busca)
@app.route("/cadastrar", methods = ["POST"])
def cadastrar():
    nome = request.form["nome"].strip()
    turma = request.form["turma"].strip()

    if not nome or not turma:
        return "Nome e turma são obrigatorios.", 400
    with conectar_banco() as conexao:
        conexao.execute("INSERT INTO alunos (nome, turma) VALUES (?,?)",(nome,turma))
            
    return redirect(url_for("inicio"))

@app.route("/consultar", methods = ["POST"])
def consultar():
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)