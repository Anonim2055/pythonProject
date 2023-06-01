from flask import Blueprint,jsonify,request

main = Blueprint('main',__name__,url_prefix='')

@main.route('/',methods=['GET'])
def index():
    resp = jsonify({
        "message":"Flask Server Run"
    })
    return resp