
class Entity_manager:
    def __init__(self):
        self.entites = []

    def add(self, entity):
        self.entites.append(entity)

    def update(self):
        for entity1 in self.entites:
            for entity2 in self.entites:
                if (entity1 != entity2):
                    if(entity1.active and entity2.active):
                        if(entity1.check_collision(entity2)):
                            entity1.collision(entity2)

    def render(self, display):
        for entity in self.entites:
            display.blit(entity.model, entity.model_rect)

    def return_bomb_coords(self):
        coords = []
        for a in self.entites:
            if (a.group_id == 2):
                coords.append((a.x,a.y))
        return coords

    def reset(self):
        self.entites.clear()
