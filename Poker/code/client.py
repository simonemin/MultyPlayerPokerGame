import socket
from game import Game
import pickle
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = ''
port = 5555
addr = (server, port)
start = False
p_name = input('Enter your player name!')

client.connect(addr)

while True:
    if not start:
        try:
            message = client.recv(1024).decode('ascii')

            if message == 'p_name':
                client.send(p_name.encode('ascii'))
            elif message == 'inizio':
                start = True
                client.send(f'{p_name}: ready!'.encode('ascii'))
            else:
                print(message)   
        except:
            client.close()
            print('Error')
            break
    else:
        break

#players list
players = pickle.loads(client.recv(1024))
print(players)

game = Game(client, players, p_name)
game.run()
sys.exit()















