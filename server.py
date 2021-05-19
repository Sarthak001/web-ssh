import ssh
from flask import Flask,render_template,redirect, url_for,request,session,app
from datetime import datetime , timedelta
from flask_socketio import SocketIO,send,emit
import _thread
import time
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '!secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://database:database@192.168.122.76:3306/webssh'
socketio = SocketIO(app)
db = SQLAlchemy(app)

users = {}




class logs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    source_ip = db.Column(db.String(100))
    ssh_ip = db.Column(db.String(100))
    time = db.Column(db.String(100))


    def __init__(self,source_ip,ssh_ip,time):
        self.source_ip = source_ip
        self.ssh_ip = ssh_ip
        self.time = time

















@app.route('/')
def details():
    return render_template('details.html')

@app.route('/auth',methods=["POST"])
def auth():
    ip = request.form["ip"]
    port = request.form["port"]
    username = request.form["username"]
    password = request.form["password"]
    session['ip'] = ip
    ip_address = request.remote_addr
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    log = logs(ip_address,ip,dt_string)
    db.session.add(log)
    db.session.commit()

    port = int(port)
    obj = ssh.ssh(ip,port,username,password)
    users[ip] = obj
    # ssh.connection(ip,port,username,password)
    _thread.start_new_thread(obj.recv, ())
    return redirect(url_for('terminal'))
    

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


@app.route('/admin')
def test2():
    l = logs.query.filter(logs.id > 0).all()
    return render_template('adminlogs.html',data=l)

@app.route('/ui')
def ui():
    return render_template('terminal.html')





if __name__ == '__main__':
    db.create_all()
    socketio.run(app,debug=True)