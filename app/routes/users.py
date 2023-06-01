from ..main import db
from flask import Blueprint,jsonify,request
from ..models.userModel import User
users = Blueprint('users',__name__,url_prefix='/users')


@users.route('/login', methods=['POST'])
def login():
    body = request.json
    user_model = User(db)
    response = user_model.user_login(body)
    if 'error' in response:
        return jsonify(response), 400

    return jsonify(response)

#READ
@users.route('/users',methods=['GET'])
def get_users():
    user_model = User(db)
    response = user_model.get_all_users()
    if 'error' in response:
        return jsonify(response),400

    return jsonify(response)


# CREATE


@users.route('', methods=['POST'])
def add_user():
    body = request.json
    user_model = User(db)
    response = user_model.create(body)
    if 'error' in response:
        return jsonify(response),400
    return jsonify(response),201


# # UPDATE
#
#


@users.route('/<string:_id>',methods=["PUT"])
def update_user(_id):
    body =request.json
    user_model = User(db)
    response = user_model.user_update(body,_id)
    if 'error' in response:
        return jsonify(response), 400
    return jsonify(response)


#DELETE
@users.route('/<_id>',methods=["DELETE"])
def delete_user(_id):
    try:
        db.users.delete_one({"_id": ObjectId(_id)})
        return jsonify({"message": f"id:{_id} deleted from users list"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
