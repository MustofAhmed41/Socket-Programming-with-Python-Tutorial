import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # client address will be automatically be fetched
        self.server = "192.168.0.102"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        # print(self.pos) #prints the information sent back when connected and prints it here

    def getPos(self):
        return self.pos

    def connect(self):
        try: # when we try to connect, we will try to immediately send some information back to the object
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)