import ssh
from flask import Flask,render_template,redirect, url_for,request,session,app
from datetime import datetime , timedelta
from flask_socketio import SocketIO,send,emit
import _thread
import time
import database
import os
import pathlib
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


path = pathlib.Path(__file__).parent.absolute()


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '!secret!'
socketio = SocketIO(app)
UPLOAD_FOLDER = f'{path}/keys'
app.config['UPLOAD_FOLDER'] = "/home/kahtras/projects/web-ssh/keys"
ALLOWED_EXTENSIONS = {'.pub'}
users = {}
active_shells = []

@app.route('/')
def details():
    return render_template('details.html')

@app.route('/auth',methods=["POST"])
def auth():
    ip = request.form["ip"]
    port = request.form["port"]
    username = request.form["username"]
    password = request.form["password"]
    authmethod = request.form["auth"]
    if(authmethod == "key"):
        password = ''
        key = request.files['key']
        filename = secure_filename(key.filename)
        key.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), encoding = 'utf-8') as f:
            privatekey = f.read()
        if(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            print("The file does not exist") 
    else:
        privatekey  = ''

    session['ip'] = ip
    ip_address = request.remote_addr
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log = database.logs(source_ip=ip_address,ssh_ip=ip,time=dt_string)
    activeuser = database.activeusers(source_ip=ip_address,ssh_ip=ip,time=dt_string)
    database.session.add(log)
    database.session.commit()
    database.session.add(activeuser)
    database.session.commit()

    port = int(port)
    obj = ssh.ssh(ip,port,username,authmethod,password,privatekey)
    users[ip] = obj
    # ssh.connection(ip,port,username,password)
    
    return redirect(url_for('terminal'))

@app.route('/adminauth',methods=["POST"])
def adminauth():
    password = request.form["password"]
    session['admin'] = password
    print(password)
    if password == "superuserdo":
        return render_template('adminpanel.html')
    else:
        return redirect(url_for('ui'))

@app.route('/terminal')
def terminal():
    if not session.get("ip"):
        return redirect(url_for('details'))
    else:
        return render_template('terminal.html')


@app.route('/info')
def info():
    if not session.get("ip"):
        return redirect(url_for('details'))
    else:
        gg = ''
        lst = list(users.keys())
        print(lst)
        if(session["ip"] in lst):
            obj = users[session["ip"]]
            obj.details()
            gg= obj.recv()
            print(gg)
        return render_template('sv_info.html',data=gg)


@socketio.on('jsrecv')
def jsrecv(msg):
    lst = list(users.keys())
    if(session["ip"] in lst):
        obj = users[session["ip"]]
        obj.send(msg)
        data = obj.recv()
        emit('py',data)


@app.route('/log')
def log():
    l = logs.query.filter(logs.id > 0).all()
    
    return render_template('adminpanel.html',data=l)

@app.route('/activeusers')
def activeusers():
    return render_template('adminpanel.html')

@app.route('/ui')
def ui():
    return render_template('adminauth.html')


@app.route('/disconnect')
def disconnect():
    if(session["ip"] in active_shells):
        obj = users[session["ip"]]
        result = obj.disconnect()
        active_shells.remove(session["ip"])
        return redirect(url_for('terminal'))

@app.route('/connect')
def connect():
    if not(session["ip"] in active_shells):
        print(users)
        obj = users[session["ip"]]
        obj.connection()
        _thread.start_new_thread(obj.recv, ())
        obj.invoke_shell()
        active_shells.append(session["ip"])
        return redirect(url_for('terminal'))





if __name__ == '__main__':
    socketio.run(app,debug=True)