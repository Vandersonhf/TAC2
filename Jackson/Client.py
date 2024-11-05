import socket


class AppClient:
    def __init__(self, host, port):        
        self.host = host
        self.port = port        

    def send(self, message):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        # send message
        data_string = message.encode()
        self.socket.send(data_string)
        self.socket.close()
        
        client.receive()
    
    def receive(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port + 1))
        self.socket.listen(1)
        print(f'AppClient listening on port {self.port + 1}!')    
        while True:
            conn, address = self.socket.accept()
            print(f"Received connection from {address}")
            with conn:
                data = conn.recv(128)
                message = data.decode()
                print(message)
                break   # one message only
        self.socket.close()


client = AppClient("localhost",  5041)
client.send("OI")
