import pygame
import globals

class GameView:
    def __init__(self):
        self.font100 = pygame.font.SysFont(None,100)
        self.font80 = pygame.font.SysFont(None,80)
        self.colors = globals.COLORS
        self.screen_width = 1600
        self.screen_height = 1600
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
        self.board_image = pygame.image.load('assets/images/board.png').convert_alpha()

        self.bubblees_images = {}
        for c in self.colors:
            img = pygame.image.load(f'assets/images/bubblee_{globals.ASCII[c]}.png').convert_alpha()
            self.bubblees_images[c] = img

        self.power_images = {}
        for c in self.colors:
            if c != 'x':
                img = pygame.image.load(f'assets/images/power_{globals.ASCII[c]}.png').convert_alpha()
                img = pygame.transform.scale(img, (180, 180))
                self.power_images[c] = img

        self.bag_image = pygame.image.load('assets/images/bag.png').convert_alpha()
        self.bag_image = pygame.transform.scale(self.bag_image, (200, 200))

        self.accept_icon = pygame.image.load('assets/images/accept.png').convert_alpha()
        self.reject_icon = pygame.image.load('assets/images/reject.png').convert_alpha()

    def render_text(self):
        self.rendered_text = {
            "bubblees_in_bag": self.font80.render(str(self.cache["bubblees_in_bag"]), True, (255, 255, 255)),
            "score":[
                self.font100.render(str(self.cache["score"][0]), True, (0, 0, 0)),
                self.font100.render(str(self.cache["score"][1]), True, (0, 0, 0))
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
        pygame.display.update()

    def draw_score(self,score):
        if score != self.cache["score"]:
            self.cahce = score
            self.render_text()

        self.screen.blit(self.rendered_text["score"][0],(90,120))
        self.screen.blit(self.rendered_text["score"][0],(90,1400))

    def draw_bag(self,value,color):
        if value != self.cache["bubblees_in_bag"]:
            self.cache["bubblees_in_bag"] = value
            self.render_text()

        if color in self.colors:
            self.screen.blit(self.bubblees_images[color],(880,1150))

        self.screen.blit(self.bag_image,(920,1250))
        self.screen.blit(self.rendered_text["bubblees_in_bag"],(1000,1330))

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
            self.screen.blit(self.bubblees_images[color],(x+6,y+5))