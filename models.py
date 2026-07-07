from flask_sqlalchemy import SQLAlchemy

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