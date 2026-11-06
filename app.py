import os
import sqlite3
from flask import Flask,render_template,request,redirect,url_for,flash
from datetime import datetime

app = Flask(__name__)
os.makedirs(app.instance_path,exist_ok=True)

DATABASE = os.path.join(app.instance_path,"escola.db")
ano_atual = datetime.now()

def conectar_banco():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def criar_tabela():
    with conectar_banco() as conexao:
        conexao.execute(""" 
        CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome_completo TEXT NOT NULL,
        nome_responsavel TEXT NOT NULL, 
        data_nascimento DATE NOT NULL,
        cpf_aluno VARCHAR(11) UNIQUE CHECK (length(cpf_aluno) = 14)) 
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
        id_aluno INTEGER NOT NULL UNIQUE,
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

@app.route("/cadastrar", methods = ["GET","POST"])
def cadastrar():
    if request.method == "POST":
        nome_completo = request.form["nome_completo"].strip()
        nome_responsavel = request.form["nome_responsavel"].strip()
        data_nascimento = request.form["data_nascimento"].strip()
        cpf_aluno = request.form["cpf_aluno"].strip()
        if not nome_completo or not nome_responsavel or not data_nascimento:
            return "Nome do aluno, nome do responsável e data de nascmiento são obrigatorios.", 400
        with conectar_banco() as conexao:
            cursor = conexao.execute("INSERT INTO alunos (nome_completo, nome_responsavel, data_nascimento, cpf_aluno) VALUES (?,?,?,?)",(nome_completo,nome_responsavel,data_nascimento,cpf_aluno))
            id_aluno = cursor.lastrowid
            return redirect(url_for("matricular_aluno", id_aluno = id_aluno))
        
    return render_template("cadastro.html")

@app.route("/cadastrarTurma", methods = ["GET", "POST"])
def cadastrarTurma():
    if request.method == "POST":
        turma = request.form["nomeT"].strip()
        nivelEns = request.form["nivel"].strip()
        turno = request.form["turno"].strip()
        ano_letivo = request.form["ano_letivo"].strip()
        if not turma or not nivelEns or not turno:
            return "Nome da turma necessário", 400
        with conectar_banco() as conexao:
            conexao.execute("INSERT INTO turmas (nome_turma, nivel_ens, turno, ano_letivo) VALUES (?,?,?,?)", (turma, nivelEns, turno, ano_letivo))
            return redirect(url_for("cadastrar"))
    return render_template("cadastrarTurma.html")

@app.route("/matricular_aluno", methods = ["GET", "POST"])
def matricular_aluno():
    id_aluno = request.args.get("id_aluno") or request.form.get("id_aluno")
    with conectar_banco() as conexao:
        turmas = conexao.execute("SELECT id, nome_turma FROM turmas ORDER BY nome_turma DESC").fetchall()
    if request.method == "POST":
        id_turma = request.form["turma"].strip()
        data_hoje = datetime.now().strftime("%d/%m/%Y")
        if not id_turma:
            return "Nome da turma necessário", 400
        with conectar_banco() as conexao:
            conexao.execute("INSERT INTO matriculas (id_turma,id_aluno, data_matricula) VALUES (?,?,?)", (id_turma,id_aluno,data_hoje))
            return redirect(url_for("inicio"))
    return render_template("matricula.html", turmas = turmas, id_aluno = id_aluno)

@app.route("/consultar")
def consultar():
    busca = request.args.get("busca","").strip()
    with conectar_banco() as conexao:
            if busca:
                dados_alunos = conexao.execute("""
                SELECT a.id, 
                       a.nome_completo, 
                       a.data_nascimento, 
                       t.nome_turma,
                       m.data_matricula 
                FROM alunos AS a 
                LEFT JOIN matriculas AS m
                    ON a.id = m.id_aluno
                LEFT JOIN turmas AS t
                    ON t.id = m.id_turma
                WHERE a.nome_completo LIKE ? OR t.nome_turma LIKE ? 
                ORDER BY a.id DESC""",(f"%{busca}%", f"%{busca}%")).fetchall()
            else:
                dados_alunos = conexao.execute("""
                SELECT  a.id, 
                        a.nome_completo, 
                        a.data_nascimento, 
                        t.nome_turma,
                        m.data_matricula 
                    FROM alunos AS a 
                    LEFT JOIN matriculas AS m
                    ON a.id = m.id_aluno
                    LEFT JOIN turmas AS t
                    ON t.id = m.id_turma
                    ORDER BY a.id DESC""").fetchall()
    return render_template("listagem.html", alunos = dados_alunos, busca = busca)

@app.route("/editar_aluno/<int:id_aluno>", methods = ["GET", "POST"])
def editar_aluno(id_aluno):
    with conectar_banco() as conexao:
        aluno = conexao.execute("SELECT * FROM alunos WHERE id = ?",(id_aluno,)).fetchone()
        if aluno is None:
            return "aluno não encontrado", 404
        if request.method == "POST":
            nome_completo = request.form["nome_completo"]
            nome_responsavel = request.form["nome_responsavel"]
            data_nascimento = request.form["data_nascimento"]
            cpf_aluno = request.form["cpf_aluno"]

            conexao.execute("""
            UPDATE alunos 
            SET nome_completo = ?,
                nome_responsavel = ?,
                data_nascimento = ?,
                cpf_aluno = ?
            WHERE id = ? 
            """, (nome_completo,nome_responsavel,data_nascimento,cpf_aluno,id_aluno))
            return redirect(url_for("inicio"))
    return render_template("editar.html", aluno = aluno)

@app.route("/excluir_aluno/<int:id_aluno>", methods = ["GET","POST"])
def excluir_aluno(id_aluno):
    with conectar_banco() as conexao:
        aluno = conexao.execute("SELECT * FROM alunos WHERE id = ?",(id_aluno,)).fetchone()
        if request.method == "POST":
            conexao.execute("DELETE FROM matriculas WHERE id_aluno = ?", (id_aluno,))
            conexao.execute("DELETE FROM alunos WHERE id = ?",(id_aluno,))
            return redirect(url_for("consultar"))
    return render_template("excluir.html", aluno = aluno)

if __name__ == "__main__":
    app.run(debug=True)