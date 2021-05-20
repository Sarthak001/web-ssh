from __future__ import print_function
import os
import socket
from ssh2.session import Session
import _thread
import time



class ssh:
    def __init__(self,ip,port,username,authmethod,passwd = None,key = None):
        self.ip = ip
        self.port = port
        self.username = username
        self.passwd = passwd
        self.key = key
        self.authmethod = authmethod


    
    def connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        self.session = Session()
        self.session.handshake(self.sock)
        # session.agent_auth(user)
        if(self.authmethod == 'password'):
            self.session.userauth_password(self.username, self.passwd)
            self.channel = self.session.open_session()
        else:
            privatekey = self.key.encode('utf-8')
            self.session.userauth_publickey_frommemory(self.username, privatekey, passphrase='')
            self.channel = self.session.open_session()

    def invoke_shell(self):
        self.channel.pty(term='bash')
        self.channel.shell()

    def send(self,msg):
        self.channel.write(msg)

    def recv(self):
        while True:
            time.sleep(0.01)
            size, data = self.channel.read(9999)
            return(data.decode())
    
    def details(self):
        self.channel.write("hostname \r")
        self.channel.write("uptime \r")
        self.channel.write("hostnamectl | grep Op \r")
        self.channel.write("uname -r \r")




    def disconnect(self):
        self.channel.send_eof()
        self.channel.close()
        self.session.disconnect()
        self.sock.close()
        return ("disconnection successful")

