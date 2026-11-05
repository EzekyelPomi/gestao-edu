import os
import sqlite3
from flask import Flask,render_template,request,redirect,url_for
from datetime import datetime

app = Flask(__name__)
os.makedirs(app.instance_path,exist_ok=True)

DATABASE = os.path.join(app.instance_path,"escola.db")

def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    with conectar_banco() as conexao:
#       conexao.execute(""" 
#       CREATE TABLE IF NOT EXISTS alunos (
#       id INTEGER PRIMARY KEY AUTOINCREMENT, 
#       nome TEXT NOT NULL, 
#       turma TEXT NOT NULL) """)
#       conexao.execute(""" 
#       CREATE TABLE IF NOT EXISTS turma (
#       id INTEGER PRIMARY KEY AUTOINCREMENT, 
#       nomeTurma TEXT NOT NULL UNIQUE, 
#       nivelEns TEXT NOT NULL, 
#       turno TEXT NOT NULL) """)

        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_completo TEXT NOT NULL,
        nome_responsavel TEXT NOT NULL, 
        data_nascimento DATE NOT NULL,
        cpf_aluno VARCHAR(11) UNIQUE) 
        """)
        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_turma TEXT NOT NULL UNIQUE, 
        nivel_ens TEXT NOT NULL,
        turno TEXT NOT NULL,
        ano_letivo INTEGER NOT NULL,
        sala TEXT) 
        """)
        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_professor TEXT NOT NULL UNIQUE, 
        formacao TEXT NOT NULL) 
        """)
        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_disciplina TEXT NOT NULL UNIQUE) 
        """)
        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS matriculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_aluno INTEGER NOT NULL,
        id_turma INTEGER NOT NULL,
        data_matricula DATE NOT NULL,
        
        FOREIGN KEY (id_aluno) REFERENCES alunos(id),
        FOREIGN KEY (id_turma) REFERENCES turmas(id)) 
        """)
        conexao.execute("""
        CREATE TABLE IF NOT EXISTS atribuicoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_turma_at INTEGER NOT NULL,
        id_professor_at INTEGER NOT NULL,
        id_disciplina_at INTEGER NOT NULL,
        
        FOREIGN KEY (id_turma_at) REFERENCES turmas(id),
        FOREIGN KEY (id_professor_at) REFERENCES professores(id),
        FOREIGN KEY (id_disciplina_at) REFERENCES disciplinas(id))
        """)
        conexao.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_atribuicao_av INTEGER NOT NULL,
        descricao_av TEXT,
        nota_max_av REAL,
        
        FOREIGN KEY (id_atribuicao_av) REFERENCES atribuicoes(id),
        CHECK (nota_max_av >= 0))
        """)
        conexao.execute("""
        CREATE TABLE IF NOT EXISTS notas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_matricula_nt INTEGER NOT NULL,
        id_avaliacao_nt INTEGER NOT NULL,
        nota REAL,
        
        FOREIGN KEY (id_matricula_nt) REFERENCES matriculas(id),
        FOREIGN KEY (id_avaliacao_nt) REFERENCES avaliacoes(id),
        
        CHECK (nota >= 0),
        UNIQUE (id_matricula_nt, id_avaliacao_nt))
        """)

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
    ano_atual = datetime.now().year
    if request.method == "POST":
        turma = request.form["nomeT"].strip().upper()
        nivelEns = request.form["nivel"].strip().upper()
        turno = request.form["turno"].strip().upper()
        if not turma or not nivelEns or not turno:
            return "Nome da turma necessário", 400
        with conectar_banco() as conexao:
            conexao.execute("INSERT INTO turmas (nome_turma, nivel_ens, turno, ano_letivo) VALUES (?,?,?,?)", (turma, nivelEns, turno, ano_atual))
            return redirect(url_for("cadastrar"))
    return render_template("cadastrarTurma.html")

if __name__ == "__main__":
    app.run(debug=True)