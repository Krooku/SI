import pygame
import map
import saper
import bomb
import entity_manager
import genetic

pygame.init()

hof = []

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (10, 123, 10)
blue = (0, 0, 100)
bg_color = green

window_width = 992
window_height = 800
FPS = 30

level = map.Map(32)
level.load_map("mapa1")


entity_manager = entity_manager.Entity_manager()

entity_manager.add(bomb.Bomb(7, 12, "bomba.gif", level, 10))
entity_manager.add(bomb.Bomb(8, 15, "bomba.gif", level, 20))
entity_manager.add(bomb.Bomb(11, 5, "bomba.gif", level, 30))
entity_manager.add(bomb.Bomb(23, 20, "bomba.gif", level, 40))
entity_manager.add(bomb.Bomb(21, 7, "bomba.gif", level, 50))
entity_manager.add(saper.Saper(4, 3, 0, "saper.gif", level, entity_manager))


#--------------------------------------------------------------------------------

gameDisplay = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Inteligentny Saper')
clock = pygame.time.Clock()
gameExit = False

while not gameExit: #game_loop
    for event in pygame.event.get(): #event_loop
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit = True
            if event.key == pygame.K_1:
                entity_manager.entites[5].state = 1

            if event.key == pygame.K_0:
                hof = genetic.prepare_genetic(entity_manager, level)

            if event.key == pygame.K_2:
                entity_manager.entites[5].play_from_list([3, 2, 3, 1, 0, 3, 2, 1, 3, 3, 2, 1, 1, 0, 0], level)

            if event.key == pygame.K_9:
                entity_manager.reset()
                entity_manager.add(bomb.Bomb(7, 12, "bomba.gif", level, 10))
                entity_manager.add(bomb.Bomb(8, 15, "bomba.gif", level, 20))
                entity_manager.add(bomb.Bomb(11, 5, "bomba.gif", level, 30))
                entity_manager.add(bomb.Bomb(23, 20, "bomba.gif", level, 40))
                entity_manager.add(bomb.Bomb(21, 7, "bomba.gif", level, 50))
                entity_manager.add(saper.Saper(4, 3, 0, "saper.gif", level, entity_manager))
                entity_manager.entites[5].state = 5

            #if event.key == pygame.K_SPACE:
                #saper.rozbroj(mapa)

    entity_manager.update()
    #rand = random.randint(0, 4)
    #entity_manager.entites[5].change_direction(rand)
    #entity_manager.entites[5].move(level)

    if entity_manager.entites[5].state == 1:
        entity_manager.entites[5].search(level)

    if entity_manager.entites[5].state == 5:
        entity_manager.entites[5].search3(hof)

    #if entity_manager.entites[5].state == 0:
        #entity_manager.entites[5].search1(level)


    gameDisplay.fill(bg_color)
    #rysujobiekty(mapa)

    level.draw_map(gameDisplay)
    entity_manager.render(gameDisplay)
    #gameDisplay.blit(testowaBomba.bombaModel, testowaBomba.bombaModelRect)
    #tekst(saper.kierunek, mapa)
    pygame.display.update()
    clock.tick(FPS)
#koniec()
pygame.quit()
quit()