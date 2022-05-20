from dataclasses import dataclass
import pygame, pytmx, pyscroll


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]

class MapManager:
    def __init__(self, screen, player):
        self.walls = None
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "House_1UP"

        self.register_map("Bourg_Jaajette", portals=[
            Portal(from_world="Bourg_Jaajette", origin_point="enter_house", target_world="House_1", teleport_point="spawn_house"),
            Portal(from_world="Bourg_Jaajette", origin_point="enter_routin", target_world="Routin", teleport_point="spawn_routin"),
            Portal(from_world="Bourg_Jaajette", origin_point="enter_armory", target_world="Armory", teleport_point="spawn_armory"),
            Portal(from_world="Bourg_Jaajette", origin_point="enter_dojo", target_world="Dojo", teleport_point="enter_dojo_player")
        ])
        self.register_map("Routin", portals=[
            Portal(from_world="Routin", origin_point="exit_routin", target_world="Bourg_Jaajette", teleport_point="enter_routin_exit")
        ])
        self.register_map("House_1", portals=[
            Portal(from_world="House_1", origin_point="exit_house", target_world="Bourg_Jaajette", teleport_point="enter_house_exit"),
            Portal(from_world="House_1", origin_point="enter_house_up", target_world="House_1UP", teleport_point="spawn_house_up")
        ])
        self.register_map("House_1UP", portals=[
            Portal(from_world="House_1UP", origin_point="exit_house_up", target_world="House_1", teleport_point="exit_house_up")
        ])
        self.register_map("Armory", portals=[
            Portal(from_world="Armory", origin_point="armory_exit", target_world="Bourg_Jaajette", teleport_point="enter_armory_exit")
        ])
        self.register_map("Dojo", portals=[
            Portal(from_world="Dojo", origin_point="exit_dojo", target_world="Bourg_Jaajette", teleport_point="exit_dojo_player")
        ])

        self.teleport_player('player')

    def check_collisions(self):
        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_objets(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)


        #collision avec les murs
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_objets(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[]):
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

        # Creer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_objets(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()
