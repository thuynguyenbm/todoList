from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route('/')
def home():
    return "hi!"

@app.route('/api/list', methods=['GET'])
def list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM toDo")
    toDo = cur.fetchall()
    res=[]
    for item in toDo:
        data={}
        data['id'] = item[0]
        data['description'] = item[1]
        data['status'] = item[2]
        res.append(data)
    return jsonify(res)

@app.route('/api/add', methods=['POST'])
def add():
    toDo = request.get_json(force=True)
    itemDescription = toDo['itemDescription']
    cur = mysql.connection.cursor()
    latestId=cur.execute("SELECT id FROM toDo ORDER BY ID DESC LIMIT 1")
    cur.execute("INSERT INTO toDo(id, description, status) VALUES (%s, %s, 'Doing')", [latestId,itemDescription])
    mysql.connection.commit()
    cur.close()
    message={'message':'added sucessfully!'}
    return message

@app.route('/api/update',methods = ['GET'])
def edit():
    id = request.args.get('id')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM toDo WHERE id = %s", [id])
    toDo = cur.fetchone()
    if toDo[2] == 'Doing':
        cur.execute("UPDATE toDo SET status = 'Done' WHERE id = %s", [id])
    else:
        cur.execute("UPDATE toDo SET status = 'Doing' WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    message = {'message':'updated sucessfully!'}
    return message

@app.route('/api/delete',methods=['GET']) 
def remove():
    id = request.args.get('id')
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM toDo WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    message = {'message':'deleted sucessfully!'}
    return message

if __name__ == '__main__':
    app.run(debug=True)