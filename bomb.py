import pygame
import entity
import random
import neuralnetwork


class Bomb(entity.Entity):
    def __init__(self, x, y, file_name, level, neuralnet):
        super(entity.Entity, self).__init__()
        self.photo = 'images/dataset/random_bomb/r ('+str(random.randint(1,6))+').jpg'
        self.neuralnet = neuralnet
        self.x = x
        self.y = y

        self.active = True

        self.group_id = 2

        self.load(file_name)
        self.model_rect = self.model.get_rect()
        self.model_rect.x = self.x * level.width
        self.model_rect.y = self.y * level.width

    def defuse(self):
        if(self.active):
            if(self.neuralnet.recognize(self.photo)==True):
                self.load("bombarozbrojona.gif")
                self.active = False
            else:
                self.load("bombazle.gif")

    def collision(self, entity):
        if(entity.group_id == 4):
            print("xd")

