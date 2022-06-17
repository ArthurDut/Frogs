import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        """
            Constructeur de la classe AnimateSprite
        :param name: nom du sprite
        :type name: str
        """
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'sprites/{name}.png')
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(48),
            'up': self.get_images(16),
        }
        self.speed = 2


    def change_animation(self, name):
        """
            Fonction qui se charge de changer la frame d'animation
        :param name: nom du sprite
        :type name: str
        """
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(0, 0)
        self.clock += self.speed * 12

        if self.clock >= 100:

            self.animation_index += 1

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, x):
        """
            Fonction qui récupère toutes les images et les stocks dans un dictionnaire
        :param x: coordonnée x
        :type x: int
        :return: Liste d'image
        :rtype: list
        """
        images = []

        for i in range(0, 4):
            y = i*16
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self, x, y):
        """
            Fonction qui renvoie l'image a utiliser
        :param x: coordonnée x
        :type x: int
        :param y: coordonnée y
        :type y: int
        :return: Taille de l'image
        :rtype: basestring
        """
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        return image
