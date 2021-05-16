import ssh
from flask import Flask,render_template,redirect, url_for,request,session,app
from datetime import timedelta
from flask_socketio import SocketIO,send,emit
import _thread
import time

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '!secret!'
socketio = SocketIO(app)

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
    port = int(port)
    ssh.connection(ip,port,username,password)
    _thread.start_new_thread(ssh.recv, ())
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
        return render_template('sv_info.html')


@socketio.on('jsrecv')
def jsrecv(msg):
    ssh.send(msg)
    r_msg = ssh.recv()
    socketio.emit('py',r_msg)


if __name__ == '__main__':
    socketio.run(app,debug=True)