import socket


class AppServer:
    def __init__(self, host, port):        
        self.host = host
        self.port = port

    def receive(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Server up!')
        while True:
            conn, address = self.socket.accept()
            print(f'received connection from {address}')
            with conn:
                data = conn.recv(128)
                message = data.decode()
                print(message)
                server.send("OLA")
                break
    
    def send(self, message):      
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
        #with self.socket:
        self.socket.connect((self.host, self.port+1))
        print("conectado socket 2")
        self.socket.send(message.encode())                


server = AppServer("localhost", 5041)
server.receive()
