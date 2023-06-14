from marshmallow import ValidationError
from flask import session
from ..schemas.productSchema import ProductSchema
from bson.objectid import ObjectId

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
        return list(self.db.find({"user_id":session.get('_id')}))




    def delete_product_by_id(self, _id):
        try:
            result = self.db.delete_one({"_id": ObjectId(_id)})

            if result.deleted_count > 0:
                return True
            else:
                return {"error":"Unable to delete the product."}

        except Exception as e:
            print("Error: ", e)
            return {"error":"An error occurred."}

    def get_product_by_id(self, _id):
        try:
            product = self.db.find_one({"_id": ObjectId(_id)})

            if product is not None:
                return product
            else:
                return {"error": "Product not found."}

        except Exception as e:
            print("Error: ", e)
            return {"error": "An error occurred while retrieving the product."}


    def update_by_id(self, data, _id):
        try:
            validate_data = self.productValid.load(data)
            try:
                result = self.db.update_one(
                    {"_id": ObjectId(_id)},
                    {"$set": {
                        "name": validate_data["name"],
                        "description": validate_data.get("description"),  # description is not required
                        "category": validate_data["category"],
                        "price": validate_data["price"],
                        "img_url": validate_data["img_url"],
                    }}
                )

                if result.modified_count > 0:
                    return True
                else:
                    return {"error": "Failed to update the product."}

            except Exception as e:
                print(e)  # Print the error message
                return {"error": "An error occurred while updating the product."}
        except ValidationError as err:
            if err.messages:
                error_messages = {}
                for field, errors in err.messages.items():
                    error_messages[field] = errors[0]
                return {"error_validate": error_messages}

