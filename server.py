import socket
from _thread import *
from player import Player
import pickle
import sys

server = "192.168.0.102"
port = 5555

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)  # AFNET means types of connection, SOCK_STREAM means how information is coming in.

try:
    s.bind((server, port))  # port might be busy then it might throw error, so encole in try except block
except socket.error as e:  # connecting server and port
    str(e)

s.listen(2)  # the parameter implies number of connection allows
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, (255, 0, 0)), Player(100, 100, 50, 50, (0, 0, 255))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:  # while client is connected it will be running continuously
        try:  # if we get error try to increase this size
            data = pickle.loads(conn.recv(
                2048))  # this represent size of data, if we want larger amount of data then do like 2048*8, but they will become slower because larger amount of data
            players[player] = data

            if not data:  # if we don't get any data, then it means the connection has ended
                print("Disconnected")
                break
            else:  # then connection is there so getting and sending data
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(
                pickle.dumps(reply))  # sending information over server, so we convert data to byte format and send
        except:
            break

    print("Lost connection")
    conn.close()  # when we close connection, we need to do this


currentPlayer = 0
while True:  # this will continusouly look for connection, continusously try to grab connection
    conn, addr = s.accept()  # this is conn is going to be the connection, addr will  be the ip address
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1

# if cannot run the server file then we mainly it might be because port number ex:5050 already being used
# so we need to kill port 5050. To do this
# do this in cmd prompt
# netstat -ano | findstr :5555
# then we will get o/p like this
#  TCP    192.168.0.103:5050     0.0.0.0:0              LISTENING       8680
#  UDP    0.0.0.0:5050           *:*                                    6772
# in output there might be more than 2 rows somethings, just try all number, (Mainly the row which has LISTENING will do the work)
# now try to destroy both 8680 and 6772, i am not sure which one but try to do with both if one dies it server will run again
# taskkill /PID 13336 /F       # if this fails try
# taskkill /PID 6772 /F
# o/p will be now
# SUCCESS: The process with PID 8680 has been terminated.
