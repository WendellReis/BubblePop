import pygame
import copy
from src.game.game import Game
from src.ui.gameview import GameView
import src.utils.sucessor as sucessor
from src.utils.GameStateTree import GameStateTree
import src.utils.action as action


if __name__ == '__main__':
    show_graph = True
    game = Game(seed=1234)

    pygame.init()
    pygame.mixer.quit()
    view = GameView()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            game.update(event)
            if game.get_dirty():
                view.draw(game)
                game.set_dirty(False)

        clock.tick(60)

    pygame.quit()
