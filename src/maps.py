from dataclasses import dataclass
import pygame, pytmx, pyscroll

from src.player import NPC
from src.player import Monsters



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
    monsters: list[Monsters]

class MapManager:
    def __init__(self, screen, player):
        """
        :param screen: Taille de la fenêtre
        :type screen: basestring
        :param player: nom du sprite du player
        :type player: Class
        """
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
            NPC("old_woman", nb_points=1, dialog1=["Mon fils s'est noyé ici il y a quelques années", "Mais le dieu Grenouille veille sur lui désormais"], dialog2=["", ""]),
            NPC("woman", nb_points=1, dialog1=["Le Dieu grenouille est inquiet", "Le démon grenouille s'est réveillé et il a enlevé ", "S'il te plaît, apporte une arme au garde"], dialog2=["","un garde du village",""])
        ])
        self.register_map("Routin", portals=[
            Portal(from_world="Routin", origin_point="exit_routin", target_world="Bourg_Jaajette", teleport_point="enter_routin_exit")
        ], npcs=[
            NPC("Krillin", nb_points=2, dialog1=["Kienzan !", "J'ai peur d'encore mourrir face a ces monstres..."], dialog2=["", ""]),
            NPC("monk_1", nb_points=1, dialog1=["Merci de m'avoir apporté cette arme ", "Grâce a toi je vais pouvoir tuer ces monstres"], dialog2=["",""]),
            NPC("boss", nb_points=1, dialog1=["Tu es venu sauver cet homme ?","Tu espère vraiment qu'il pourra me vaincre ?","Bien va lui donner cette arme"], dialog2=["","",""])
        ], monsters=[
            Monsters('Beast1', nb_points=2),
            Monsters("Beast2", nb_points=1),
            Monsters("Beast3", nb_points=4)
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
            NPC("armor_man", nb_points=1, dialog1=["Le garde a besoin d'une arme ?", "J'ai ce qu'il te faut, prends cette épée oubliée par "],
                dialog2=["", "un ancien chevalier et va la donner au garde sur la Routin"])
        ])

        self.register_map("Dojo", portals=[
            Portal(from_world="Dojo", origin_point="exit_dojo", target_world="Bourg_Jaajette", teleport_point="exit_dojo_player")
        ], npcs=[
            NPC("dojo_master", nb_points=1, dialog1=["La Grenouille maléfique est bien trop déroce pour ", "Le garde t'attends, fonce l'aider ! ", "C'est un bon ami, je m'en voudrais s'il lui arrivait "],
                dialog2=["toi", "", "quelque chose"])
        ])

        self.teleport_player('player')
        self.teleport_npcs()
        self.teleport_mosnters()

    #Collisons pour les dialogues
    def check_npc_collisions(self, dialog_box):
        """
        :param dialog_box: spécification de la boîte de dialogue
        :type dialog_box: Class
        """
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

            if type(sprite) is Monsters:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        """
        :param name: nom de la carte
        :type name: str
        """
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[], monsters=[]):
        """
        :param name: nom de la carte
        :type name: str
        :param portals: liste de portail
        :type portals: list
        :param npcs: liste des NPC
        :type npcs: list
        :param monsters: liste des Monsters
        :type monsters: list
        """
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
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs, monsters)

        for monster in monsters:
            group.add(monster)

    def get_map(self):
        """
        :return: nom de la carte
        :rtype: str
        """
        return self.maps[self.current_map]

    def get_group(self):
        """
        :return: groupe de la carte
        :rtype: str
        """
        return self.get_map().group

    def get_walls(self):
        """
        :return: Murs de la carte
        :rtype: str
        """
        return self.get_map().walls

    def get_object(self, name):
        """
        :param name: nom des objets du calque objet
        :type name: basestring
        :return: Objets appartenant a la carte
        :rtype: basestring
        """
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def teleport_mosnters(self):
        for map in self.maps:
            map_data = self.maps[map]
            monsters = map_data.monsters

            for monster in monsters:
                monster.load_points(map_data.tmx_data)
                monster.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move()

        for monster in self.get_map().monsters:
            monster.move()




"""
    #Collisions pour les attaques
    def check_monster_collision(self, attack):
        for sprite in self.get_group().srpites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is Monsters:
                attack.execute()"""