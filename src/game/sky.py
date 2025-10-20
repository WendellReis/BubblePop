import random
import globals
from src.game.cell import Cell

class Sky:
    def __init__(self):
        self.colors = globals.COLORS
        self.matriz = [[],[]]
        for j in range(0,5):
            self.matriz[0].append(Cell((177 + 39 + 130*j,int(1600/2) - 106)))
            self.matriz[1].append(Cell((177 + 39 + 130*j,int(1600/2) + 14 )))

    def get_matriz(self):
        return self.matriz

    def generate_sky(self):
        for j in range(0,5):
            c1 = self.colors[random.randint(0,len(self.colors)-1)]
            c2 = self.colors[random.randint(0,len(self.colors)-1)]
            self.matriz[0][j].set_color(c1)
            self.matriz[1][j].set_color(c2)

    def set_sky(self,matriz):
        for j in range(0,5):
            self.matriz[0][j].set_color(matriz[0][j])
            self.matriz[1][j].set_color(matriz[1][j])

    def count_empty(self):
        count = 0
        for j in range(0,5):
            if self.matriz[0][j].get_color() not in globals.COLORS:
                count+=1
            if self.matriz[1][j].get_color() not in globals.COLORS:
                count+=1
        return count
    
    def get_click(self,click):
        for j in range(0,5):
            if self.matriz[0][j].collide(click):
                return [0,j]
            elif self.matriz[1][j].collide(click):
                return [1,j]
        return None
    
    def get_color_matriz(self):
        m = [[],[]]
        for j in range(0,5):
            m[0].append(self.matriz[0][j].get_color())
            m[1].append(self.matriz[1][j].get_color())
        return m