from dataclasses import dataclass
import pygame, pytmx, pyscroll

from src.player import NPC



@dataclass
class Portal:
    from_world:  str
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
    npcs: list[NPC]

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
        ], npcs=[
            NPC("villager", nb_points=4, dialog1=["J'ai perdu les clés de ma maison", "Je suis enfermé dehors !"], dialog2=["", ""]),
            NPC("boy", nb_points=2, dialog1=["C'est enfin le jour de la fête du dieu Grenouille !", "J'attendais ça depuis si longtemps"], dialog2=["", ""]),
            NPC("old_woman", nb_points=1, dialog1=["Mon fils s'est noyé ici il y a quelques années", "Mais le dieu Grenouille veille sur lui désormais"], dialog2=["", ""])
        ])
        self.register_map("Routin", portals=[
            Portal(from_world="Routin", origin_point="exit_routin", target_world="Bourg_Jaajette", teleport_point="enter_routin_exit")
        ], npcs=[
            NPC("Krillin", nb_points=2, dialog1=["Kienzan !", "J'ai peur d'encore mourrir face a ces monstres..."], dialog2=["", ""]),
            NPC("monk_1", nb_points=1, dialog1=["Merci de m'avoir sauvé de tous ces affreux "], dialog2=["monstres"])
        ])
        self.register_map("House_1", portals=[
            Portal(from_world="House_1", origin_point="exit_house", target_world="Bourg_Jaajette", teleport_point="enter_house_exit"),
            Portal(from_world="House_1", origin_point="enter_house_up", target_world="House_1UP", teleport_point="spawn_house_up")
        ], npcs=[
            NPC("giovanni", nb_points=1, dialog1=["Tu es maintenant assez grand pour découvrir le ", "Va voir le dieu Grenouille et reçois sa bénédiction"]
                , dialog2=["monde par toi même", ""])
        ])
        self.register_map("House_1UP", portals=[
            Portal(from_world="House_1UP", origin_point="exit_house_up", target_world="House_1", teleport_point="exit_house_up")
        ])
        self.register_map("Armory", portals=[
            Portal(from_world="Armory", origin_point="armory_exit", target_world="Bourg_Jaajette", teleport_point="enter_armory_exit")
        ], npcs=[
            NPC("armor_man", nb_points=1, dialog1=["Tu as besoin d'une arme ?", "J'ai ce qu'il te faut, prends cette épée oubliée par "],
                dialog2=["", "un ancien chevalier"])
        ])

        self.register_map("Dojo", portals=[
            Portal(from_world="Dojo", origin_point="exit_dojo", target_world="Bourg_Jaajette", teleport_point="exit_dojo_player")
        ], npcs=[
            NPC("dojo_master", nb_points=1, dialog1=["La Grenouille maléfique est bien trop déroce pour ", 'Tu dois recevoir mon entrainement afin de devenir ', "Voilà ! Tu peux maintenant aller affronter cette "],
                dialog2=["toi", "plus puissant", "maudite Grenouille !"])
        ])

        self.teleport_player('player')
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
             if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                 dialog_box.execute(sprite.dialog1, sprite.dialog2)

    def check_collisions(self):
        #portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)


        #collision avec les murs
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
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

        # récupérer tous les NPC pour les ajouter au groupe

        for npc in npcs:
            group.add(npc)

        # Creer un objet Map
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()



