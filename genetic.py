from deap import creator, base, tools, algorithms
import random
import numpy
import multiprocessing


#szansa crossover, szansa mutacji
CXPB, MUTPB = 0.5, 0.2

def set_creator(cr):
    global creator
    creator = cr


set_creator(creator)
#really just cares about others when there is a draw)
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -100.0, 10.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

def set_creator(cr):
    global creator
    creator = cr

def prepare_genetic(entity_manager, level):
    """
    prepares the genetic algorithm using the deap library
    :param LogicEngine:
    :return:
    """
    #1: count of enemies, count of bombs
    #2 : my_own hp count of moves
    #3 : number of enemy hp
    #fitness function that aims to minimize first objective, and maximize the second, minimize the third
    #creator.create("FitnessMulti", base.Fitness, weights=(-100.0, 1.0, -10.0))

    #this registers hall of fame
    hof = tools.HallOfFame(5)
    #creator.create("Individual", list, fitness=creator.FitnessMulti)
    #individual with genes of the form of list, that take previously defined fitness function
    toolbox = base.Toolbox()

    #registers function that generates genes
    max_gene_value = 5#len(LogicEngine.monsters + LogicEngine.mixtures)#ilosc bomb
    toolbox.register("attr_int", random.randrange, 0, max_gene_value,  1)

        #registers how to make an individual
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_int,  entity_manager.entites[5].bombs_left * 3) #len(LogicEngine.monsters + LogicEngine.mixtures) * 3)#ilosc bomb


    #register statistics
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg #1 bombs | #2 moves | time", numpy.mean, axis=0)
    stats.register("std #1 bombs | #2 moves | time", numpy.std, axis=0)
    stats.register("min #1 bombs | #2 moves | time", numpy.min, axis=0)
    stats.register("max #1 bombs | #2 moves | time", numpy.max, axis=0)

    #this registers the way to select from population to crossover
    #tournament selection, choose random from population, run tournaments based on fitness score, winner goes through
    # tak naprawdę probabilistycznie wybiera: wybierz z szansą #1 że najlepszy wygra
    # wybierz z szansą mniejszą że drugi wygra..
    # słabsi przechodzą i jest diversity bo tournament size jest ograniczony, to znaczy że może być np
    # 15 najsłabszych wybranych, i 15- najsłabszy wtedy przejdzie dalej
    # https://en.wikipedia.org/wiki/Tournament_selection
    toolbox.register("select", tools.selTournament, tournsize=25)


    #registers how to mate
    # wybiera dwa punkty na stringu (liście) DNA.
    toolbox.register("mate", tools.cxTwoPoint)

    #registers how to mutate
    #szansa mutacji to indpb
    #metoda to: szansa indpb że dla atrybutu wylosuje nowy z przedziału)
    toolbox.register("mutate", tools.mutUniformInt, low= 0, up = max_gene_value - 1, indpb=0.05)
    #registers evaluate function
    toolbox.register("evaluate", evaluate_state_after_moves, entity_manager = entity_manager)
    #registers how to make a population
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #create population of 300
    pop = toolbox.population(n=300)



    #multiprocessing
    pool = multiprocessing.Pool()
    toolbox.register("level", pool.map)

    # number of gens to go through
    ngen = 100
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=ngen,
                                   stats=stats, halloffame=hof, verbose=True)
    print(hof)
    #knowledge_frames.__save_to_file__(str(log), "gen_outcome_{}".format(ngen))
    #knowledge_frames.__save_to_file__("\n" + str(hof), "gen_outcome_{}".format(ngen), newFile=False)
    #knowledge_frames.__save_to_file__("\n" + (str(get_fitness_for_hof(hof, LogicEngine))), "gen_outcome_{}".format(ngen), newFile=False)

    #print(get_fitness_for_hof(hof, entity_manager))
    #wait = input("Pokaż zwycięzcę: ")


    print(get_fitness_for_hof(hof))
    #entity_manager.entites[5].play_from_list(hof[0], level)

    return hof[0]



def get_fitness_for_hof(hof):
    return [winner.fitness.values for winner in hof]

def evaluate_state_after_moves(individual, entity_manager):
    """
    function that evaluates individual's fitness socre
    :param individual:
    :return:
    """
    simulated_logic_engine = simulate_from_list(individual, entity_manager)

    count_of_active_bombs = entity_manager.entites[5].bombs_left #jak najmniej
    count_of_time = entity_manager.entites[5].bombs_time() #jak najmniej
    count_of_saper_moves = entity_manager.entites[5].get_moves() #najmniej

    if(count_of_time > 0):
        return count_of_active_bombs, count_of_saper_moves, count_of_time
    else:
        return 0, 0, 10000000000

def simulate_from_list(list_of_indexes_of_objects_to_visit, entity_manager):
    """
    simulates the game from starting LogicEngine Position using the list of objects in order to visit
    :param LogicEngine: starting state of LogicEngine
    :param list_of_indexes_of_objects_to_visit:
    :return:
    """
    #original_object_list = copy.deepcopy(LogicEngine.original_object_list)
    simulated_logic_engine = entity_manager
    for index in list_of_indexes_of_objects_to_visit:
        if(simulated_logic_engine.entites[index].group_id == 2):
            simulated_logic_engine = simulated_logic_engine.entites[5].simulate_move_absolute_coordinate(x = simulated_logic_engine.entites[index].x, y = simulated_logic_engine.entites[index].y)
            if(simulated_logic_engine.entites[5].bombs_time() < 50):
                break
    return simulated_logic_engine


#
    # print("GENETIC LOG: PREPARED THE GENETIC ALGORITHM")
    #
    # #evaluates the entire population
    # fitnesses = list(map(toolbox.evaluate, pop))
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    # fits = [ind.fitness.values for ind in pop]
    #
    # generation_count = 1
    # record = stats.compile(pop)
    # print(record)
    # print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
    # hof.update(pop)

    # #evolution loop
    # while generation_count < ngen and fit[0] > 0 and fit[2] > 0:
    #     generation_count += 1
    #
    #     #Select new generation
    #     offspring = toolbox.select(pop, len(pop))
    #     # Clone the selected individuals
    #     offspring = list(map(toolbox.clone, offspring))
    #
    #     # Apply crossover and mutation on the offspring
    #     for child1, child2 in zip(offspring[::2], offspring[1::2]): #spółkowanie pierwszej połowy z drugą z wybranych
    #         if random.random() < CXPB: #szansa spółkowania
    #             toolbox.mate(child1, child2)
    #             del child1.fitness.values
    #             del child2.fitness.values #zmienia fitness na nieistniejący dzieci
    #
    #     for mutant in offspring:
    #         if random.random() < MUTPB: #szansa mutacji
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values #zmienia fitness na nieistniejący tych, którzy mutated
    #
    #     # Evaluate the individuals with an invalid fitness
    #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    #     fitnesses = map(toolbox.evaluate, invalid_ind)
    #     for ind, fit in zip(invalid_ind, fitnesses):
    #         ind.fitness.values = fit
    #
    #     pop[:] = offspring #nowa populacja zamiast starej
    #     record = stats.compile(pop)
    #     hof.update(pop)
    #     print(record)
    #     print("GENETIC LOG: SIMULATED SCORES OF {} GEN".format(generation_count))
    #     print("Best three ever to live: ", hof)
