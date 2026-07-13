from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Atendente(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    experiencia = db.Column(db.Integer, default=0)  # anos de experiência
    nota = db.Column(db.Float, default=0.0)
    disponivel = db.Column(db.Boolean, default=False)
    segmento = db.Column(db.String(100))
    
    def __repr__(self): #representa um obj como string
        return f"<Atendente {self.nome}>"
    
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    segmento = db.Column(db.String(100))
    nota = db.Column(db.Float, default=0.0)
    
    def __repr__(self):
        return f"<Empresa {self.nome}>"
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'empresa' ou 'atendente'
    """
    userMixin é uma classe que fornece implementações 
    padrão para os métodos que Flask-Login espera que 
    um objeto de usuário tenha. Isso inclui métodos 
    como is_authenticated, is_active, 
    is_anonymous e get_id. Ao herdar de UserMixin, 
    a classe usuarios automaticamente obtém essas implementações, 
    facilitando a integração com o sistema de login do Flask-Login.
    """
    def __repr__(self):
        return f"<Usuario {self.email}>"
    
    
class Vaga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500))
    data_evento = db.Column(db.String(20), nullable=False)
    taxa = db.Column(db.Float, nullable=False)
    segmento = db.Column(db.String(100))
    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=False)

    def __repr__(self):
        return f"<Vaga {self.titulo}>"
    
    
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remetente_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    destinatario_id=db.Column(db.Integer,db.ForeignKey("usuario.id"), nullable=False)
    conteudo = db.Column(db.String(1000), nullable=False)
    data_envio = db.Column(db.DateTime, default=db.func.now())
    
    def __repr__(self):
        return f"<Mensagem de {self.remetente_id} para {self.destinatario_id}>"