import pygame


class BG(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('graphics/background.png').convert()

        self.rect = self.image.get_rect(topleft = (0,0))


class Button(pygame.sprite.Sprite):
    def __init__(self, groups, b_name, callback) -> None:
        super().__init__(groups)
    
        self.name = b_name

        self.callback = callback

        self.image = pygame.image.load(f'graphics/buttons/{b_name}.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect(topleft = (0,0))
    
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.mask.get_at(event.pos):
                    self.callback()
                
   
class Pot(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('graphics/board/pot.png').convert_alpha()

        self.rect = self.image.get_rect(topleft = (0,0)) 


class BoardCards(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('graphics/board/boardCard.png').convert_alpha()

        self.rect = self.image.get_rect(topleft = (0,0))


class StableBoard(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        self.image = pygame.image.load('graphics/board/stableOb.png').convert_alpha()

        self.rect = self.image.get_rect(topleft = (0,0))


class Text():
    def __init__(self,font, x, y,screen) -> None:

        self.font = font
        self.x , self.y = x, y
        self.screen = screen

    
    def get_text(self):
        return self.text
    
    def show(self, text):
        img = self.font.render(text, True, 'white')
        self.screen.blit(img, (self.x, self.y))


class Cards():
    def __init__(self, id, id_player, screen) -> None:

        if id == id_player:
            image = pygame.image.load('graphics/players/p1.png').convert_alpha()
            rect = image.get_rect(topleft = (0,0))
            screen.blit(image, rect)
        else:
            image = pygame.image.load('graphics/players/p2.png').convert_alpha()
            rect = image.get_rect(topleft = (0,0))
            screen.blit(image, rect)

    
        



        
       
        








        



