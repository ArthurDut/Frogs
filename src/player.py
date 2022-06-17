import pygame

from src.animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        """
            Constructeur de la classe Entity
        :param name: Nom du sprite
        :type name: str
        :param x: coordonnée x
        :type x: int
        :param y: coordonnée y
        :type y: int
        """
        super().__init__(name)
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 14)
        self.old_position = self.position.copy()

    def save_location(self):
        """
            Fonction qui sauvegarde la position du joueur
        """
        self.old_position = self.position.copy()

    def move_right(self):
        """
            Fonction qui permet de se déplacer a droite
        """
        self.change_animation("right")
        self.position[0] += self.speed

    def move_left(self):
        """
            Fonction qui permet de se déplacer a gauche
        """
        self.change_animation("left")
        self.position[0] -= self.speed

    def move_up(self):
        """
            Fonction qui permet de se déplacer en haut
        """
        self.change_animation("up")
        self.position[1] -= self.speed

    def move_down(self):
        """
            Fonction qui permet de se déplacer en bas
        """
        self.change_animation("down")
        self.position[1] += self.speed

    def update(self):
        """
            Fonction qui vérifie la position de l'entité
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """
            Fonction qui téléporte le joueur en arrière en cas de collision
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):
    def __init__(self):
        """
            Constructeur de la classe Player
        """
        super().__init__("player", 0, 0)


class NPC(Entity):

    def __init__(self, name, nb_points, dialog1, dialog2):
        """
            Constructeur de la classe NPC
        :param name: nom du sprite
        :type name: str
        :param nb_points: Points définis sur Tiled
        :type nb_points: int
        :param dialog1: Dialogue entré dans MapManager
        :type dialog1: str
        :param dialog2: Dialogue entré dans MapManager
        :type dialog2: str
        """
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.points = []
        self.dialog1 = dialog1
        self.dialog2 = dialog2
        self.name = name
        self.speed = 0.7
        self.current_point = 0

    def move(self):
        """
            Fonction qui vérifie les conditions de mouvement des NPC
        """
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        """
            Focntion qui place les NPC aux bons endroits
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        """
            Fonction qui permet de récupérer de Tiled les points de déplacement des NPC
        :param tmx_data: Récupère le chemin dans Tiled
        :type tmx_data: basestring
        """
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)


class Monsters(Entity):

    def __init__(self, name, nb_points):
        """
            Constructeur de la classe Monsters
        :param name: nom du sprite
        :type name: str
        :param nb_points: Points définis sur Tiled
        :type nb_points: int
        """
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0

    def move(self):
        """
            Fonction qui vérifie les conditions de mouvement des Monstres
        """
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        """
            Fonction qui place les Monstres aux bons endroits
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_points(self, tmx_data):
        """
            Fonction qui récupère sur Tiled les points de déplacement des monstres
        :param tmx_data: Récupère le chemin dans Tiled
        :type tmx_data: basestring
        """
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)
