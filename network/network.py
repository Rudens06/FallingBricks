import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.101.4"
        self.port = 5555
        self.receive_buffer = 2048
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        
    def get_pos(self):
        return self.pos
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(self.receive_buffer).decode('utf8')
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(self.receive_buffer).decode('utf8')
        except socket.error as e:
            print(e)
     