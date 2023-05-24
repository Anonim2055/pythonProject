from bson.errors import InvalidId
from flask import Flask,jsonify,request
from pymongo import MongoClient
from bcrypt import hashpw,gensalt
from bson.objectid import ObjectId


app = Flask(__name__)

try:
    mongo = MongoClient(host="localhost",port=27018,serverSelectionTimeoutMS=5000)
    db = mongo.flask

    print("MongoDB Connect")
except Exception:
    print("Unable to connect MongoDB")


@app.route('/',methods=['GET'])
def index():
    resp = jsonify({
        "message":"Flask Server Run"
    })
    return resp



#READ


@app.route('/users',methods=['GET'])
def get_users():
    users = db.users.find({})
    user_list = [{
        "id": str(user['_id']),
        "email": user["email"],
        "password": user["password"],
        "name": user["name"]
    } for user in users]
    return jsonify(user_list)


# CREATE


@app.route('/users',methods=['POST'])
def add_user():
    body = request.json
    required_keys = {"name", "email","password"}
    # check if there's any invalid key in the request body
    if set(body.keys()) != required_keys:
        return jsonify({"error": "Invalid or missing field in request body"}), 400
        # return error message with 400 status code

    password = body["password"].encode('utf-8')  # convert password to bytes
    hashed_password = hashpw(password,gensalt())  # hash the password

    result = db.users.insert_one({
        "email":body["email"],
        "name":body["name"],
        "password":hashed_password.decode('utf-8')  # store hashed password as string
    })

    resp = jsonify({
        "id":str(result.inserted_id),
        "message":"user added"
    })
    return resp
#
# # UPDATE
#
#

from bson.objectid import ObjectId

@app.route('/users/<string:_id>',methods=["PUT"])
def update_user(_id):
    body =request.json
    valid_keys = {"name", "email","password"}



    try:
        user = db.users.find_one({"_id": ObjectId(_id)})
    except InvalidId:
        return jsonify({"error": "Invalid ObjectId format"}), 400
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # check if there's any invalid key in the request body
    if any(key not in valid_keys for key in body.keys()):
        return jsonify({"error": "Invalid field in request body"}), 400

    if 'password' in body:
        password = body["password"].encode('utf-8')  # convert password to bytes
        hashed_password = hashpw(password, gensalt())  # hash the password
        body['password'] = hashed_password.decode('utf-8')

    try:

        result = db.users.update_one({"_id": ObjectId(_id)}, {"$set": body})
        if result.matched_count == 0:
            return jsonify({"error": "No user with the given id found"}), 404
        else:
            return jsonify({"message": f"User {_id} updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400




#DELETE
@app.route('/users/<_id>',methods=["DELETE"])
def delete_user(_id):
    try:
        db.users.delete_one({"_id": ObjectId(_id)})
        return jsonify({"message": f"id:{_id} deleted from users list"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True,port=3000)