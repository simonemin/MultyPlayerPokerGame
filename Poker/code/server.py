import socket, time, copy
import threading
import pickle
from deck import Deck
from winConditions import winCondition


class My_server():
    def __init__(self) -> None:
            
        server = ''
        port = 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:  
            self.s.bind((server, port))
        except socket.error as e:
            print(e)

        self.n_players = int(input('Tell me the number of total players!'))

        self.s.listen()
        print('Waiting for a connection') 
        
        self.clients = []
        self.players_name = []
        self.ids = []
        self.mainDeck = Deck()
        self.players_hands = {}
        self.game_board = []
        self.set_board = True
        self.start_game = False

    
    def handle_player(self, client, id):
        client.send('inizio'.encode('ascii'))
        reply = client.recv(1024).decode('ascii')
        print(reply)
        client.send(pickle.dumps(self.players_name))
        while True:
            if not self.set_board and not self.start_game:
                client.send(pickle.dumps(self.players_hands[id]))
                ver = client.recv(1024).decode('ascii')
                print(ver)
                client.send(pickle.dumps(self.game_board))
                ver = client.recv(1024).decode('ascii')
                print(ver)
                self.start_game = True

            if self.start_game:    
                try:    
                    message = pickle.loads(client.recv(1024))
                    print(message)
                    # special cases
                    if message[1] == 'quit':
                        client.sendall(pickle.dumps(message))
                        index = self.clients.index(client)
                        self.clients.remove(client)
                        #self.ids.remove(id)
                        del self.players_name[index]
                        client.close()
                        break
                    if int(message[2]) == 0:
                        message = self.checkWinner()
                        for cl in self.clients:
                            cl.sendall(pickle.dumps(message))
                        continue   

                    # sending to the players
                    for cl in self.clients:
                        if cl != client:
                            cl.sendall(pickle.dumps(message))

                except:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    del self.players_name[index]
                    #self.ids.remove(id)
                    client.close()
                    break

    def checkWinner(self):
        max = 0
        index = None
        
        for i in self.players_hands:
            board = self.game_board
            print(i)
            cards = copy.deepcopy(self.game_board) + self.players_hands[i]
            print(self.game_board)
            print(cards)
            res = winCondition(cards)
            if max < res:
                max = res
                index = i
        if max == 0:
            message = 'tie'
        else:
            message = f'winner,{index}'
            lis = message.split(",")
            print(type(lis[1]), lis)
        
        return message




    def broadcast(self,message):
        for client in self.clients:
            client.send(message)

    def Hand(self):
        hand = []
        for _ in range(2):
            hand.append(self.mainDeck.dealCard())
        return hand  
              
    # def Flop(cl):
    #     _ = mainDeck.dealCard()
        
    #     cl.sendall(pickle.dumps(mainDeck.dealCard()))
       
    def run(self):
        id = 0      
        while True:
            client, addr = self.s.accept()
            print('Connected to:', addr)
            
            client.send('p_name'.encode('ascii'))
            p_name = client.recv(1024).decode('ascii')
            print(f'{p_name} is the new player!') 
            self.broadcast(f'{p_name} has joined the table'.encode('ascii'))
            self.players_name.append(p_name)
            self.clients.append(client)
            print(self.clients)
            
            
            
            if len(self.clients) == self.n_players:
                for client in self.clients:
                    self.ids.append(id)
                    thread = threading.Thread(target=self.handle_player, args=(client,id))
                    thread.start()
                    id += 1
                break

        while True:
            if self.set_board:
                for i in self.ids:
                  self.players_hands[i] = self.Hand()  
                _ = self.mainDeck.dealCard()
                for _ in range(3):
                    self.game_board.append(self.mainDeck.dealCard())
                self.set_board = False
                break


server = My_server()
server.run()
    

            


    
        


    

    





