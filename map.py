import pygame


class Map:
    def __init__(self, width):
        self.data = []
        self.width = width
        self.bombs = 5
        self.bushes = []
        self.map_width = 0
        self.map_height = 0

    def load_map(self, file_name):
        f = open("maps/" + file_name).read()
        self.data = [y.split() for y in f.split('\n')]
        for a in self.data:
            self.map_height += 1
            for b in a:
                self.map_width += 1
        return self.data

    def draw_element(self, x, y, file_name, display):
        model = pygame.image.load("images/" + file_name)
        rect = pygame.Rect(x * self.width, y * self.width, self.width, self.width)
        display.blit(model, rect)

    def draw_map(self, display):
        posx = 0
        for a in self.data:
            posy = 0
            for b in a:
                if (b == "0"):
                    self.draw_element(posy, posx, "sand.png", display)
                elif (b == "1"):
                    self.draw_element(posy, posx, "wall.png", display)
                elif (b == "2"):
                    self.draw_element(posy, posx, "wall_r1.png", display)
                elif (b == "3"):
                    self.draw_element(posy, posx, "wall_pu.png", display)
                elif (b == "4"):
                    self.draw_element(posy, posx, "wall_r2.png", display)
                elif (b == "5"):
                    self.draw_element(posy, posx, "wall_pl.png", display)
                elif (b == "6"):
                    self.draw_element(posy, posx, "wall_r4.png", display)
                elif (b == "7"):
                    self.draw_element(posy, posx, "wall_pd.png", display)
                elif (b == "8"):
                    self.draw_element(posy, posx, "wall_r3.png", display)
                elif (b == "9"):
                    self.draw_element(posy, posx, "wall_pr.png", display)
                elif (b == "b"):
                    self.draw_element(posy, posx, "bush1.png", display)
                elif (b == "c"):
                    self.draw_element(posy, posx, "bush2.png", display)
                posy += 1
            posx += 1

    def return_bushes_coords(self):
        y = 0
        for a in self.data:
            x = 0
            for b in a:
                if (b == "b" or b == "c"):
                    self.bushes.append((x, y))
                x += 1
            y += 1
        return self.bushes
