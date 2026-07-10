from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Atendente, Empresa, Usuario, Vaga
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
    
    
    if tipo == "atendente":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        novo = Atendente(usuario_id=usuario.id, nome=nome, cpf=cpf)
        db.session.add(novo)
        db.session.commit()
        return redirect("/atendentes")
    
    else:
        nome_empresa = request.form["nome_empresa"]
        cnpj = request.form["cnpj"]
        nova = Empresa(usuario_id=usuario.id, nome=nome_empresa, cnpj=cnpj)
        db.session.add(nova)
        db.session.commit()
        return redirect("/empresas")

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

@app.route("/perfil/editar")
@login_required
def perfil_editar():
    return render_template("perfil_editar.html")

@app.route("/perfil/salvar", methods=["POST"])
@login_required
def perfil_salvar():
    segmento = request.form["segmento"]
    experiencia = request.form["experiencia"]
    
    atendente = Atendente.query.filter_by(usuario_id=current_user.id).first()
    if atendente:
        atendente.segmento = segmento
        atendente.experiencia = experiencia
        db.session.commit()
    return redirect("/atendentes")



@app.route("/perfil/empresa/editar")
@login_required
def perfil_empresa_editar():
    return render_template("perfil_empresa_editar.html")

@app.route("/perfil/empresa/salvar", methods=["POST"])
@login_required
def perfil_empresa_salvar():
    segmento = request.form["segmento"]
    
    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()
    if empresa:
        empresa.segmento = segmento
        db.session.commit()
    return redirect("/empresas")

@app.route("/vagas")
@login_required
def listar_vagas():
    vagas = Vaga.query.all()
    return render_template("vagas.html", vagas=vagas)

@app.route("/vaga/nova")
@login_required
def vaga_nova():
    return render_template("vaga_nova.html")

@app.route("/vaga/criar", methods=["POST"])
@login_required
def vaga_criar():
    titulo = request.form["titulo"]
    descricao = request.form["descricao"]
    data_evento = request.form["data_evento"]
    taxa = request.form["taxa"]
    segmento = request.form["segmento"]
    
    empresa = Empresa.query.filter_by(usuario_id=current_user.id).first()
    if empresa:
        nova = Vaga(titulo=titulo, descricao=descricao, data_evento=data_evento, taxa=taxa, segmento=segmento, empresa_id=empresa.id)
        db.session.add(nova)
        db.session.commit()
    return redirect("/vagas")

from models import db, Atendente, Empresa, Usuario, Vaga





@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")



    
      



if __name__ == "__main__":
    app.run(debug=True)


