from flask import Blueprint,jsonify,request,render_template
from ..middleware.authorization import login_required
main = Blueprint('main',__name__,url_prefix='')

@main.route('/',methods=['GET'])
def index():

    message="Flask Server Run"
    users = [
        {
            "name": "User1 Name",
            "email": "user1@example.com",
            "password": "user1password"
        },
        {
            "name": "User2 Name",
            "email": "user2@example.com",
            "password": "user2password"
        }
    ]
    return render_template('index.html',message=message,users=users)


@main.route('/protected',methods=['GET'])
@login_required
def protected_route():
    return render_template('protected.html')

