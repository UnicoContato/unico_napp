from app.extensions import db
from datetime import datetime

class ValoresAtributos(db.Model):
    __tablename__ = "valores_atributos"

    id = db.Column("id_valor_atributo", db.Integer, primary_key=True)
    valor = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)