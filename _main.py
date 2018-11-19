import pygame
import map
import saper
import bomb
import entity_manager
import math
import sys

# do zrobienia

# MAPA
# tablica X * Y
#

# SAPER:
# wybiera_kierunek do poruszania sie
# Sprawdza czy przed nim znajduje sie mina
# Jesli tak, probuje ja rozbroic
# Sprawdza, czy w poblizu znajduje sie niesprawdzone miejsce, kieruje sie tam
# omija sciany, oraz inne przeszkody
# Oznacza przebyta droge jako bezpieczna

# MINA:
# kazda na poczatku jest aktywna (oznaczona cyfra 2)
# rozbrojona zostaje oznaczona cyfra 3 oraz inna tekstura


# Rozminowanie konczy sie po rozbrojeniu wszystkich min przez sapera
from pygame.transform import rotate

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


'''
class Saper:
    def __init__(self, pozycjax, pozycjay, kierunek):
        self.x = pozycjax
        self.y = pozycjay
        self.kierunek = kierunek #kierunek poruszania sie (0 - dol, 1 - prawo, 2 - gora, 3 - lewo)
        self.saperModel = pygame.image.load("images/saper.gif")
        self.saperModelRect = self.saperModel.get_rect()
        self.saperModelRect.x = self.x*bokKratki
        self.saperModelRect.y = self.y*bokKratki

    def zmienkierunek(self, x):
        if(x == 1): #obroc sie w prawo
            self.saperModel = rotate(self.saperModel, -90)
            self.kierunek = (self.kierunek-1)%4
        elif(x == 2):    #obroc sie w lewo
            self.saperModel = rotate(self.saperModel, 90)
            self.kierunek = (self.kierunek+1)%4
        elif(x == 0):   #odwroc sie w tyl
            self.saperModel = rotate(self.saperModel, 180)
            self.kierunek = (self.kierunek + 2) % 4

    def kolizja(self,mapa):
        if (self.kierunek == 0):
            if (mapa[self.x + 1][self.y] != "0"):
                return True
            else:
                return False
        elif (self.kierunek == 1):
            if (mapa[self.x][self.y + 1] != "0"):
                return True
            else:
                return False
        elif (self.kierunek == 2):
            if (mapa[self.x - 1][self.y] != "0"):
                return True
            else:
                return False
        elif (self.kierunek == 3):
            if (mapa[self.x][self.y - 1] != "0"):
                return True
            else:
                return False

    def rozbroj(self, mapa):
        if (self.kierunek == 0):
            if (mapa[self.x + 1][self.y] == "2"):
                mapa[self.x + 1][self.y] = "3"
        elif (self.kierunek == 1):
            if (mapa[self.x][self.y + 1] == "2"):
                mapa[self.x][self.y + 1] = "3"
        elif (self.kierunek == 2):
            if (mapa[self.x - 1][self.y] == "2"):
                mapa[self.x - 1][self.y] = "3"
        elif (self.kierunek == 3):
            if (mapa[self.x][self.y - 1] == "2"):
                mapa[self.x][self.y - 1] = "3"

    def porusz(self, mapa):
        if not(self.kolizja(mapa)):
            if (self.kierunek == 0):
                self.saperModelRect.y += bokKratki
                self.x += 1
            elif (self.kierunek == 1):
                self.saperModelRect.x += bokKratki
                self.y += 1
            elif (self.kierunek == 2):
                self.saperModelRect.y -= bokKratki
                self.x -= 1
            elif (self.kierunek == 3):
                self.saperModelRect.x -= bokKratki
                self.y -= 1
        else:
            print(self.kolizja(mapa))
'''


#class Bomba:
#    def __init__(self, pozycjax, pozycjay, uzbrojona):
#        self.uzbrojona = uzbrojona
#        self.x = pozycjax
#        self.y = pozycjay
#        self.bombaModel = pygame.image.load("bomba.gif")
#        self.bombaModelRect = self.bombaModel.get_rect()
#        self.bombaModelRect = self.bombaModelRect.move(self.x, self.y)
#
#    def rozbroj(self):
#        self.uzbrojona = False
#        self.bombaModel = pygame.image.load("bombarozbrojona.gif")
'''
def tekst(x, mapa):   #informacje na ekranie
   font=pygame.font.SysFont("monospace", 15)
   napis=font.render("Kierunek:"+str(x) + " Pozycja: " + str(saper.x) + " " + str(saper.y) + " Bomby: " + str(sprawdzbomby(mapa)) , 2 ,(255,255,255))
   gameDisplay.blit(napis, (0, 0))

def ladujmape(nazwa):   #ladowanie mapy do tablicy
    f = open(nazwa).read()
    tablica = [y.split() for y in f.split('\n')]
    return tablica

#rysowanie sciany
def sciana(x,y):
    scianaModel = pygame.image.load("sciana.gif")
    scianaRect = pygame.Rect(x*bokKratki, y*bokKratki, bokKratki, bokKratki)
    gameDisplay.blit(scianaModel, scianaRect)

#rysowanie krzaka
def krzak(x,y):
    krzakModel = pygame.image.load("krzak.gif")
    krzakRect = pygame.Rect(x*bokKratki, y*bokKratki, bokKratki, bokKratki)
    gameDisplay.blit(krzakModel, krzakRect)

#rysowanie bomby
def bomba(x,y):
    bombaModel = pygame.image.load("bomba.gif")
    bombaRect = pygame.Rect(x*bokKratki, y*bokKratki, bokKratki, bokKratki)
    gameDisplay.blit(bombaModel, bombaRect)

#rysowanie rozbrojonej bomby
def bombarozbrojona(x,y):
    bombaRozbrojonaModel = pygame.image.load("bombarozbrojona.gif")
    bombaRozbrojonaRect = pygame.Rect(x*bokKratki, y*bokKratki, bokKratki, bokKratki)
    gameDisplay.blit(bombaRozbrojonaModel, bombaRozbrojonaRect)

#rysowanie obiektow na mapie
def rysujobiekty(mapa):
    posx = 0
    for a in mapa:
        posy = 0
        for b in a:
            if (b == "1"):
                sciana(posy, posx)
            elif (b == "4"):
                krzak(posy, posx)
            elif (b == "2"):
                bomba(posy, posx)
            elif (b == "3"):
                bombarozbrojona(posy,posx)
            posy += 1
        posx += 1

#sprawdzenie ilosci bomb na mapie
def sprawdzbomby(mapa):
    ilosc = 0
    for a in mapa:
        for b in a:
            if(b == "2"):
                   ilosc += 1
    return ilosc

#informacja o zakonczeniu
def koniec():
    font = pygame.font.SysFont("monospace", 15)
    if (sprawdzbomby(mapa) == 0):
        napis = font.render(
            "Rozbrojono wszystkie bomby.",
            2, (255, 255, 255))
    else:
        napis = font.render(
            "Zakonczono.",
            2, (255, 255, 255))
    gameDisplay.blit(napis, (window_height/2, window_width/2))
    pygame.display.update()
    pygame.time.wait(20000)'''

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
