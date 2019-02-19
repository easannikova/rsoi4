import psycopg2
import flask 
from flask import jsonify
from flask import request
import json
from flask_cors import CORS
import math
import hashlib
import datetime
import jwt

app = flask.Flask(__name__)
CORS(app)
# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def db_conn():
    con = None
    con = psycopg2.connect(database = 'usersDB', user = 'sea')
    print(con)
    return con


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def movie_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/login')

# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})

@app.route('/api/1.0/login', methods=['POST'])
def check_login():
    with db_conn() as db:
        cur = db.cursor()
        login = request.json['login']
        password = request.json['password']
        password = hashlib.sha256(password.encode('utf-8'))
        password = password.hexdigest()
        print(password)
        cur.execute("select password from users where login = '%s';" % (str(login)))
        row = cur.fetchone()
        real_pass = row[0]
        if (real_pass == password):
            resp = "ok"
        else:
            resp = "Wrong!"
            return jsonify({"Result": None})            
        print (resp)
        token = ''
        secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
        
        payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=108000),
        'iat': datetime.datetime.utcnow(),
        'sub': login
        }
        token = jwt.encode(
        payload,
        secret_key,
        algorithm='HS256'
        )
        token_b =  token.decode('utf-8')
        print('token', token.decode('utf-8'))
        return jsonify({"Result": token_b})

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run(host = "localhost", port = 5004)
    
