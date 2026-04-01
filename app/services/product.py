from services.validation_service import ValidationService
from app.models.atributos import Atributo
from app.models.produto import Produto
from app.models.imagens import Imagem
from app.models.order import Order
from app.extensions import db


class ProductService:
    def __init__(self):
        self.validation = ValidationService()
    
    def ingest(self, payload: dict) -> None:
        items = payload.get("items", list())
        if not items:
            self.validation.errors.append({"codigo_erro": 1001,
                                            "descricao": f'items - {self.all_errors.get("1001")}'})
            return [self.validation, False]

        for item in items:
            out_product = self.validation.validate_payload(item, Produto)
            if item.get("imagens"):
                out_image = self.validation.validate_payload(item.get("imagens"), Imagem)
            if item.get("order"):
                out_order = self.validation.validate_payload(item.get("order"), Order)
            if item.get("atributos"):
                attributes_keys = {key: None for key in list(item["atributos"].keys())}
                for attribute_key in attributes_keys:
                    attribute = Atributo.query.filter_by(nome=attribute_key).first()
                    


