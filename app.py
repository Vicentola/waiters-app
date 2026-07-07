from flask import Flask, render_template, request, redirect
from models import db, Atendente, Empresa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waiters.db"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

    
@app.route("/atendentes")
def listar_atendentes():
    atendentes = Atendente.query.all() #query all() retorna todos os registros da tabela Atendente
    return render_template("atendentes.html", atendentes=atendentes) # retorna a lista de atendentes para o template atendentes.html

@app.route("/cadastro/atendente")
def cadastro_atendente():
    return render_template("cadastro_atendente.html")

@app.route("/cadastrar/atendente", methods=["POST"])
def cadastrar_atendente():
    nome = request.form["nome"]
    experiencia = request.form["experiencia"]
    segmento = request.form["segmento"]
    novo = Atendente(nome=nome, experiencia=experiencia, nota=0.0, segmento=segmento)
    db.session.add(novo)
    db.session.commit()
    return redirect("/atendentes")

@app.route("/empresas")
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template("empresas.html", empresas=empresas)

@app.route("/cadastro/empresa")
def cadastro_empresa():
    return render_template("cadastro_empresa.html")

@app.route("/cadastrar/empresa", methods=["POST"])
def cadastrar_empresa():
    nome = request.form["nome"]
    segmento = request.form["segmento"]
    nova = Empresa(nome=nome, segmento=segmento, nota=0.0)
    db.session.add(nova)
    db.session.commit()
    return redirect("/empresas")

if __name__ == "__main__":
    app.run(debug=True)


