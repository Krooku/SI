import pygame
import map
import saper
import bomb
import entity_manager
import neuralnetwork
import trash
import random

pygame.init()

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
level.load_map("mapa2")

neuralnet = neuralnetwork.neuralnetwork()

entity_manager = entity_manager.Entity_manager()

entity_manager.add(bomb.Bomb(7, 12, "bomba.gif", level, neuralnet))
entity_manager.add(bomb.Bomb(8, 15, "bomba.gif", level, neuralnet))
entity_manager.add(bomb.Bomb(11, 5, "bomba.gif", level, neuralnet))
entity_manager.add(trash.Trash(15, 4, "bomba.gif", level, neuralnet))
entity_manager.add(bomb.Bomb(3, 7, "bomba.gif", level, neuralnet))
entity_manager.add(saper.Saper(4, 3, 0, "saper.gif", level, entity_manager))

neuralnet.recognize('images/dataset/random_trash/r (1).jpg')
neuralnet.recognize('images/dataset/random_trash/r (2).jpg')
neuralnet.recognize('images/dataset/random_trash/r (3).jpg')
neuralnet.recognize('images/dataset/random_trash/r (4).jpg')
neuralnet.recognize('images/dataset/random_trash/r (5).jpg')
neuralnet.recognize('images/dataset/random_trash/r (6).jpg')


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
        if entity_manager.entites[5].bombs_left == 0:
            gameExit = True
            #if event.key == pygame.K_SPACE:
                #saper.rozbroj(mapa)

    entity_manager.update(gameDisplay)
    #rand = random.randint(0, 4)
    #entity_manager.entites[5].change_direction(rand)
    #entity_manager.entites[5].move(level)
    entity_manager.entites[5].search(level)

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