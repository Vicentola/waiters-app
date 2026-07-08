from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Atendente(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    experiencia = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Float, default=0.0)
    disponivel = db.Column(db.Boolean, default=False)
    segmento = db.Column(db.String(100), nullable=False)
    
    def __repr__(self): #representa um obj como string
        return f"<Atendente {self.nome}>"
    
class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    segmento = db.Column(db.String(100), nullable=False)
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