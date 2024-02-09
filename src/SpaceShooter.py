import pygame, sys, random
pygame.init()

#variables
sirkaObrazovky, vyskaObrazovky = pygame.display.Info().current_w, pygame.display.Info().current_h #získá šířku, výšku obrazovky
rozliseniObrazovky = (sirkaObrazovky,vyskaObrazovky)

sirkaRaketky = 80
vyskaRaketky = 30
barvaRaketky= (255,0,0)

poziceRaketkyY = vyskaObrazovky/2 - vyskaRaketky/2
poziceRaketkyX = 150

rychlostRaketky = 5

barvaPozadí = (0,0,0)
 #zaklad
okno = pygame.display.set_mode(rozliseniObrazovky)
pygame.display.set_caption("Space Shooter")

#Nepřátelé

class Nepritel:
    def __init__(self, poziceX, poziceY, vyskaNepratele, sirkaNepratele, rychlostPohybu, rychlostStrelby, rychlostKulky, barvaNepratel):
        self.poziceX = poziceX
        self.poziceY = random.randint(0,(vyskaObrazovky-vyskaNepratele))
        
        self.vyskaNepratele = vyskaNepratele
        self.sirkaNepratele = sirkaNepratele
        
        self.rychlostPohybu = rychlostPohybu
        self.rychlostStrelby = rychlostStrelby
        self.rychlostKulky = rychlostKulky
        self.barvaNepratel = barvaNepratel
        
    def vykresleniNepratel(self):
        pygame.draw.rect(okno, self.barvaNepratel, (self.poziceX, self.poziceY, self.sirkaNepratele, self.vyskaNepratele))

Nepratele = []

for i in range(3):
    Nepratele.append(
        Nepritel(
            (sirkaObrazovky - 25), #poziceX
            random.randint(0,vyskaObrazovky), #poziceY
            random.randint(0,25), # VýškaNepřátel
            random.randint(0,25), # ŠířkaNepřátel
            random.uniform(0.5,1.5), #rychlostPohybu
            2, #Rychlost Střelby
            2, #Rychlost Kulky
            (0,0,255) #barvaNepřítele)
    ))



run = True
while run:
    pygame.time.delay(10) #framerate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            sys.exit()
            
    stisknuteKlavesy = pygame.key.get_pressed()
    
    if stisknuteKlavesy[pygame.K_ESCAPE] == True: #Escape vypne všechno
        pygame.quit()
        sys.exit()

    # POHYB RAKETKY
        
    if stisknuteKlavesy[pygame.K_UP]: #POHYB NAHORU
        poziceRaketkyY = poziceRaketkyY - rychlostRaketky
    
    if stisknuteKlavesy[pygame.K_DOWN]: #POHYB DOLŮ
        poziceRaketkyY = poziceRaketkyY + rychlostRaketky
    
    
    
    okno.fill(barvaPozadí)
    
    for Nepritel in Nepratele:
        Nepritel.vykresleniNepratel()
    
    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.update() 