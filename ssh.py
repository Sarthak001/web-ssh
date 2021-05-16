from __future__ import print_function
import os
import socket
from ssh2.session import Session
import _thread
import time



def connection(ip,port,username,passwd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    session = Session()
    session.handshake(sock)
    # session.agent_auth(user)
    session.userauth_password(username, passwd)
    connection.channel = session.open_session()
    connection.channel.pty(term='bash')
    connection.channel.shell()


    

def send(msg):
    connection.channel.write(msg)

def recv():
    while True:
        time.sleep(0.01)
        size, data = connection.channel.read(9999)
        return(data.decode())
        

def disconnect():
    connection.channel.close()
    return ("Exit status: %s" % connection.channel.get_exit_status())




