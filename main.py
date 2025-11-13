import pygame
from src.game.game import Game
from src.ui.gameview import GameView
from src.ui.GameStateTreeViewer import GameStateTreeViewer

if __name__ == '__main__':
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

            # mostra grafo ao pressionar G
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                if hasattr(game, "tree"):
                    GameStateTreeViewer.show(game.tree)

            game.update(event)

            if game.get_dirty():
                view.draw(game)
                game.set_dirty(False)

        clock.tick(60)

    pygame.quit()
