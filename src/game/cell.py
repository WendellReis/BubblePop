import pygame

class Cell:
    def __init__(self,pos,color=None):
        self.select
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], 100, 100)
        self.selected = False
        self.color = color

    def deselect(self):
        self.selected = False

    def select(self):
        self.selected = True

    def is_selected(self):
        return self.selected
    
    def get_pos(self):
        return self.pos
    
    def get_color(self):
        return self.color
    
    def set_color(self,color):
        self.color = color

    def collide(self,pos):
        return self.rect.collidepoint(pos)
