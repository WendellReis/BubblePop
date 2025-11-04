import pygame
from src.game.game import Game
from src.ui.gameview import GameView
from src.utils.gamestatemanager import GameStateManager

if __name__ == '__main__':
    game = Game(seed=1234)
    manager = GameStateManager()
    pygame.init()
    pygame.mixer.quit()
    view = GameView()
    clock = pygame.time.Clock()
    running = True
    
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN])
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            else:
                game.update(event)
                view.draw(game)
        clock.tick(60)
    pygame.quit()