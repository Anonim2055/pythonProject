from marshmallow import ValidationError
from flask import session
from ..schemas.productSchema import ProductSchema
class Product:
    def __init__(self,db):
        self.db = db.products
        self.productValid = ProductSchema()

    def create(self, data):
        print(data)
        try:
            validate_data = self.productValid.load(data)
            print(validate_data)
            try:
                result = self.db.insert_one({
                    "name": validate_data["name"],
                    "description": validate_data.get("description"),  # description is not required
                    "category": validate_data["category"],
                    "price": validate_data["price"],
                    "img_url": validate_data["img_url"],
                    "user_id":session.get('_id')
                })
                print(result)
                return True
            except Exception as e:
                print(e)  # Print the error message
                return {"error": "Failed to create product."}
        except ValidationError as err:
            if err.messages:
                error_messages = {}
                for field, errors in err.messages.items():
                    error_messages[field] = errors[0]
                return {"error": error_messages}



    def get_user_product(self):
        return self.db.find({"user_id":session.get('_id')})