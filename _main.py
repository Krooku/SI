import pygame
import math
import sys

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

bg_color = blue


window_width = 992
window_height = 800
FPS = 30

width = 50
height = 50
pos_x = window_width / 2 - width / 2
pos_y = window_height / 2 + height / 2
dir = 0
speed = 10

kwadrat = pygame.Rect(pos_x, pos_y, width, height)



gameDisplay = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption('Saper')

gameExit = False

clock = pygame.time.Clock()

while not gameExit: #game_loop
    for event in pygame.event.get(): #event_loop
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameExit = True
            if event.key == pygame.K_DOWN:
                dir = 3
            if event.key == pygame.K_UP:
                dir = 1
            if event.key == pygame.K_RIGHT:
                dir = 2
            if event.key == pygame.K_LEFT:
                dir = 4

    #kwadrat.x += math.sin(clock.tick(FPS))
    #kwadrat.y += math.cos(clock.tick(FPS))

    if(dir == 1): #north
        kwadrat.y -= speed
        pos_y -= speed
    elif(dir == 2): #east
        kwadrat.x += speed
        pos_x += speed
    elif(dir == 3): #south
        kwadrat.y += speed
        pos_y += speed
    elif(dir == 4): #west
        kwadrat.x -= speed
        pos_x -= speed

    gameDisplay.fill(bg_color)
    pygame.draw.rect(gameDisplay, green, kwadrat)

    pygame.display.update()

    clock.tick(FPS)
pygame.quit()
quit()