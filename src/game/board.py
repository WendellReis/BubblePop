import random
from src.game.sky import Sky
from src.game.planet import Planet
import globals

class Board:
    def __init__(self,bubblees_in_bag,set_sky=True,sky=None):
        self.colors = globals.COLORS
        self.bubblees_in_bag = bubblees_in_bag
        self.bag_color = None

        self.planet = [Planet(True),Planet()]

        self.sky = Sky()
        if set_sky:
            self.sky.generate_sky()
        else:
            self.set_sky(sky)
    
    def get_sky(self):
        return self.sky

    def get_planet(self,id=None):
        if id is None:
            return self.planet
        elif id in [0,1]:
            return self.planet[id]
        return None
    
    def get_planet_color_matriz(self,id=None): 
        if id in [0,1]:
            return self.planet[id].get_color_matriz()
        return None
    
    def get_bubblees_in_bag(self):
        return self.bubblees_in_bag
    
    def get_bag_color(self):
        return self.bag_color

    def set_planet(self,id,matriz):
        if id not in [0,1]:
            return
        self.planet[id].set_planet(matriz)

    def set_sky(self,matriz):
        self.sky.set_sky(matriz)

    def generate_bag_bubblee(self):
        if self.bag_color is None and self.bubblees_in_bag > 0:
            self.bag_color = self.colors[random.randint(0,len(self.colors)-1)]
            self.bubblees_in_bag-=1

    def verify_setup_sky(self):
        return self.bubblees_in_bag >= self.sky.count_empty()
    
    def select_sky_cell(self,cell):
        self.sky[cell[0]][cell[1]].select()

    def deselect_sky_cell(self,cell):
        self.sky[cell[0]][cell[1]].deselect()
    
    def get_sky_click(self,event,empty=False):
        cell = self.sky.get_click(event.pos)
        if cell is None:
            return None
        
        matriz = self.sky.get_matriz()
        if empty and matriz[cell[0]][cell[1]].get_color() not in globals.COLORS:
            return cell
        if not empty and matriz[cell[0]][cell[1]] not in globals.COLORS:
            return cell
        
        return None
    
    def is_full_sky(self):
        return self.sky.count_empty() == 0
        
    def get_sky_color_matriz(self):
        return self.sky.get_color_matriz()
    
    def set_bubblees_in_bag(self,value):
        if value >= 0:
            self.bubblees_in_bag = value
