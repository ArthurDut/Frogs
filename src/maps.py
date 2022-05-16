from dataclasses import dataclass
import pygame, pytmx, pyscroll


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap

class MapManager:
    def __init__(self, screen, player):
        self.walls = None
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "Bourg_Jaajette"

        self.register_map("Bourg_Jaajette")
        self.register_map("Routin")
        self.register_map("House_1")
        self.register_map("House_1UP")

        self.teleport_player('player')

    def check_collisions(self):
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_objets(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name):
        # importation de la carte
        tmx_data = pytmx.util_pygame.load_pygame(f'Maps/{name}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3


        # Définition table des collisions
        walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # utilisation des calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        group.add(self.player)

        #Creer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_objets(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
