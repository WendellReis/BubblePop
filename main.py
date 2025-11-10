import pygame
from src.game.game import Game
from src.ui.gameview import GameView
import src.utils.sucessor as sucessor
from src.utils.gamestatemanager import GameStateManager

if __name__ == '__main__':
    game = Game(seed=1234)
    manager = GameStateManager()
    pygame.init()
    pygame.mixer.quit()
    view = GameView()
    clock = pygame.time.Clock()
    running = True
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            else:
                if game.get_dirty():
                    print(sucessor.GET(game.get_state()))
                    view.draw(game)
                    game.set_dirty(False)   
                game.update(event) 
        clock.tick(60)
    pygame.quit()