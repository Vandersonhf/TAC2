import socket
from .Game import settings
SIZE = 1024

class AppServer:
    def __init__(self, host, port):        
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
    def server_listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        #while True:
        self.conn, address = self.socket.accept()
        print(f'received connection from {address}')
        with self.conn:
            while True:
                #receive data
                data = self.conn.recv(SIZE)
                message = data.decode()
                if len(settings.buffer) < settings.buffer_max:
                    settings.buffer.append(message)
    
    
    def send_message(self, message):
        data_string = message.encode()
        self.conn.send(data_string)
    
    
    def receive_send(self):        
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Server up!')
        while True:
            conn, address = self.socket.accept()
            print(f'received connection from {address}')
            with conn:
                #receive data
                data = conn.recv(SIZE)
                message = data.decode()
                print("received ",message)
                
                # send answer
                answer = "OLA"
                conn.send(answer.encode())
                print("answer sent! ", answer)
                

#server = AppServer("localhost", 5041)
#server.receive_send()