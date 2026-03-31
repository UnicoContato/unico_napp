from app.extensions import db
from app.models.produto import Produto
from app.models.order import Order
from app.models.imagens import Imagem

def upsert_product(data):
    product = Produto.query.filter_by(sku=data.get("sku")).first()

    if not product:
        product = Produto(sku=data.get("sku"))
        db.session.add(product)

    product.name = data.get("name")
    product.status = data.get("status")
    product.brand = data.get("brand")
    product.description = data.get("description")

    return product

def process_products_bulk(payload):
    items = payload.get("products", [])
    processed = 0

    with db.session.begin():
        for item in items:
            product = upsert_product(item)

            Order.query.filter_by(product_id=product.id).delete()

            order = Order(
                product_id=product.id,
                seller_id=payload.get("seller_id"),
                price=item.get("price"),
                stock=item.get("stock")
            )
            db.session.add(order)

            Imagem.query.filter_by(product_id=product.id).delete()

            for img in item.get("images", []):
                db.session.add(Imagem(
                    product_id=product.id,
                    url=img.get("url"),
                    position=img.get("position")
                ))

            processed += 1

    return {"processed": processed}
