from app.extensions import db
from datetime import datetime

class Seller(db.Model):
    __tablename__ = "seller"

    id = db.Column("id_seller_contato", db.Integer, primary_key=True)
    cnpj = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)