from app.extensions import db
from datetime import datetime

class Imagem(db.Model):
    __tablename__ = "imagens"

    id = db.Column("id_imagem", db.Integer, primary_key=True)
    id_produto = db.Column(
        db.Integer, db.ForeignKey("produto.id_produto"), nullable=False
    )
    link = db.Column(db.Text)
    ordem = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, onupdate=datetime.utcnow)