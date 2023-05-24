from flask import Flask,jsonify,request
from pymongo import MongoClient
from bcrypt import hashpw,gensalt


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

#
# @app.route('/users',methods=['GET'])
# def get_users():
#     resp = jsonify({
#        "users_list":users_list
#     })
#     return resp
#
#
# # CREATE
#
#
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
# @app.route('/users/<int:_id>',methods=["PUT"])
# def update_user(_id):
#     body =request.json
#     valid_keys = {"name", "email","password"}
#     # check if there's any invalid key in the request body
#     if any(key not in valid_keys for key in body.keys()):
#         return jsonify({"error": "Invalid field in request body"}), 400  # return error message with 400 status code
#
#
#     return jsonify({
#         "message":"user not found"
#     })
#
# #DELETE
# @app.route('/users/<int:_id>',methods=["DELETE"])
# def delete_user(_id):
#     global users_list
#     flag = False
#     for user in users_list:
#         if user['id'] == _id:
#             flag = True
#     if flag == False:
#         return jsonify({
#         "message": f"user not found"
#     })
#     users_list = [user for user in users_list if user['id'] != _id]
#
#     resp = jsonify({
#         "message": f"id:{_id} deleted from users list"
#     })
#     return resp

if __name__ == "__main__":
    app.run(debug=True,port=3000)