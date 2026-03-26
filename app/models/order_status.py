from app.extensions import db
from datetime import datetime

class OrderStatus(db.Model):
    __tablename__ = "order_status"

    id = db.Column("id_order_status", db.Integer, primary_key=True)
    id_order = db.Column(
        db.Integer, db.ForeignKey("order.id_order"), nullable=False
    )
    quantidade = db.Column(db.Integer)
    status = db.Column(db.String(50))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)