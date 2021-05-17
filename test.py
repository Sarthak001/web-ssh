from __future__ import print_function
import os
import socket
from ssh2.session import Session
import _thread
import time



class ssh:
    def __init__(self,ip,port,username,passwd):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.session = Session()
        self.session.handshake(self.sock)
        # session.agent_auth(user)
        self.session.userauth_password(username, passwd)
        self.channel = self.session.open_session()
        self.channel.pty(term='bash')
        self.channel.shell()

    def send(self,msg):
        self.channel.write(msg)

    def recv(self):
        while True:
            time.sleep(0.01)
            size, data = self.channel.read(9999)
            return(data.decode())
        

    def disconnect(self):
        channel.close()
        return ("Exit status: %s" % connection.channel.get_exit_status())

