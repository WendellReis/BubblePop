import pygame
import globals
from src.ui.debug import Debug

class GameView:
    def __init__(self):
        self.debug = Debug()
        self.fontlarge = pygame.font.SysFont(None,80)
        self.fontsmall = pygame.font.SysFont(None,60)
        self.colors = globals.COLORS
        self.screen_width = 1000
        self.screen_height = 1000
        self.board_width = 700
        self.board_margin = 200

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.load_assets()

        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height)).convert_alpha()
        pygame.display.set_caption('BubbleePop')

        self.cache = {
            "bubblees_in_bag": 20,
            "score": [0,0]
        }

        self.render_text()

    def load_assets(self):
        self.cell_image = pygame.image.load('assets/images/cell.png').convert_alpha()
        self.cell_image.set_alpha(100)
        self.cell_selected_image = pygame.image.load('assets/images/cell.png').convert_alpha()     
        self.cell_invisible_image = pygame.image.load('assets/images/cell.png').convert_alpha()
        self.cell_invisible_image.set_alpha(0)
        
        self.bg_image = pygame.image.load('assets/images/background.png').convert()
        self.bg_image = pygame.transform.scale(self.bg_image,(self.screen_width,self.screen_height)).convert()
        
        self.board_image = pygame.image.load('assets/images/board.png').convert_alpha()
        self.board_image = pygame.transform.scale(self.board_image,(420,self.screen_height)).convert()

        self.back_btn_image = pygame.image.load('assets/images/back_btn.png').convert_alpha()
        self.skip_sky_image = pygame.image.load('assets/images/skip_sky_btn.png').convert_alpha()
        self.skip_sky_image = pygame.transform.scale(self.skip_sky_image,(120,55)).convert_alpha()

        self.bubblees_images = {}
        for c in self.colors:
            img = pygame.image.load(f'assets/images/bubblee_{globals.ASCII[c]}.png').convert_alpha()
            self.bubblees_images[c] = img

        self.power_images = {}
        for c in self.colors:
            if c != 'x':
                img = pygame.image.load(f'assets/images/power_{globals.ASCII[c]}.png').convert_alpha()
                img = pygame.transform.scale(img, (100, 100))
                self.power_images[c] = img

        self.bag_image = pygame.image.load('assets/images/bag.png').convert_alpha()
        self.bag_image = pygame.transform.scale(self.bag_image, (140, 140)).convert_alpha()

        self.accept_icon = pygame.image.load('assets/images/accept.png').convert_alpha()
        self.reject_icon = pygame.image.load('assets/images/reject.png').convert_alpha()

        self.debug_image = pygame.image.load('assets/images/debug.png').convert_alpha()
        self.debug_image = pygame.transform.scale(self.debug_image,(60,60))

    def render_text(self):
        self.rendered_text = {
            "bubblees_in_bag": self.fontsmall.render(str(self.cache["bubblees_in_bag"]), True, (255, 255, 255)),
            "score":[
                self.fontlarge.render(str(self.cache["score"][0]), True, (0, 0, 0)),
                self.fontlarge.render(str(self.cache["score"][1]), True, (0, 0, 0))
            ]
        }

    def draw(self,game):
        self.screen.blit(self.bg_image,(0,0))
        self.screen.blit(self.board_image,(200,0))
        board = game.get_board()
        self.draw_sky(board.get_sky())
        self.draw_planet(board.get_planet())
        self.draw_score(game.get_score())
        self.draw_bag(board.get_bubblees_in_bag(),board.get_bag_color())
        self.draw_buttons(game)
        self.draw_powers(game)
        self.debug.draw(self.screen,game)
        pygame.display.update()


    def draw_powers(self,game):
        current_state = game.get_current_state()
        if len(game.get_power_stack()) > 0:
            powers = game.get_power_stack()[-1][1]

            if len(powers) == 0:
                return
            
            buttons = game.get_power_buttons()
            for i in range(len(powers)):
                x,y = buttons[i].get('accept').get('pos')
                self.screen.blit(self.power_images[powers[i]],(x+2,y-110))

            if current_state == globals.STATE_CHOOSE_POWER:
                for i in range(len(powers)):
                    b_accept = buttons[i].get('accept')
                    b_reject = buttons[i].get('reject')
                    self.screen.blit(self.accept_icon,b_accept.get('pos'))
                    self.screen.blit(self.reject_icon,b_reject.get('pos'))


    def draw_score(self,score):
        self.cache["score"] = score
        self.render_text()

        self.screen.blit(self.rendered_text["score"][0],(90,80))
        self.screen.blit(self.rendered_text["score"][1],(90,880))

    def draw_bag(self,value,color):
        if value != self.cache["bubblees_in_bag"]:
            self.cache["bubblees_in_bag"] = value
            self.render_text()

        if color in self.colors:
            self.screen.blit(self.bubblees_images[color],(680,780))

        self.screen.blit(self.bag_image,(700,800))
        self.screen.blit(self.rendered_text["bubblees_in_bag"],(750,850))

    def draw_cell(self,cell,transparence=False):
        if transparence:
            self.screen.blit(self.cell_invisible_image,cell.get_pos())
        elif cell.is_selected():
            self.screen.blit(self.cell_selected_image,cell.get_pos())
        else:
            self.screen.blit(self.cell_image,cell.get_pos())
        self.draw_bubblee(cell)

    def draw_sky(self,sky):
        matriz = sky.get_matriz()
        for j in range(0,5):
            c1 = matriz[0][j]
            c2 = matriz[1][j]
            self.draw_cell(c1)
            self.draw_cell(c2)
            
    def draw_planet(self,planet):
        transparence = False
        for i in range(0,6):
            if i >= 4:
                transparence = True
            for j in range(0,5):
                c1 = planet[0].matriz[i][j]
                c2 = planet[1].matriz[i][j]
                self.draw_cell(c1,transparence)
                self.draw_cell(c2,transparence)

  
    def draw_bubblee(self,cell):
        color = cell.get_color()
        if color in self.colors:
            x,y = cell.get_pos()
            self.screen.blit(self.bubblees_images[color],(x+4,y+4))

    def draw_buttons(self,game):
        if game.get_current_state() == globals.STATE_SWAP_BUBBLEES:
            skip_btn = game.get_skip_btn()
            self.screen.blit(self.skip_sky_image,skip_btn["pos"])
        
    
        back_btn = game.get_back_btn()
        self.screen.blit(self.back_btn_image,back_btn["pos"])
        

        self.screen.blit(self.debug_image,(650,900))