import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self):
        super(pygame.sprite.Sprite, self).__init__()
        self.velocity = (0, 0)
        self.active = True
        self.group_id = 0

    def load(self, filename):
        self.model = pygame.image.load("images/" + filename)

    def check_collision(self, entity):
        #col = pygame.sprite.collide_rect(self.model.rect, entity.model.rect)
        col = self.model_rect.colliderect(entity.model_rect)
        if(col == True):
            return True
        else:
            return False

    def active(self):
        return self.active


