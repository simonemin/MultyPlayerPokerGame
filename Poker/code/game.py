import pygame, time, sys
from settings import *
from sprites import BG, Button, Pot, BoardCards, StableBoard, Text, Cards
from deck import Player
import pickle
import threading

class Game():
    
    def __init__(self, client, players, your_name):
        
        # setup
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOWS_WIDHT, WINDOWS_HEIGHT))
        pygame.display.set_caption('SimPoker/Game')
        self.clock = pygame.time.Clock()

        # players
        self.main_player = None
        self.client = client
        self.send_packet = []
        self.players = players
        self.n_players = len(players)
        for i, name in enumerate(players):
            if name == your_name:
                self.main_player = Player(str(i), your_name)
        
        # text
        self.message_on_screen = 'New Game'
        self.text_font_player_name = pygame.font.Font(None, 64)
        self.text_name = Text(self.text_font_player_name, 20, 20, self.screen)
        self.text_font_box = pygame.font.Font(None, 28)
        self.box_mess = Text(self.text_font_box, 590, 422, self.screen)
        self.x, self.y = 590, 422
        self.bet_text = Text(self.text_font_box, 620, 440, self.screen)
        self.user_input = '100'
        self.error_text = Text(self.text_font_box,500, 10, self.screen)
        self.err = ''

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        # sprite setup
        BG(self.all_sprites)
        # buttons actions
        Button(self.all_sprites, 'check', self.check)
        Button(self.all_sprites, 'fold', self.fold)
        Button(self.all_sprites, 'raise', self.up)
        Button(self.all_sprites, 'call', self.call)
        
        # board setup
        StableBoard(self.all_sprites)
        BoardCards(self.all_sprites)
        self.pot_image = Pot(self.all_sprites)
        self.board = []
        self.cards = []

        

        # game variables
        self.pot = 0
        self.your_turn = False
        self.next_turn = (int(self.main_player.get_id())+1)%self.n_players
        self.new_game = True
        self.bet_active = False
        self.bet = 0
        self.flop = False
        
        
        
    
    # Actions
    def check(self):
        if self.your_turn:
            print('Check')
            self.main_player.set_status('check')    
            self.send_packet = [self.main_player.get_id(), 'check', str(self.next_turn)]
            self.client.sendall(pickle.dumps(self.send_packet))
            self.your_turn = False
            self.x, self.y = 520, 422
            self.message_on_screen = f'{self.players[self.next_turn]} is playing'

    def fold(self):
        if self.your_turn:
            print('Fold')
            self.main_player.set_status('fold')
            self.your_turn = False

    def up(self):
        if self.your_turn:
            print('Raise')
            self.main_player.set_status('raise')
            self.your_turn = False
            self.bet_active = True

    def call(self):
        if self.your_turn:
            print('Call')
            self.main_player.set_status('call')  
            if self.main_player.get_chips() >= self.bet:
                self.main_player.set_chips(-self.bet)
                self.main_player.set_pot(self.bet)
                self.your_turn = False
            else:
                self.fold()
    
    def betting(self, bet):
        if bet > self.main_player.get_chips():
            self.err = "You don't have enough chips!"
            self.bet_active = True
        else:
            self.main_player.set_chips(-self.bet)
            self.main_player.set_pot(self.bet)
            print(self.bet)
            self.send_packet = [self.main_player.get_id(), f'bet,{bet}', str(self.next_turn)]
            self.client.sendall(pickle.dumps(self.send_packet))
            self.x, self.y = 520, 422
            self.message_on_screen = f'{self.players[self.next_turn]} is playing'

    # client-server
    def receive(self):
        if self.main_player.get_name() == self.players[0]:
            self.your_turn = True
            self.message_on_screen = 'Your Turn!'
        while True: 
            try:
                message = pickle.loads(self.client.recv(2048))
                print(message)
                if message[1] == 'quit' and message[0] == self.main_player.get_id():
                    sys.exit()
                if message == 'tie':
                    print('tie')
                    self.x, self.y = 590, 422
                    self.message_on_screen = 'Tie'
                    continue
                if 'winner' in message:
                    print('winner')
                    lis = message.split(",")
                    self.x, self.y = 590, 422
                    if lis[1] == self.main_player.get_id():
                        self.message_on_screen = 'YOU WIN'
                    else:
                        self.message_on_screen = f'{self.players[int(lis[1])]} wins'
                    continue

                if message[2] == self.main_player.get_id():
                    self.x, self.y = 520, 422
                    self.message_on_screen = f'{self.players[int(message[0])]}: {message[1]}'
                    time.sleep(2)
                    self.x, self.y = 590, 422
                    self.message_on_screen = 'Your turn!'
                    self.your_turn = True
                else:
                    self.x, self.y = 520, 422
                    self.message_on_screen = f'{self.players[int(message[0])]}: {message[1]}'
                    if self.your_turn:
                        time.sleep(2)
                        self.x, self.y = 590, 422
                        self.message_on_screen = 'Your turn!'
                    time.sleep(2)
                    self.message_on_screen = f'{self.players[int(message[2])]} is playing'
            except:
                self.client.close()
                break
    
    def start_game(self):
        try:
            hand = pickle.loads(self.client.recv(1024))
            print(hand)
            self.client.send('ok'.encode('ascii'))
            board = pickle.loads(self.client.recv(1024))
            print(board)
            self.client.send('ok'.encode('ascii'))        
        except:
            self.client.close()
        
        self.main_player.set_hand(hand)
        self.board.append(board)
        self.new_game = False
        threading.Thread(target=self.receive).start()
           
    
    #pygame
    def run(self):
        last_time = time.time()

        threading.Thread(target=self.start_game).start()

        while True:
            
            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    if self.your_turn:
                        self.client.send(pickle.dumps([self.main_player.get_id(), 'quit', str(self.next_turn)]))
                    else:
                        self.client.send(pickle.dumps([self.main_player.get_id(), 'quit', '']))
                    pygame.quit()
                    sys.exit()
                if self.bet_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_input = self.user_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.bet_active = False
                            try:
                                self.bet = int(self.user_input)
                                self.user_input = '100'
                                self.betting(self.bet)
                            except:
                                self.err = "Enter a whole number!"
                                self.user_input = '100'
                                self.bet_active = True
                        else:
                            self.user_input += event.unicode
            
            
            # game logic
            self.all_sprites.update(events)
            self.screen.fill('black')
            self.all_sprites.draw(self.screen)
            self.text_name.show(self.main_player.get_name())
            self.box_mess.show(self.message_on_screen)
            if self.bet_active:
                self.bet_text.show(self.user_input)
                self.error_text.show(self.err)
            if not self.new_game:
                for i in range(len(self.players)):
                    Cards(str(i), self.main_player.get_id(), self.screen)
                    
            
            
            

            pygame.display.update()
            self.clock.tick(FPS)

        

# if __name__ == '__main__':
#     players = ['Simone','ciccio']
#     name = 'Simone'
#     game = Game(10, players, name)
#     game.run()