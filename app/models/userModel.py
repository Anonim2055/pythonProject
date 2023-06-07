from ..schemas.userSchema import UserSchema,LoginSchema,UserUpdateSchema
from bcrypt import hashpw,gensalt,checkpw
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError
from flask_jwt_extended import create_access_token
from flask import session
from datetime import timedelta
from bson.objectid import ObjectId
from bson.errors import InvalidId

class User:
    def __init__(self,db):
        self.db = db.users
        self.userValid = UserSchema()
        self.loginValid = LoginSchema()
        self.userUpdateValid = UserUpdateSchema()


    def create(self,data):
        try:
            validate_data = self.userValid.load(data)
            print(validate_data)
            password = validate_data["password"].encode('utf-8')  # convert password to bytes
            hashed_password = hashpw(password, gensalt())  # hash the password
            try:
                result = self.db.insert_one({
                    "email": validate_data["email"],
                    "name": validate_data["name"],
                    "role": "user",
                    "password": hashed_password.decode('utf-8')  # store hashed password as string
                })
                return True
            except DuplicateKeyError:
                return {"error":{"unique": "This email is already registered."}}
        except ValidationError as err:
            if err.messages:
                error_messages = {}
                for field, errors in err.messages.items():
                    error_messages[field] = errors[0]
                return {"error": error_messages}

    def get_all_users(self):
        count = self.db.count_documents({})
        if count:
            users = self.db.find({})
            user_list = [{
                "id": str(user['_id']),
                "email": user["email"],
                "password": user["password"],
                "name": user["name"]
            } for user in users]
            return user_list
        return {'error':'No users found'}

    def user_login(self,data):
        try:
            validate_data = self.loginValid.load(data)
            user = self.db.find_one({'email': validate_data['email']})
            # if email exist in DB
            if user is None:
                return "Invalid email or password"

            checkPassword = checkpw(validate_data['password'].encode('utf-8'), user['password'].encode('utf-8'))

            # if password is matched to DB return token
            if user and checkPassword:
                session['_id'] =str(user['_id'])
                session['role'] = user['role']
                return True
            else:
                return "Invalid email or password"
        except ValidationError as err:
            return 'email or password invalid'


    def user_update(self,data,_id):
        validate_data = self.userUpdateValid.load(data)
        try:
            try:
                user = self.db.find_one({"_id": ObjectId(_id)})
            except InvalidId:
                return {"error": "Invalid ObjectId format"}
            if user is None:
                return {"error": "User not found"}

            if 'password' in validate_data:
                password = validate_data["password"].encode('utf-8')  # convert password to bytes
                hashed_password = hashpw(password, gensalt())  # hash the password
                validate_data['password'] = hashed_password.decode('utf-8')

            try:
                result = self.db.update_one({"_id": ObjectId(_id)}, {"$set": validate_data})
                if result.matched_count == 0:
                    return {"error": "No user with the given id found"}
                else:
                    return {"message": f"User {_id} updated successfully"}
            except Exception as e:
                return {"error": str(e)}
        except ValidationError as err:
            return {'error': err.messages}
