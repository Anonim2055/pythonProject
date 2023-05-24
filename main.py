from flask import Flask,jsonify,request
_id =2
users_list = [
    {
        "id":1,
        "name":"yarin",
        "email":"byarin90@gmail.com"
    },
    {
        "id":2,
        "name":"david",
        "email":"david@gmail.com"
    }
]

app = Flask(__name__)

# READ


@app.route('/',methods=['GET'])
def index():
    resp = jsonify({
        "message":"Flask Server Run"
    })
    return resp



#READ


@app.route('/users',methods=['GET'])
def get_users():
    resp = jsonify({
       "users_list":users_list
    })
    return resp


# CREATE


@app.route('/users',methods=['POST'])
def add_user():
    body = request.json
    required_keys = {"name", "email"}
    # check if there's any invalid key in the request body
    if set(body.keys()) != required_keys:
        return jsonify({"error": "Invalid or missing field in request body"}), 400
        # return error message with 400 status code


    _name = body['name']
    _email = body['email']
    body['id'] = _id + 1
    users_list.append(body)
    print(body)
    resp = jsonify({
        "message":"user added"
    })
    return resp

# UPDATE


@app.route('/users/<int:_id>',methods=["PUT"])
def update_user(_id):
    body =request.json
    valid_keys = {"name", "email"}
    # check if there's any invalid key in the request body
    if any(key not in valid_keys for key in body.keys()):
        return jsonify({"error": "Invalid field in request body"}), 400  # return error message with 400 status code

    for user in users_list:
        if user['id'] == _id:
            user.update(body)
            return jsonify({
                "message": f"user with id:{_id} updated"
            })
    return jsonify({
        "message":"user not found"
    })

#DELETE
@app.route('/users/<int:_id>',methods=["DELETE"])
def delete_user(_id):
    global users_list
    flag = False
    for user in users_list:
        if user['id'] == _id:
            flag = True
    if flag == False:
        return jsonify({
        "message": f"user not found"
    })
    users_list = [user for user in users_list if user['id'] != _id]

    resp = jsonify({
        "message": f"id:{_id} deleted from users list"
    })
    return resp

if __name__ == "__main__":
    app.run(debug=True,port=3000)