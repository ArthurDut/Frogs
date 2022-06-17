import pygame
import pytmx
import pyscroll
from player import Player
from src.dialog import DialogBox
from src.maps import MapManager



class Game:

    def __init__(self):
        # Fenêtre du jeu
        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Frog's Quest")

        # Génération du joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox()

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()

        # Boucle de la fenêtre
        running = True

        while running:
            self.map_manager.draw()
            self.player.save_location()
            self.handle_input()
            self.update()
            self.dialog_box.render(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                    elif event.key == pygame.K_k:
                        self.map_manager.check_monster_collision(self)

            clock.tick(60)

        pygame.quit()
