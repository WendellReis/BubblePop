import pygame
import globals

class Debug:
    def __init__(self):
        self.font = pygame.font.SysFont(None,50)

        self.turn = 0
        self.state = -1

        self.TEXTS = {
            "turn": self.render("Turn: 0"),

            globals.STATE_SETUP_SKY: self.render('SETUP'),
            globals.STATE_SWAP_BUBBLEES: self.render('SWAP BUBBLEES'),
            globals.STATE_DROP_BUBBLEES: self.render('DROP BUBBLEES'),
            globals.STATE_CHECK_MATCHES: self.render('CHECK MATCHES'),
            globals.STATE_CHOOSE_POWER: self.render('CHOOSE POWER'),
            globals.STATE_CHECK_WIN: self.render('CHECK WIN'),
            globals.STATE_ENDGAME: self.render('ENDGAME'),

            globals.STATE_USE_POWER: {
                'red': self.render('RED'),
                'blue': self.render('BLUE'),
                'purple': self.render('PURPLE'),
                'green': self.render('GREEN'),
                'yellow': self.render('YELLOW'),
            }
        }
                
    def render(self,text,font=80):
        if font == 80:
            return self.font.render(text, True, (0, 0, 0))
    
    def update(self,game):
        turn = game.get_turn()
        if turn != self.turn:
            self.turn = turn
            self.TEXTS["turn"] = self.render(f"Turn: {turn}")

    def draw(self,screen,game):
        screen.blit(self.TEXTS["turn"],(650,100))
        screen.blit(self.TEXTS[game.get_current_state()],(650,150))