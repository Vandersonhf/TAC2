import socket
from .Game import settings
SIZE = 1024

class AppClient:
    def __init__(self, host, port):        
        self.host = host
        self.port = port    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

    def connect_server(self):               
        self.socket.connect((self.host, self.port))
        self.conn = self.socket
        
    def send_message(self, message):
        data_string = message.encode()
        self.conn.send(data_string)
        
    def receive_messages(self):
        with self.conn:
            while True:
                #receive data
                data = self.conn.recv(SIZE)
                message = data.decode()
                if len(settings.buffer) < settings.buffer_max:
                    settings.buffer.append(message)
                    

    def send_receive(self, message):        
        self.socket.connect((self.host, self.port))
        conn = self.socket
        
        # send message
        data_string = message.encode()
        conn.send(data_string)
        print("message sent ", message)
        
        # receive aswer                  
        print(f"Received answer from {self.host}")
        with conn:
            data = conn.recv(SIZE)
            answer = data.decode()
            print("server answer ",answer)
        

#client = AppClient("localhost",  5041)
#client.send_receive("OI")
