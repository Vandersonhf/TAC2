import socket
SIZE = 1024

class AppClient:
    def __init__(self, host, port):        
        self.host = host
        self.port = port    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    

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
        

client = AppClient("localhost",  5041)
client.send_receive("OI")
