import pygame
import globals

class Debug:
    def __init__(self):
        self.font = pygame.font.SysFont(None,50)

        self.turn = 0
        self.turn_power = -1
        self.state = -1

        self.TEXTS = {
            "turn": self.render("Turn: 0"),
            "turn_power": self.render("Turn Power: -1"),
            globals.STATE_SETUP_SKY: self.render('SETUP'),
            globals.STATE_SWAP_BUBBLEES: self.render('SWAP BUBBLEES'),
            globals.STATE_DROP_BUBBLEES: self.render('DROP BUBBLEES'),
            globals.STATE_CHECK_MATCHES: self.render('CHECK MATCHES'),
            globals.STATE_CHOOSE_POWER: self.render('CHOOSE POWER'),
            globals.STATE_CHECK_WIN: self.render('CHECK WIN'),
            globals.STATE_ENDGAME: self.render('ENDGAME'),
            globals.STATE_POWER_RED: self.render('POWER RED'),
            globals.STATE_POWER_BLUE: self.render('POWER BLUE'),
            globals.STATE_POWER_PURPLE: self.render('POWER PURPLE'),
            globals.STATE_POWER_GREEN: self.render('POWER GREEN'),
            globals.STATE_POWER_YELLOW: self.render('POWER YELLOW')
        }
                
    def render(self,text,font=80):
        if font == 80:
            return self.font.render(text, True, (0, 0, 0))
    
    def update(self,game):
        turn = game.get_turn()
        turn_power = game.get_turn_power()
        if turn != self.turn:
            self.turn = turn
            self.TEXTS["turn"] = self.render(f"Turn: {turn}")
        if turn_power != self.turn_power:
            self.turn_power = turn_power
            self.TEXTS["turn_power"] = self.render(f"Turn Power: {turn_power}")

    def draw(self,screen,game):
        self.update(game)
        screen.blit(self.TEXTS["turn"],(650,50))
        screen.blit(self.TEXTS["turn_power"],(650,100))
        if game.get_current_state() == globals.STATE_ENDGAME:
            text = self.render(f"Vitoria do jogador {game.get_winner()}")
            screen.blit(text,(650,150))
        else:
            screen.blit(self.TEXTS[game.get_current_state()],(650,150))