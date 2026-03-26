from app.extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "order"

    id = db.Column("id_order", db.Integer, primary_key=True)
    id_seller_contato = db.Column(
        db.Integer, db.ForeignKey("seller.id_seller_contato"), nullable=False
    )
    id_produto = db.Column(
        db.Integer, db.ForeignKey("produto.id_produto"), nullable=False
    )
    estoque = db.Column(db.Integer)
    preco = db.Column(db.Numeric(10, 2))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)