from src.game.cell import Cell

class Planet:
    def __init__(self,top = False):
        self.matriz = []
        for i in range(0,6):
            self.matriz.append([])
            for j in range(0,5):
                if top:
                    self.matriz[i].append(Cell((177 + 39 + 130*j,110*i + 20)))
                else:
                    self.matriz[i].append(Cell((177 + 39 + 130*j,1600 - 110*i - 120)))

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