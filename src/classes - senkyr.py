import sys
import random

import pygame
pygame.init()

class Micek:
    def __init__(self, velikost, pozice_x, pozice_y, rychlost_x, rychlost_y):
        self.velikost = velikost
        
        self.pozice_x = pozice_x
        self.pozice_y = pozice_y
        
        self.rychlost_x = rychlost_x
        self.rychlost_y = rychlost_y
        
        self.cervena = random.randint(1, 255)
        self.zelena = random.randint(1, 255)
        self.modra = random.randint(1, 255)
    
    def vykreslit(self):
        pygame.draw.ellipse(okno, (self.cervena, self.zelena, self.modra), (self.pozice_x, self.pozice_y, self.velikost, self.velikost))
    
    def pohnout_se(self):
        self.pozice_x += self.rychlost_x
        self.pozice_y += self.rychlost_y
        
    def zustat_v_okne(self, rozliseni_okna):
        if self.pozice_x > rozliseni_okna[0] - self.velikost:
            self.pozice_x = rozliseni_okna[0] - self.velikost
            self.rychlost_x *= -1
        if self.pozice_y > rozliseni_okna[1] - self.velikost:
            self.pozice_y = rozliseni_okna[1] - self.velikost
            self.rychlost_y *= -1
        if self.pozice_x < 0:
            self.pozice_x = 0
            self.rychlost_x *= -1
        if self.pozice_y < 0:
            self.pozice_y = 0
            self.rychlost_y *= -1

micky = []

for i in range(100):
    micky.append(
        Micek(random.randint(15, 80),
              random.randint(1, 600),
              random.randint(1, 400),
              random.randint(1, 8) / 10,
              random.randint(1, 8) / 10)
        )

rozliseni_okna = (800, 600)

okno = pygame.display.set_mode(rozliseni_okna)

while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for micek in micky:
        micek.pohnout_se()
        micek.zustat_v_okne(rozliseni_okna)
    
    okno.fill((0, 255, 255))
    
    for micek in micky:
        micek.vykreslit()
    
    pygame.display.update()