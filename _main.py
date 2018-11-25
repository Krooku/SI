import pygame
import map
import saper
import bomb
import entity_manager
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
level.load_map("mapa1")

entity_manager = entity_manager.Entity_manager()

entity_manager.add(bomb.Bomb(4, 20, "bomba.gif", level))
entity_manager.add(bomb.Bomb(8, 15, "bomba.gif", level))
entity_manager.add(bomb.Bomb(11, 5, "bomba.gif", level))
entity_manager.add(bomb.Bomb(23, 20, "bomba.gif", level))
entity_manager.add(bomb.Bomb(23, 13, "bomba.gif", level))
entity_manager.add(saper.Saper(2, 2, 0, "saper.gif", level))

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
            if event.key == pygame.K_DOWN:
                entity_manager.entites[5].change_direction(0)
            if event.key == pygame.K_UP:
                entity_manager.entites[5].move(level)
            if event.key == pygame.K_RIGHT:
                entity_manager.entites[5].change_direction(1)
            if event.key == pygame.K_LEFT:
                entity_manager.entites[5].change_direction(2)
            #if event.key == pygame.K_SPACE:
                #saper.rozbroj(mapa)

    entity_manager.update(gameDisplay)
    rand = random.randint(0, 4)
    entity_manager.entites[5].change_direction(rand)
    entity_manager.entites[5].move(level)

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