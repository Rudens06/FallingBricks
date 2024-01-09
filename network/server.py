import socket
from _thread import *
import sys

server = "192.168.101.4"
port = 5555
receive_buffer = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)
  
s.listen(2)
print("Server Started, waiting for a connection...")

def read_pos(str):
        str = str.split(",")
        return int(str[0]), int(str[1])
    
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def encode_player_pos(current_player):
    return str.encode((make_pos(player_positions[current_player])))
    
def receive_pos(conn):
    return read_pos(conn.recv(receive_buffer).decode("utf-8"))

def update_player_pos(current_player, position):
    player_positions[current_player] = position

player_positions = [(350,300), (200, 200)]

def threaded_client(conn, current_player):
    conn.send(encode_player_pos(current_player))
    reply=""
    while True:
        try:
            data = receive_pos(conn)
            update_player_pos(current_player, data)
            
            if not data:
                print("Disconnected")
                break
            else:
                if current_player == 1:
                    reply = encode_player_pos(0)
                elif current_player == 0:
                    reply = encode_player_pos(1)
                
                print("Received: ", data)
                print("Sending: ", reply)
            
            conn.sendall(reply)
        except:
            break
    
    print("Lost connection")
    conn.close()

current_player = 0

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
