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
        
    '''def send_messages_buffer(self):
        for message in settings.buffer_out:
            self.send_message(message)
        settings.buffer_out = []'''

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
            data = conn.recv(settings.size)
            answer = data.decode()
            print("server answer ",answer)
        

#client = AppClient("localhost",  5041)
#client.send_receive("OI")
