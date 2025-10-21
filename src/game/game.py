import random
import time
import json
import pygame
import src.utils.action as action
import globals
from src.game.board import Board

class Game:
    def __init__(self,seed=time.time()):
        random.seed(seed)

        conf = None
        with open("conf.json", "r") as f:
            conf = json.load(f)

        self.state_handlers = {
            globals.STATE_SETUP_SKY: self.setup_sky,
            globals.STATE_SWAP_BUBBLEES: self.swap_bubblees,
            globals.STATE_DROP_BUBBLEES: self.drop_bubblees,
            globals.STATE_USE_POWER: self.use_power,
            globals.STATE_CHECK_WIN: self.check_win,
            globals.STATE_CHOOSE_POWER: self.choose_power,
            globals.STATE_VERIFY_POWER: self.verify_power,
            globals.STATE_ENDGAME: self.endgame,
            globals.STATE_CHECK_MATCHES: self.check_matches
        }
        
        self.board = Board(conf["bubblees_in_bag"],set_sky=conf["set_sky"],sky=conf["sky"])
        self.current_state = conf["current_state"]
        self.turn = conf["turn"]
        self.board.set_planet(0,conf["planet"][0])
        self.board.set_planet(1,conf["planet"][1])
        self.score = conf["score"]
        self.power_stack = conf["power_stack"]
    
        self.memory = None
        self.history = [self.get_state()]
        self.record_state()
        
        self.load_buttons()

    def get_board(self):
        return self.board
    
    def get_score(self):
        return self.score
    
    def load_buttons(self):
        x,y = (1200,1300)
        self.back_btn = {
            "pos": (x,y),
            "rect": pygame.Rect(x,y,120,120)
        }

        x,y = (1350,1300)
        self.back_2_btn = {
            "pos": (x,y),
            "rect": pygame.Rect(x,y,120,120)
        }

        x,y = (1183,1200)
        self.skip_btn = {
            "pos":(x,y),
            "rect": pygame.Rect(x,y,150,80)
        }

    def get_turn(self):
        return self.turn
    
    def get_current_state(self):
        return self.current_state

    def get_skip_btn(self):
        return self.skip_btn

    def get_back_btn(self):
        return self.back_btn
    
    def get_back_2_btn(self):
        return self.back_2_btn
    
    def record_state(self):
        self.history.append(self.get_state())

    def next_state(self,act,data=None):
        if data is None:
            self.set_state(action.EXECUTE(self.get_state(),act))
        else:
            self.set_state(action.EXECUTE(self.get_state(),act,data))
        self.record_state()

    def get_state(self):
        state = {}
        state["turn"] = self.turn
        state["current_state"] = self.current_state
        state["planet"] = [
            self.board.get_planet_color_matriz(0),
            self.board.get_planet_color_matriz(1)
        ]
        state["sky"] = self.board.get_sky_color_matriz()
        state["score"] = self.score
        state["power_stack"] = self.power_stack
        state["bubblees_in_bag"] = self.board.get_bubblees_in_bag()
        state["bag_color"] = self.board.get_bag_color()
        return state

    def set_state(self,state):
        self.turn = state["turn"]
        self.current_state = state["current_state"]
        self.board.set_planet(0,state["planet"][0])
        self.board.set_planet(1,state["planet"][1])
        self.board.set_sky(state["sky"])
        self.score = state["score"]
        self.power_stack = state["power_stack"]
        self.board.set_bubblees_in_bag(state["bubblees_in_bag"])
        self.board.set_bag_color(state["bag_color"])

    def setup_sky(self,event):
        if self.board.verify_setup_sky():
            if self.board.is_full_sky():
                self.next_state("NAVIGATE",globals.STATE_SWAP_BUBBLEES)
                return
            
            if self.board.get_bag_color() not in globals.COLORS:
                self.next_state("GENERATE_BUBBLEE",self.board.generate_color())
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.memory is None:
                    self.memory = self.board.get_sky_click(event,empty=True)

                    if self.memory is not None:
                        self.next_state("SETUP",self.memory)
                        self.memory = None
        else:
            self.next_state("NAVIGATE",globals.STATE_CHECK_WIN)

    def swap_bubblees(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.memory is None:
                self.memory = self.board.get_sky_click(event)

                if self.memory is not None:
                    self.board.select_sky_cell(self.memory)
            else:
                cell = self.board.get_sky_click(event)
                if cell is not None:
                    if cell == self.memory:
                        self.board.deselect_sky_cell(self.memory)
                        self.memory = None
                    elif self.adj(self.memory,cell):
                        self.next_state("SWAP_BUBBLEES",[self.memory,cell])
                        self.board.deselect_sky_cell(self.memory)
                        self.memory = None
                        
    def drop_bubblees(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.memory is None:
                self.memory = self.board.get_sky_click(event)

                if self.memory is not None:
                    self.board.select_sky_cell(self.memory)
            else:
                cell = self.board.get_sky_click(event)

                if cell is not None:
                    if cell == self.memory:
                        self.board.deselect_sky_cell(self.memory)
                        self.memory = None
                    elif self.adj(self.memory,cell) and (cell[0] == self.turn or self.memory[0] == self.turn):
                        self.next_state("DROP BUBBLEES",[self.memory,cell])
                        self.board.deselect_sky_cell(self.memory)
                        self.memory = None

    def check_matches(self,event):
        pass

    def use_power(self,event):
        pass

    def check_win(self,event):
        pass

    def choose_power(self,event):
        pass

    def verify_power(self,event):
        pass

    def endgame(self,event):
        pass

    def update(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_buttons(event)
        self.state_handlers[self.current_state](event)

    def check_buttons(self,event):
        if self.back_btn["rect"].collidepoint(event.pos) and len(self.history) > 1:
            self.set_state(self.history[-2])
            self.history.pop()
        elif self.back_2_btn["rect"].collidepoint(event.pos) and len(self.history) > 2:
            self.set_state(self.history[-3])
            self.history.pop()
            self.history.pop()
        elif self.current_state == globals.STATE_SWAP_BUBBLEES and self.skip_btn["rect"].collidepoint(event.pos):
            self.next_state("NAVIGATE",globals.STATE_DROP_BUBBLEES)
            if self.memory is not None:
                self.board.deselect_sky_cell(self.memory)
                self.memory = None

    def adj(self,c1,c2):
        if c1[0] == c2[0] and (c1[1] == c2[1]+1 or c2[1] == c1[1]+1):
            return True
        if c1[1] == c2[1] and (c1[0] == c2[0]+1 or c2[0] == c1[0]+1):
            return True
        return False