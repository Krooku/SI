import pygame
import entity
import random
import neuralnetwork


class Trash(entity.Entity):
    def __init__(self, x, y, file_name, level, neuralnet):
        super(entity.Entity, self).__init__()
        self.photo = 'images/dataset/random_trash/r ('+str(random.randint(1,7))+').jpg'
        self.neuralnet = neuralnet
        self.x = x
        self.y = y
        self.active = False

        self.group_id = 3

        self.load(file_name)
        self.model_rect = self.model.get_rect()
        self.model_rect.x = self.x * level.width
        self.model_rect.y = self.y * level.width

    def defuse(self):
        if(self.active):
            if(self.neuralnet.recognize(self.photo)==False):
                self.load("smiec.gif")
                self.active = False
            else:
                self.load("bombazle.gif")

    def collision(self, entity):
        if(entity.group_id == 1):
            print("xd")
            self.defuse()

