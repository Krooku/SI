import pygame
import entity
import graph


class Saper(entity.Entity):
    def __init__(self, x, y, direction, file_name, level, entity_manager):
        super(entity.Entity, self).__init__()

        self.kol = 0

        self.points_to_visit = []


        self.entity_manager = entity_manager
        self.simulation = False

        self.state = 0 #0nothing, 1 A*, 2 genetic
        self.level = level
        self.stepcount = 0

        self.x = x
        self.y = y
        self.direction = direction

        self.group_id = 1

        self.load(file_name)
        self.model_rect = self.model.get_rect()
        self.model_rect.x = self.x * level.width
        self.model_rect.y = self.y * level.width

        self.bomb_coords = []
        self.bomb_coords = entity_manager.return_bomb_coords()
        self.graph = graph.graph(level)

        self.instructionstep = 0 #numer kroku dla znalezienia kazdej bomby
        self.result = []
        self.max_moves = 150
        self.moves = 0
        self.bombs_left = 0
        for bomb in self.bomb_coords:
            self.bombs_left += 1


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
        if (self.direction == 0): #south
            if (level.data[self.y + 1][self.x] != "0"):
                return True
            else:
                return False
        elif (self.direction == 1): #east
            if (level.data[self.y][self.x + 1] != "0"):
                return True
            else:
                return False
        elif (self.direction == 2): #north
            if (level.data[self.y - 1][self.x] != "0"):
                return True
            else:
                return False
        elif (self.direction == 3): #west
            if (level.data[self.y][self.x - 1] != "0"):
                return True
            else:
                return False

    def collision(self, entity):
        if(entity.group_id == 2):
            entity.defuse()
            self.bombs_left -= 1
            print(entity.time)
            entity.group_id = 3

    def move(self, level):
        if not (self.level_collision(level)):
            if (self.direction == 0):
                self.model_rect.y += level.width
                self.y += 1
            elif (self.direction == 1):
                self.model_rect.x += level.width
                self.x += 1
            elif (self.direction == 2):
                self.model_rect.y -= level.width
                self.y -= 1
            elif (self.direction == 3):
                self.model_rect.x -= level.width
                self.x -= 1
            self.stepcount += 1
        else:
            print(self.level_collision(level))

    def goaltest(self, pos, end):
        if (pos[0] == end[0] and pos[1] == end[1]):
            return True
        return False

    def AStarSearch(self, end):
        G = {}  # Actual movement cost to each position from the start position
        F = {}  # Estimated movement cost of start to end going via this position

        # Initialize starting values
        graph = self.graph
        start = (self.x, self.y, self.direction)
        G[start] = 0
        F[start] = graph.heuristic(start, end)
        explored = set()
        openVertices = set([start])
        prev = {} #poprzednia pozycja

        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            position = None #obecna pozycja
            currentFscore = None
            for pos in openVertices:
                if position is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    position = pos

            # Check if we have reached the goal
            if (self.goaltest(position, end)):
                # Retrace our route backward
                path = [position]
                endpos = position
                while position in prev:
                    position = prev[position]
                    path.append(position)
                path.reverse()
                return path, F[endpos]  # Done!

            # Mark the current vertex as closed
            openVertices.remove(position)
            explored.add(position)

            # Update scores for vertices near the current position
            for neighbour in graph.get_vertex_neighbours(position):
                if neighbour in explored:
                    continue  # We have already processed this node exhaustively
                candidateG = G[position] + graph.move_cost(position, neighbour)

                if neighbour not in openVertices:
                    openVertices.add(neighbour)  # Discovered a new vertex
                elif candidateG >= G[neighbour]:
                    continue  # This G score is worse than previously found

                # Adopt this G score
                prev[neighbour] = position
                G[neighbour] = candidateG
                H = graph.heuristic(neighbour, end)
                F[neighbour] = G[neighbour] + H

        raise RuntimeError("A* failed to find a solution")

    def go(self,pos):
        #go to pos
        dir = self.direction
        z = pos[2]
        if(dir == z):
            if ((self.direction == 0 and pos[1] == self.y+1) or (self.direction == 1 and pos[0] == self.x+1) or (self.direction == 2 and pos[1] == self.y-1) or (self.direction == 3 and pos[0] == self.x-1)):
                self.move(self.level)
                self.moves += 1
                self.max_moves -= 1
                for entity in self.entity_manager.entites:
                    if entity.group_id == 2:
                        entity.time -= 0.4
        elif((dir == 3 and z == 2) or (dir == 2 and z == 1) or (dir == 1 and z == 0) or (dir == 0 and z ==3)):
            self.change_direction(1)
        elif((dir == 3 and z == 0) or (dir == 2 and z == 3) or (dir == 1 and z == 2) or (dir == 0 and z == 1)):
            self.change_direction(2)

    '''def search(self,level):
        if(self.bombs_left >= 0): #jesli sa bomby do szukania
            if(len(self.result) > self.instructionstep):    #jesli sa kroki do wykonania
                print("pos:", self.x, self.y, self.direction, "===> ", self.result[self.instructionstep])
                #print(self.result)
                self.go(self.result[self.instructionstep], level)  # idz w najblizsze miejsce prowadzace do bomby
                self.instructionstep += 1
            else:                   #brak krokow do wykonania
                self.result, self.cost = self.AStarSearch(self.bomb_coords[self.bombs_left-1]) #wyznacz droge do bomby
                self.bombs_left -= 1
                self.instructionstep = 0
                print ("koszt przejscia do kolejnej bomby: ", self.cost)'''

    def search(self,level):#edited
        if(self.bombs_left >= 0): #jesli sa bomby do szukania
            if(len(self.result) > self.instructionstep):    #jesli sa kroki do wykonania
                #print("pos:", self.x, self.y, self.direction, "===> ", self.result[self.instructionstep])
                #print(self.result)
                self.go(self.result[self.instructionstep])  # idz w najblizsze miejsce prowadzace do bomby
                self.instructionstep += 1
            else:                   #brak krokow do wykonania
                if(self.bombs_left != 0):
                    self.result, self.cost = self.order_search(self.bombs_left)
                    #self.bombs_left -= 1
                    self.instructionstep = 0
                    print("koszt przejscia do kolejnej bomby: ", self.cost)
                else:
                    print(self.moves)
                    self.state = 0

    def order_search(self, bombs):
        bombs = bombs
        costs = []
        results = []

        for i in range(bombs):
            result, cost = self.AStarSearch(self.bomb_coords[i])
            results.append(result)
            costs.append(cost)

        j = self.find_min(costs)
        del self.bomb_coords[j]

        return results[j], costs[j]


    def find_min(self, costs):
        first = True
        cost = 0
        min = 0
        j = 0
        for i in costs:
            if i < cost and first == False:
                min = j
                cost = i
            elif first:
                min = j
                cost = i
                first = False
            j += 1
        return min


    def get_moves(self):
        return self.moves

    def get_max_moves(self):
        return self.max_moves

    def simulate_action(self, function_name, *args, **kwargs):
        """
        this method simulates behaviour of any of the LogicEngine methods without actually executing them in the game
        :param function_name:
        :param args:
        :param kwargs:
        :return: simulated game state
        """
        simulated_logic_engine = self.entity_manager
        #simulated_logic_engine.entities[5].simulation = True
        method_to_call = getattr(simulated_logic_engine.entites[5], function_name)
        method_to_call(*args, **kwargs)



        simulated_logic_engine.update()


        return simulated_logic_engine

    def simulate_move(self, dx=0, dy=0):
        """ simulates player's move by +-dx, +-dy coordinates """
        #self.model_rect.x +=  32
        #self.model_rect.y +=  32
        return self.simulate_action('go1', dx, dy)

    def simulate_move_absolute_coordinate(self,  save_simulated_state_JSON = False, x=0, y=0):
        """ simulates player's move onto absolute dx, dy coordinates """
        #self.model_rect.x += 32
        #self.model_rect.y +=  32
        return self.simulate_action('go1', x, y)

    def bombs_time(self):
        total_time = 0
        for entity in self.entity_manager.entites:
            if entity.group_id == 2:
                total_time += entity.time
        return total_time



    def go1(self, x, y):#edited
        if(len(self.result) > self.instructionstep):    #jesli sa kroki do wykonania
            self.go(self.result[self.instructionstep])  # idz w najblizsze miejsce prowadzace do bomby
            self.instructionstep += 1

        else:                   #brak krokow do wykonania
            if(self.bombs_left != 0):
                self.result, self.cost = self.AStarSearch((x, y))
                self.bombs_left -= 1
                self.instructionstep = 0


    def search3(self,hof):
        if(self.kol < len(hof)): #jesli sa bomby do szukania0
            if(len(self.result) > self.instructionstep):    #jesli sa kroki do wykonania
                #print(self.result)
                self.go(self.result[self.instructionstep])  # idz w najblizsze miejsce prowadzace do bomby
                self.instructionstep += 1
            else:
                self.result.clear()
                if(self.entity_manager.entites[hof[self.kol]].group_id == 2):                   #brak krokow do wykonania
                    self.result, self.cost = self.AStarSearch(self.bomb_coords[hof[self.kol]]) #wyznacz droge do bomby
                self.bombs_left -= 1
                self.kol += 1
                self.instructionstep = 0

