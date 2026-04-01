from typing import Union
import json


class ValidationService:
    def __init__(self, payload: dict = None, type: any = None):
        self.all_errors = json.loads(open("app/errors.json").read())
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
        self.payload = payload if not self.payload else self.payload
        self.type = type if not self.type else self.type
        if not self.payload:
            self.errors.append({"codigo_erro": 1000,
                                "descricao": self.all_errors.get("1000")})
            return [self.errors, False]
        if self.type:
            keys = self.type.__table__.columns.keys()
            if len(keys) > 0:
                for key in keys[1:]: # Removing the primary key from the loop 
                    if not key in ["criado_em", "atualizado_em"] and not self.payload.get(key):
                        self.errors.append({"codigo_erro": 1001,
                                            "descricao": f'{key} - {self.all_errors.get("1001")}'})
                    elif not key in ["criado_em", "atualizado_em"] and self.payload.get(key):
                        final_payload[key] = self.payload.get(key)
        if len(self.errors) == 0:
            return [final_payload, True]
        return [self.errors, False]
