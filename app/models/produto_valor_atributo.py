from app.extensions import db

class ProdutoValorAtributo(db.Model):
    __tablename__ = "produtos_valores_atributos"

    id = db.Column("id_produto_valor_atributo", db.Integer, primary_key=True)
    id_produto = db.Column(
        db.Integer, db.ForeignKey("produto.id_produto"), nullable=False
    )
    id_atributo = db.Column(
        db.Integer, db.ForeignKey("atributos.id_atributo"), nullable=False
    )
    id_valor_atributo = db.Column(
        db.Integer, db.ForeignKey("valores_atributos.id_valor_atributo"), nullable=False
    )