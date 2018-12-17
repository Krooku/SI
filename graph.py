
class graph:
    def __init__(self, map):
        self.barriers = map.return_bushes_coords()
        self.height = map.map_height
        self.width = map.map_width

    def heuristic(self, start, goal):
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return dx + dy

    def get_vertex_neighbours(self, pos):
        n = []
        x = pos[0]
        y = pos[1]
        z = pos[2]  #zwrot

        if(z == 0 and y < self.height):    #south
            n.append((x,y+1,z))
        elif(z == 1 and x < self.width):  #east
            n.append((x+1, y, z))
        elif(z == 2 and y > 0):  #north
            n.append((x, y-1, z))
        elif(z == 3 and x > 0):  #west
            n.append((x-1, y, z))
        n.append((x, y, (z+1)%4))
        n.append((x, y, (z-1)%4))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if ((b[0],b[1]) == barrier ):
                return 100
        return 1
