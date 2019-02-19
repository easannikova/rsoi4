import psycopg2
import flask 
from flask import jsonify
from flask import request
import json
from flask_cors import CORS
import math
import hashlib
import datetime

secret_key = b'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
client_id = '83df86a8cdca48f0bc03a7869eca3096'
app = flask.Flask(__name__)
CORS(app)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def hash_sk():
    h = hashlib.sha256(secret_key)
    return h.hexdigest()

def db_conn():
    con = None
    con = psycopg2.connect(database = 'seansesDB', user = 'sea')
    return con


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def seanse_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    '''for field_name in ['hall_id', 'movie_id']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(
          field_name))'''

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code

secret_key = b'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
client_id = '5086fa03f5564bc7bc78e1f37409ed1d'

@app.route('/')
def root():
    return flask.redirect('/api/1.0/seanses')

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


@app.route('/api/1.0/seanses', methods=['GET'])
def get_seanses():
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from seanses;')
        rows = cur.fetchall()
        seanses = []
        for row in rows:
            seanses.append({"id": row[0], "data": row[1], "time": row[2], "hall_number": row[3], "movie_title": row[4]})
        return jsonify({"seanses": seanses})

@app.route('/api/1.0/seanses/auth', methods=['GET'])
def get_seanse_token(movie_id):
    #создем токен проверяем логин пароль
    login = request.json['login']
    password = request.json['password']
    if (password == secret_key & login == client_id):
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
    else
        return jsonify({"Result": None})

@app.route('/api/1.0/seanses/<int:movie_id>', methods=['GET'])
def get_seanse(movie_id):
    #проверяем валидность токена
    token = request.headers.get("token")
    try:
        payload = jwt.decode(auth_token, secret_key)
        exp = payload['exp']
    except jwt.ExpiredSignatureError:
        return ({"Error": "Access denied!"})
    except jwt.InvalidTokenError:
        return ({"Error": "Access denied!"})
    if (exp < datetime.time / 1000):
        return ({"Error": "Access denied!"})
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from seanses where id = %s;', (str(movie_id),))
        row = cur.fetchone()
        seanse = {"id": row[0], "data": row[1], "time": row[2], "hall_number": row[3], "movie_title": row[4]}
        return jsonify({"seanse": seanse})


@app.route('/api/1.0/seanses', methods=['POST'])
def post_seanse():
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    (json, errors) = seanse_validate()
    if errors:  # list is not empty
        return resp(400, {"errors": errors})

    with db_conn() as db:
        cur = db.cursor()
        hall_id = request.json['hall_number']
        movie_id = request.json['movie_title']
        data = request.json['data']
        time = request.json['time'] 
        id = request.json['id']
        print(id, hall_id, movie_id)
        #INSERT INTO seanses (id, hall_id, year, movie_id, genre, rating, FC) VALUES ($1, $2, $3, $4, $5, $6, $7)
        insert = cur.execute("INSERT INTO seanses (id,  data, time, hall_number, movie_title) VALUES (%s, %s, %s, %s, %s)"
                             + "RETURNING id" % (id, data, time, hall_id, movie_id))
                             #+ "RETURNING id", (str(id), hall_id, movie_id))
        db.commit()
        seanse = {"id": id, "data": data, "time": time, "hall_number": hall_id, "movie_title": movie_id}
        #[(movie_id,)] = insert(json['hall_id'], json['movie_id'])
        return jsonify({"New seanse": seanse})

@app.route('/api/1.0/seanses/<int:seanse_id>', methods=['PUT'])
def put_seanse(seanse_id):
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    (json, errors) = seanse_validate()
    if errors:  # list is not empty
        return resp(400, {"errors": errors})

    with db_conn() as db:
        cur = db.cursor()
        obj = request.json['object']
        value = request.json['value']
        if (obj == 'movie_title'):
            query = "UPDATE seanses SET movie_title = %s WHERE id = %s"
        else:
            query = "UPDATE seanses SET hall_number = %s WHERE id = %s"
        update = cur.execute(query, (str(value), str(seanse_id)))
        db.commit()
        return jsonify({'Result of updating': 'Succes'})


@app.route('/api/1.0/seanses/<int:id>', methods=['DELETE'])
def delete_seanse(id):
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        query = "DELETE FROM seanses WHERE id = %s;" % (str(id))
        delete = cur.execute(query, (str(id)))
        db.commit()
        return jsonify({'Result of deleting': 'Succes'})

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run(host = "localhost", port = 5002)
