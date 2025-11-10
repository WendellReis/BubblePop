from src.game.cell import Cell
import globals

class Planet:
    def __init__(self,top = False):
        self.matriz = []
        for i in range(0,6):
            self.matriz.append([])
            for j in range(0,5):
                if top:
                    self.matriz[i].append(Cell((177 + 36 + 80*j,80*i + 20)))
                else:
                    self.matriz[i].append(Cell((177 + 36 + 80*j,1000 - 80*i - 97)))

    def set_planet(self,matriz):
        for i in range(0,6):
            for j in range(0,5):
                self.matriz[i][j].set_color(matriz[i][j])

    def get_color_matriz(self):
        m = []
        for i in range(0,6):
            m.append([])
            for j in range(0,5):
                m[i].append(self.matriz[i][j].get_color())
        return m
    
    def get_cell_click(self,event):
        for i in range(0,4):
            for j in range(0,5):
                if self.matriz[i][j].rect.collidepoint(event.pos):
                    return [i,j]
        return None
    
    def get_cell_color(self,cell):
        return self.matriz[cell[0]][cell[1]].get_color()
    
    def select_all(self,op=1):
        if op == 1:
            for i in range(0,6):
                for j in range(0,5):
                    if self.matriz[i][j].get_color() in globals.COLORS:
                        self.matriz[i][j].select()

        else:
            for i in range(0,6):
                for j in range(0,5):
                    if self.matriz[i][j].get_color() in globals.COLORS:
                        self.matriz[i][j].deselect()

    def is_free_bubble(self,pos):
        i,j = pos

        if self.matriz[i][j].get_color() not in globals.COLORS:
            return False

        i+=1
        while i < 6:
            if self.matriz[i][j].get_color() in globals.COLORS:
                return False
            i+=1
        return True

