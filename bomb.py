import pygame
import entity


class Bomb(entity.Entity):
    def __init__(self, x, y, file_name, level):
        super(entity.Entity, self).__init__()

        self.x = x
        self.y = y

        self.group_id = 2

        self.load(file_name)
        self.model_rect = self.model.get_rect()
        self.model_rect.x = self.x * level.width
        self.model_rect.y = self.y * level.width

    def defuse(self):
        self.load("bombarozbrojona.gif")

    def collision(self, entity):
        if(entity.group_id == 4):
            print("xd")

