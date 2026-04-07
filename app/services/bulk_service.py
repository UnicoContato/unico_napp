from app.models.produto_valor_atributo import ProdutoValorAtributo
from app.services.validation_service import ValidationService
from app.models.valores_atributos import ValoresAtributos
from app.models.atributos import Atributo
from app.models.produto import Produto
from app.models.imagens import Imagem
from app.models.order import Order
from app.extensions import db


class BulkService:
    def __init__(self):
        self.validation = ValidationService()

    def ingest(self, payload: dict) -> list:
        # try:
            report = {
                "products": {"inserted": 0, "existing": 0},
                "images": {"inserted": 0, "existing": 0},
                "orders": {"inserted": 0, "existing": 0},
                "attributes": {"inserted": 0, "existing": 0}
            }
            items = payload.get("itens", list())
            if not items:
                self.validation.errors.append({"codigo_erro": 1001,
                                                "descricao": f'itens - {self.validation.all_errors.get("1001")}'})
                return [self.validation.errors, False]

            for item in items:
                # Validating the product object and then inserting in the database
                out_product, validation_ok = self.validation.validate_payload(item, Produto)
                if validation_ok is False:
                    continue

                product_search = Produto.query.filter_by(sku=out_product["sku"]).first()
                if not product_search:
                    product_search = Produto(**out_product)
                    db.session.add(product_search)
                    db.session.flush()
                    report["products"]["inserted"] += 1
                else:
                    report["products"]["existing"] += 1

                # Handle images for this product
                if item.get("imagens"):
                    for image_data in item["imagens"]:
                        # Map legacy field names for backward compatibility
                        mapped_image_data = image_data.copy()
                        if "url" in mapped_image_data:
                            mapped_image_data["link"] = mapped_image_data.pop("url")
                        if "posicao" in mapped_image_data:
                            mapped_image_data["ordem"] = mapped_image_data.pop("posicao")

                        # Set the product ID for the image
                        mapped_image_data["id_produto"] = product_search.id

                        # Check if image already exists (by link and product_id)
                        image_search = Imagem.query.filter_by(
                            id_produto=product_search.id,
                            link=mapped_image_data.get("link")
                        ).first()

                        if not image_search:
                            # Create image directly without validation for simplicity
                            try:
                                image_obj = Imagem(**mapped_image_data)
                                db.session.add(image_obj)
                                db.session.flush()
                                report["images"]["inserted"] += 1
                            except Exception as e:
                                print(f"Error creating image: {e}")
                                continue
                        else:
                            report["images"]["existing"] += 1

                # Handle orders for this product
                if item.get("orders"):
                    for order_data in item["orders"]:
                        # Add product ID before validation since it's required
                        order_data_with_product = order_data.copy()
                        order_data_with_product["id_produto"] = product_search.id

                        # Support alternate seller ID keys for bulk payloads
                        if "id_seller_contato" not in order_data_with_product:
                            if "seller_id" in order_data_with_product:
                                order_data_with_product["id_seller_contato"] = order_data_with_product.pop("seller_id")
                            elif "id_seller" in order_data_with_product:
                                order_data_with_product["id_seller_contato"] = order_data_with_product.pop("id_seller")

                        # Validate order payload
                        out_order, validation_ok = self.validation.validate_payload(order_data_with_product, Order)
                        if validation_ok is False:
                            continue

                        seller_id = out_order.get("id_seller_contato")
                        if seller_id is None:
                            continue

                        # Check if order already exists (by seller and product combination)
                        order_search = Order.query.filter_by(
                            id_seller_contato=seller_id,
                            id_produto=product_search.id
                        ).first()

                        if not order_search:
                            order_obj = Order(**out_order)
                            db.session.add(order_obj)
                            db.session.flush()
                            report["orders"]["inserted"] += 1
                        else:
                            report["orders"]["existing"] += 1
                if item.get("atributos"):
                    attributes_keys = {key: None for key in list(item["atributos"].keys())}
                    for attribute_key in attributes_keys:
                        if item["atributos"].get(attribute_key):

                            attribute = Atributo.query.filter_by(nome=attribute_key).first()
                            if not attribute:
                                attribute_insert = {"nome": attribute_key,
                                "tipo": str(type(item["atributos"].get(attribute_key)))}
                                attribute = Atributo(**attribute_insert)
                                db.session.add(attribute)
                                db.session.flush()

                            attribute_value = ValoresAtributos.query.filter_by(valor=item["atributos"].get(attribute_key)).first()
                            if not attribute_value:
                                attribute_value_insert = {"valor": item["atributos"].get(attribute_key)}
                                attribute_value = ValoresAtributos(**attribute_value_insert)
                                db.session.add(attribute_value)
                                db.session.flush()

                            attribute_value_product = ProdutoValorAtributo.query.filter_by(
                                                                        id_produto=product_search.id,
                                                                        id_atributo=attribute.id,
                                                                        id_valor_atributo=attribute_value.id).first()
                            if not attribute_value_product:
                                attribute_value_product_insert = {"id_produto": product_search.id,
                                                                "id_atributo": attribute.id,
                                                                "id_valor_atributo": attribute_value.id}
                                attribute_value_product = ProdutoValorAtributo(**attribute_value_product_insert)
                                db.session.add(attribute_value_product)
                                db.session.flush()
                                report["attributes"]["inserted"] += 1
                            else:
                                report["attributes"]["existing"] += 1
            if len(self.validation.errors) == 0:
                db.session.commit()
                return [report, True]
            return [self.validation.errors, False]
        # except Exception as e:
        #     db.session.rollback()
        #     print(f"Error processing bulk payload: {e}")
        #     if len(self.validation.errors) == 0:
        #         return [{"codigo_erro": 1000, "descricao": "Erro interno ao processar o payload"}], False
        #     return [self.validation.errors, False]