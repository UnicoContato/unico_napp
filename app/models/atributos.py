from app.extensions import db
from datetime import datetime

class Atributo(db.Model):
    __tablename__ = "atributos"

    id = db.Column("id_atributo", db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    nome = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)