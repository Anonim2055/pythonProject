from ..main import db
from flask import Blueprint,jsonify,request,render_template,redirect,url_for,session
from ..models.userModel import User
users = Blueprint('users',__name__,url_prefix='/users')
from bson.objectid import ObjectId
from flask_jwt_extended import get_jwt_identity

@users.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        body = request.form
        user_model = User(db)
        response = user_model.user_login(body)
        print(response)
        if response is True:
            return redirect(url_for('main.index'))
        else:
            error = response
            return render_template('login.html',error=error)
    return render_template('login.html')


#READ
@users.route('',methods=['GET'])
def get_users():
    user_model = User(db)
    response = user_model.get_all_users()
    if 'error' in response:
        return jsonify(response),400

    return jsonify(response)


# CREATE


@users.route('/register', methods=['POST','GET'])
def add_user():
    if request.method == 'POST':
        body = request.form
        user_model = User(db)
        response = user_model.create(body)
        if response is True:
            return redirect(url_for('users.login'))

        if 'error' in response:
            error =response['error']
            return render_template('register.html',error=error)
        if 'error' in response:
            error = response['error']
            return render_template('register.html', error=error)

    return render_template('register.html')


# # UPDATE
#
#


@users.route('',methods=["PUT"])
def update_user():
    _id = get_jwt_identity()['_id']
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


@users.route('/logout')
def logout():
    session.pop('_id', None)
    session.pop('role', None)
    return redirect(url_for('users.login'))
