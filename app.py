import os
import logging
import sqlite3
import json
from flask import Flask, jsonify, g, request, make_response
from distutils.util import strtobool

app = Flask(__name__)
logging.basicConfig(filename=os.getenv('FLASK_LOG', 'data/log/flask.log'), level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE = os.getenv('DATABASE', 'data/db/test.db')

#======DB Start
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=[], one=False):
    cur = get_db().cursor().execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return (r[0] if r else None) if one else r

def insert_db(name, status=0):
    db = get_db()
    cur = db.cursor()
    statement = "INSERT INTO Table1(name, status) VALUES (?, ?);"
    cur.execute(statement, [name, status])
    id = cur.lastrowid
    db.commit()
    cur.close()
    return id

def update_db(id, name, status):
    db = get_db()
    cur = db.cursor()
    statement = "UPDATE Table1 SET name = ?, status = ? WHERE id = ?"
    cur.execute(statement, [name, status, id])
    db.commit()
    cur.close()
    return True

def delete_db(id):
    db = get_db()
    cur = db.cursor()
    statement = "DELETE FROM Table1 WHERE id = ?"
    cur.execute(statement, [id])
    db.commit()
    return True
#======DB End


@app.route("/task", methods=["GET"])
def get_task():
    data = query_db('select * from Table1')
    logger.info("Success Get Task!")
    resp = make_response(json.dumps({"result": data}), 200)
    resp.headers['Content-Type'] = "application/json"
    return resp

@app.route("/task", methods=["POST"])
def insert_task():
    details = request.get_json()
    name = details.get('name', None)
    status = details.get('status', 0)
    logger.info("Insert Task Name[%s], Status[%s]" % (name, status))
    try:
        if status not in [0, 1]:
            raise ValueError
        result = insert_db(name, status)
    except ValueError:
        logger.error("Error Insert Task Status[%s]" % (status,))
        resp = make_response("ERROR IN POST Task(The status on can be 1 or 0)!", 400)
    except:
        logger.error("Error Insert Task!")
        resp = make_response("ERROR IN POST Task!", 400)
    else:
        data = query_db('select * from Table1 where id = ?;', args=[result], one=True)
        logger.info("Success Insert Task ID[%s]" % result)
        resp = make_response(json.dumps({"result": data}), 201)
        resp.headers['Content-Type'] = "application/json"
    return resp

@app.route("/task", methods=["PUT"])
def update_task():
    details = request.get_json()
    name = details.get('name', None)
    status = details.get('status', None)
    id = details.get('id', None)
    logger.info("Update Task ID[%s], Name[%s], Status[%s]" % (id, name, status))
    if not (id and name and status != None):
        logger.error("Error Update Task! ID, name, status can not be None!")
        resp = make_response("The ID, name, status can not be None!", 400)
    elif not query_db('select * from Table1 where id = ?;', args=[id], one=True):
        logger.error("Error Update Task ID[%s]" % (id,))
        resp = make_response("The ID[%s] is not Exist!" % id, 400)
    else:
        try:
            if status not in [0, 1]:
                raise ValueError
            update_db(id, name, status)
        except ValueError:
            logger.error("Error Update Task Status[%s]" % (status,))
            resp = make_response("ERROR IN PUT Task(The status on can be 1 or 0)!", 400)
        except:
            logger.error("Error Insert Task!")
            resp = make_response("ERROR IN PUT Task!", 400)
        else:
            data = query_db('select * from Table1 where id = ?;', args=[id], one=True)
            logger.info("Success Update Task ID[%s]" % id)
            resp = make_response(json.dumps({"result": data}), 200)
            resp.headers['Content-Type'] = "application/json"
    return resp

@app.route("/task", methods=["DELETE"])
def delete_task():
    details = request.get_json()
    id = details.get('id', None)
    logger.info("DELETE Task ID[%s]!" % (id, ))

    if not query_db('select * from Table1 where id = ?;', args=[id], one=True):
        logger.error("Error Update Task ID[%s]" % (id,))
        resp = make_response("The ID[%s] is not Exist!" % id, 400)
    else:
        try:
            delete_db(id)
        except:
            logger.error("Error Delete Task!")
            resp = make_response("ERROR IN DELETE Task!", 400)
        else:
            resp = make_response("", 200)
    return resp

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(debug=strtobool(os.getenv('FLASK_DEBUG', True)), host='0.0.0.0', port=8888)