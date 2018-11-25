import pygame
import entity


class Saper(entity.Entity):
    def __init__(self, x, y, direction, file_name, level):
        super(entity.Entity, self).__init__()

        self.x = x
        self.y = y
        self.direction = direction

        self.group_id = 1

        self.load(file_name)
        self.model_rect = self.model.get_rect()
        self.model_rect.x = self.x * level.width
        self.model_rect.y = self.y * level.width

    def change_direction(self, x):
        if(x == 1): #obroc sie w prawo
            self.model = pygame.transform.rotate(self.model, -90)
            self.direction = (self.direction - 1) % 4
        elif(x == 2):    #obroc sie w lewo
            self.model = pygame.transform.rotate(self.model, 90)
            self.direction = (self.direction + 1) % 4
        elif(x == 0):   #odwroc sie w tyl
            self.model = pygame.transform.rotate(self.model, 180)
            self.direction = (self.direction + 2) % 4

    def level_collision(self, level):
        if (self.direction == 0):
            if (level.data[self.x + 1][self.y] != "0"):
                return True
            else:
                return False
        elif (self.direction == 1):
            if (level.data[self.x][self.y + 1] != "0"):
                return True
            else:
                return False
        elif (self.direction == 2):
            if (level.data[self.x - 1][self.y] != "0"):
                return True
            else:
                return False
        elif (self.direction == 3):
            if (level.data[self.x][self.y - 1] != "0"):
                return True
            else:
                return False

    def collision(self, entity):
        if(entity.group_id == 2):
            entity.defuse()

    def move(self, level):
        if not (self.level_collision(level)):
            if (self.direction == 0):
                self.model_rect.y += level.width
                self.x += 1
            elif (self.direction == 1):
                self.model_rect.x += level.width
                self.y += 1
            elif (self.direction == 2):
                self.model_rect.y -= level.width
                self.x -= 1
            elif (self.direction == 3):
                self.model_rect.x -= level.width
                self.y -= 1
        else:
            print(self.level_collision(level))
