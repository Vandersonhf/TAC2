import socket
from .Game import settings

class AppClient:
    def __init__(self, host, port, iprange = 0):        
        self.host = host
        self.port = port    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.iprange = iprange    
        #self.find_host()

    def find_host(self):
        abcd = self.host.split('.')
        for d in range(int(abcd[3]), int(abcd[3])+self.iprange+1):
            self.host = f'{abcd[0]}.{abcd[1]}.{abcd[2]}.{d}'
            try:  
                print("trying ", self.host)        
                self.socket.connect((self.host, self.port))
                self.socket.close()
                print('found', self.host)
                return 
            except: pass
    
    def connect_server(self):     
        try: 
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
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
                    

