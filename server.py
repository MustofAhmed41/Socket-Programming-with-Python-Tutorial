import socket  # sockets and threading will handle connections to our server
from _thread import *  # allows other to connect to our serve
import sys

# this file is for creating server, whenever we want clients to connect this must be in running mode
# the server scripts must be running on this i/p address as given in string "server" variable
# we can run clients scrips on the same machine as i/p

server = "192.168.0.105"  # this is my pcs i/p address from user prompt # server entrance
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 1st parameter implies type of connection

# bind our server to sockets


#  if port 5555 is already being used it might throw error

try:
    s.bind((server, port))  # binding server to port
except socket.error as e:
    str(e)

s.listen(2)  # opening up port # if we dont pass anything as parameter it won't limit any number of clients but
# we are going to limit it to 2

print("Waiting for a connection, Server started")


def threaded_client(conn):
    #  we want our client to be connected continously so we are going to do it in while loop

    while True:
        try:
            data = conn.recv(2048)  # this 2048 represents size of data sent by client. If the size of
            # data is large then we can put like 2048*5, but the larger the file the slower the client
            reply = data.decode("utf-8")  # whenever we send data in client-server then we
            # send encoded data, so we need to decode it here

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(reply))  # sending data in encoded format (in byte size)
        except:
            break


while True:  # this loop will continuously check if there is any connection
    conn, addr = s.accept()  # this is going accept clients, in addr variable IP address of client will be stored
    print("Connected to: ", addr)

    start_new_thread(threaded_client(conn, ))
