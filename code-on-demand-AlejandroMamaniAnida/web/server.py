from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)



@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'


@app.route('/users', methods = ["PUT"])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'


@app.route('/users', methods = ["DELETE"])
def delete_users():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(messages)
    session.commit()
    return "Deleted User"



@app.route('/messages', methods = ["GET"])
def get_messages():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/messages', methods = ['POST'])
def create_message():
    c =  json.loads(request.form['values'])
    message = entities.Message(
        content=c['content'],
        user_from_id=c['user_from']['name']['id'],
        user_to_id=c['user_to']['name']['id']
    )
    session= db.getSession(engine)

    session.add(message)
    session.commit()
    return 'Created Message'


@app.route('/messages', methods=["PUT"])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        try:
            setattr(message, key, c[key])
        except AttributeError:
            _key = key+'_id'
            setattr(message,_key,c[key]['name']['id'])
    session.add(message)
    session.commit()
    return 'Updated Message Form'

@app.route('/messages', methods = ["DELETE"])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(messages)
    session.commit()
    return "Deleted Message"


@app.route('/authenticate', methods = ["POST"])
def authenticate():
    message = json.loads(request.data)
    username = message['username']
    password = message['password']
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username == username
            ).filter(entities.User.password == password
            ).one()
        session['logged_user'] = user.id
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


@app.route('/current', methods = ["GET"])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(
        entities.User.id == session['logged_user']
        ).first()
    return Response(json.dumps(
            user,
            cls=connector.AlchemyEncoder),
            mimetype='application/json'
        )


@app.route('/logout', methods = ["GET"])
def logout():
    session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = ".."
app.run(port=5000, threaded=True, host=('127.0.0.1'))
