from app.extensions import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column("id_produto", db.Integer, primary_key=True)
    ean = db.Column(db.String(20))
    sku = db.Column(db.String(50), index=True)
    nome = db.Column(db.String(255))
    marca = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    status = db.Column(db.String(50))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)