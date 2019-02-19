import psycopg2
import flask 
from flask import jsonify
from flask import request
import json
from flask_cors import CORS
import math
import hashlib

secret_key = b'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
client_id = 'a21512acc9154a1fa3c413b3c8defc8b'
app = flask.Flask(__name__)
CORS(app)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def hash_sk():
    h = hashlib.sha256(secret_key)
    return h.hexdigest()

def db_conn():
    con = None
    con = psycopg2.connect(database = 'hallsDB', user = 'sea')
    return con


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def hall_validate():
    errors = []
    json = request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    '''for field_name in ['number']:
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


@app.route('/')
def root():
    return flask.redirect('/api/1.0/halls')

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


@app.route('/api/1.0/halls', methods=['GET'])
def get_halls():
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from halls;')
        rows = cur.fetchall()
        halls = []
        for row in rows:
            halls.append({"id": row[0], "number": row[1], "floor": row[2], "seats_count": row[3], "is3d": row[4]})
        return jsonify({"halls": halls})

@app.route('/api/1.0/halls/<int:hall_id>', methods=['GET'])
def get_hall(hall_id):
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        cur.execute('SELECT * from halls where id = %s;', (str(hall_id)))
        row = cur.fetchone()
        hall = {"id": row[0], "number": row[1], "floor": row[2], "seats_count": row[3], "is3d": row[4]}
        return jsonify({"hall": hall})


@app.route('/api/1.0/halls', methods=['POST'])
def post_hall():
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        print("dddddddddd")
        cur = db.cursor()
        hall_id = 100
        print('hallllllllllll idddddd', hall_id);
        number = request.json['number']
        floor = request.json['floor']
        seats_count = request.json['seats_count']
        is3d = request.json['is3d']
        print("is3d"+is3d)
        print("seats_count"+seats_count)

        #hall_id = request.json['id']
        insert = cur.execute("INSERT INTO halls (id, number, floor, seats_count, is3d) VALUES (%s, %s, %s, %s,%s)"
                             + "RETURNING id", (str(hall_id), str(number), str(floor), str(seats_count), str(is3d)))
        db.commit()
        hall = {"id": hall_id, "number": number, "floor": floor, "seats_count": seats_count, "is3d": is3d}
        return jsonify({"New hall": hall})

@app.route('/api/1.0/halls/<int:hall_id>', methods=['PUT'])
def put_hall(hall_id):
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    (json, errors) = hall_validate()
    if errors:  # list is not empty
        return resp(400, {"errors": errors})
    with db_conn() as db:
        cur = db.cursor()
        print("jssoooonn", request.json)
        number = request.json['number']
        print(hall_id, number)
        query = "UPDATE halls SET number = %s WHERE id = %s"
        update = cur.execute(query, (str(number), str(hall_id)))
        db.commit()
    return jsonify({'Result of updating': 'Succes'})


@app.route('/api/1.0/halls/<int:hall_id>', methods=['DELETE'])
def delete_hall(hall_id):
    secret = request.headers.get("secret")
    my_secret = hash_sk()
    if my_secret == secret:
        return ({"Error": "Access denied!"})
    with db_conn() as db:
        cur = db.cursor()
        query = "DELETE FROM halls WHERE id = %s" % (str(hall_id))
        delete = cur.execute(query)
        db.commit()
        return jsonify({'Result of deleting': 'Succes'})

if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run(host = "localhost", port = 5001)
