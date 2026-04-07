from typing import Union
import json
import os


class ValidationService:
    def __init__(self, payload: dict = None, type: any = None):
        errors_path = os.path.join(os.path.dirname(__file__), "..", "errors.json")
        self.all_errors = json.loads(open(errors_path).read())
        self.payload = payload
        self.type = type
        self.errors = list()
    
    def validate_payload(self, payload: dict = None, type: any = None) -> Union[dict, bool]:
        """
            Method used to validate the input from 
            each payload and compare with the respectative
            DB model
        """
        final_payload = dict()
        self.errors = []
        self.payload = payload if payload is not None else self.payload
        self.type = type if type is not None else self.type
        if not self.payload:
            self.errors.append({"codigo_erro": 1000,
                                "descricao": self.all_errors.get("1000")})
            return [self.errors, False]
        if self.type:
            keys = self.type.__table__.columns.keys()
            if len(keys) > 0:
                for key in keys[1:]: # Removing the primary key from the loop 
                    if key in ["criado_em", "atualizado_em"]:
                        continue

                    value = self.payload.get(key)
                    if value is None or value == "":
                        self.errors.append({"codigo_erro": 1001,
                                            "descricao": f'{key} - {self.all_errors.get("1001")}'})
                    else:
                        final_payload[key] = value
        if len(self.errors) == 0:
            return [final_payload, True]
        return [self.errors, False]
