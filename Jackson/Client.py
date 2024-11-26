import socket
from .Game import settings

class AppClient:
    def __init__(self, host, port):        
        self.host = host
        self.port = port    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

    def connect_server(self):     
        try:          
            self.socket.connect((self.host, self.port))
            self.conn = self.socket
            settings.client_connected = True
        except Exception as E:
            print("Could not connect to server:", E)
        
    def send_message(self, message):
        data_bytes = message.encode()
        self.conn.send(data_bytes)
    
    def receive_messages(self):
        with self.conn:
            while True:
                try:
                    #receive data
                    data = self.conn.recv(settings.size)
                    message = data.decode()
                    if len(settings.buffer_in) < settings.buffer_in_max:
                        settings.buffer_in.append(message)
                except: break
                    

