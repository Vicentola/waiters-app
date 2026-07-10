from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Atendente, Empresa, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waiters.db"
app.config["SECRET_KEY"] = "waiters_secret_key"
db.init_app(app)

login_manager=LoginManager()
login_manager.init_app(app) # init_app é usado para inicializar a extensão com a aplicação Flask
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

    
@app.route("/atendentes")
@login_required
def listar_atendentes():
    atendentes = Atendente.query.all() #query all() retorna todos os registros da tabela Atendente
    return render_template("atendentes.html", atendentes=atendentes) # retorna a lista de atendentes para o template atendentes.html

@app.route("/cadastro/atendente")
@login_required
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

@app.route("/atendente/perfil/<int:id>")
@login_required
def perfil_atendente(id):
    atendente = db.session.get(Atendente, id)
    if atendente:
        return render_template("perfil_atendente.html", atendente=atendente)
    return redirect("/atendentes")

@app.route("/empresas")
@login_required
def listar_empresas():
    empresas = Empresa.query.all()
    return render_template("empresas.html", empresas=empresas)

@app.route("/cadastro/empresa")
@login_required
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

@app.route("/registro")
def registro():
    return render_template("registro.html")


@app.route("/registrar", methods=["POST"])
def registrar():
    email = request.form["email"]
    senha = request.form["senha"]
    tipo = request.form["tipo"]
    
    senha_hash = generate_password_hash(senha)
    usuario = Usuario(email=email, senha=senha_hash, tipo=tipo)
    db.session.add(usuario)
    db.session.commit()
    return redirect("/login")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logar", methods =["POST"])
def logar():
    email = request.form["email"]
    senha = request.form["senha"]
    
    usuario = Usuario.query.filter_by(email=email).first()
    #como se fosse uma consulta sql, o first retorna o primeiro resultado ou None
    #o if checa isso, se achou o user ou n
    if usuario and check_password_hash(usuario.senha, senha):
        login_user(usuario)
        return redirect("/")
    return "Email ou senha incorretos."

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")
    
      



if __name__ == "__main__":
    app.run(debug=True)


