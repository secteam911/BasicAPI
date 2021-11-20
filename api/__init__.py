from base64 import b64decode
from flask import jsonify, request, Blueprint, session
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from functools import wraps
from datetime import datetime, timedelta
from config import config
import jwt
from models import db
from models import User , Message

from sqlalchemy import exc


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = (request.headers['x-access-tokens']).encode("UTF-8")
        if not token:
            return jsonify({"Error": "Unauthorized"}), 401
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithm='HS256')

            this_user = User.query.filter_by(id=data['user_id']).first()
            
            if this_user.id == data['user_id'] :
                return f(*args, **kwargs)
            else:
                return jsonify({"Error":"Unauthorized"}), 401

        except BaseException:
            return jsonify({"Error": "Unauthorized"}), 401

    return decorator



api = Blueprint('api', __name__, url_prefix="/v1")


# API routes
@api.route('/api-token-auth', methods=['POST'])
def token_auth():
    # takes two arguments a username and a password as a json
    """
    {
        "username": "string",
        "password": "string"
    }
    """

    if not request.json:
        return jsonify({"Error": "No json provided"}), 400

    if request.method == 'POST':

        tmp_user = User.query.filter_by(
            username=request.json['username']).first()
        if not tmp_user:
            return jsonify({"Error": "No such user"}), 404

        # validate user and check provided password
        if check_password_hash(tmp_user.pass_hash, request.json['password']):
            # the user name and password provided are valid
            # generate token

            token = jwt.encode({'user_id': tmp_user.id,
                                'exp': datetime.utcnow() + timedelta(hours=1)},
                               current_app.config['SECRET_KEY'],
                               algorithm='HS256')

            return jsonify(
                {"Error": "Success", "token": token.decode('UTF-8')}), 200
        else:
            return jsonify({"Error": "Forbidden wrong password "}), 403

    else:
        return jsonify({"Error": "Wrong request method"}), 400






# this endpoint will add a user to the data base if request method is post
# or it will return user info if the request method is get 
@api.route('/user', methods=['GET', 'POST'])
# @token_required
def users():

    all_users = User.query.all()

    # if get then we return the users
    if request.method == "GET":
        users_lst= [] 

        for user in all_users:
            # username, first_name, last_name, last_login, is_active
            sub_lst = [user.id, 
                       user.username,
                       user.last_login]
            users_lst.append(sub_lst)


        return jsonify({"Error": "Returned User list", "Users_list":users_lst}), 200

    # create new user if json data found
    elif request.method == "POST":
        # sample data for valid POST request
        """
                {
                "username": "hello",
                "password": "12345678"

                }
        """
        if not request.json:
            return jsonify({"Error": "No JSON"}), 401
        json_data = request.json
        for item in json_data:
            if json_data[item] == "":
                return jsonify({"Error": "Can't have empty values"}), 401
        try:
            new_user = User(
                username=json_data['username'],
                pass_hash=generate_password_hash(
                    json_data['password'],
                    "sha256"),
                last_login=datetime.now()
                )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"Error":"Successfully add user to database"}),200

        except exc.IntegrityError:
            db.session.rollback()
            return jsonify({"Error": "Such username is already registered."})

        return jsonify({"Error": "Added New User.", "UserID":f"{new_user.id}"}), 200



@api.route('/message',  methods=['POST'])
@token_required
def message():


    if request.method == "POST":
        # check for JSON data 
        if not request.json:
            return jsonify({"Error": "No JSON"}), 401

        if request.json['message'] == '':
            return jsonify({"Error":"Message can't be empty"}),401

        usr = User.query.filter_by(username=request.json['username']).first()

        new_message =  Message(text=request.json['message'], user_id=usr.id)
       
        try:
            db.session.add(new_message)
            db.session.commit()
            return jsonify({"Error":"Add new message"}),200
        except exc.IntegrityError:
            return jsonify({"Error":"Failed to add new message "}),500

        

    else:
        return jsonify({"Error":"Wrong request method"}),400



@api.route('/history')
@token_required
def history():


    if request.method == "GET":
        # check for JSON data 
        if not request.json:
            return jsonify({"Error": "No JSON"}), 401

        if request.json['message'] == '':
            return jsonify({"Error":"Message can't be empty"}),401

        usr = User.query.filter_by(username=request.json['username']).first()

        n = int(str(request.json['message']).split()[1])

        

        all_messages =  Message.query.filter_by(user_id=usr.id).all()
        

        message_lst = [] 
        for i,item in enumerate(all_messages):
            if i >= n :
                break

            message_lst.append(item.text)

        return jsonify({"Error":"","UserMessages":f"{message_lst}"}),200

    else:
        return jsonify({"Error":"Wrong request method"}),400


