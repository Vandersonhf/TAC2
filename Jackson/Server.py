import socket
from .Game import settings

class AppServer:
    def __init__(self, host, port):        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
    def server_listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        while True:
            self.conn, address = self.socket.accept()
            print(f'received connection from {address}')
            settings.client_connected = True
            with self.conn:
                while True:
                    try:
                        #receive data
                        data = self.conn.recv(settings.size)
                        message = data.decode()
                        if len(settings.buffer_in) < settings.buffer_in_max:
                            settings.buffer_in.append(message)
                    except: break
    
    
    def send_message(self, message):
        data_string = message.encode()
        self.conn.send(data_string)
    
    