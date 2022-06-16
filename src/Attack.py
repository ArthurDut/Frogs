import pygame

from src.maps import MapManager
from src.maps import Map
from src.player import Monsters


def delete_monster():
    list[Monsters].remove(0)


class Attaque:

    def __init__(self):
        self.attacking = False
        self.monster = []

    def execute(self):
        if self.attacking:
            delete_monster()
        else:
            self.attacking = True


