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

pocetNepratel = 3
 
#zaklad
okno = pygame.display.set_mode(rozliseniObrazovky)
pygame.display.set_caption("Space Shooter")

#Nepřátelé

class NepritelClass:
    def __init__(self, poziceX, poziceY, vyskaNepratele, sirkaNepratele, rychlostStrelby, rychlostKulky, barvaNepratel, existuje):
        self.poziceX = poziceX
        self.poziceY = random.randint(0,(vyskaObrazovky-vyskaNepratele))
        
        self.vyskaNepratele = vyskaNepratele
        self.sirkaNepratele = sirkaNepratele
        
        self.rychlostPohybu = sirkaNepratele/vyskaNepratele # větší rychlost čím tenší je
        self.rychlostStrelby = rychlostStrelby
        self.rychlostKulky = rychlostKulky
        self.barvaNepratel = barvaNepratel 
        self.existuje = existuje

    def vykresleniNepratel(self):
        pygame.draw.rect(okno, self.barvaNepratel, (self.poziceX, self.poziceY, self.sirkaNepratele, self.vyskaNepratele))

    def PohybNepratel(self):
        self.poziceX -= self.rychlostPohybu
    
    
Nepratele = []

for i in range(pocetNepratel): 
    Nepratele.append(
        NepritelClass(
            (sirkaObrazovky + random.randint(25,100)), #poziceX - posune je za obrazovku o nahodnou hodnotu
            random.randint(10,(vyskaObrazovky - 10)), #poziceY
            random.randint(25,50), # VýškaNepřátel
            random.randint(25,100), # ŠířkaNepřátel
            
            2, #Rychlost Střelby
            2, #Rychlost Kulky
            (0,0,255), #barvaNepřítele
            True
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
    
    if poziceRaketkyY <= 0: #Ochrana horniho kraje
        poziceRaketkyY = vyskaObrazovky - vyskaRaketky 
    elif poziceRaketkyY >= vyskaObrazovky - vyskaRaketky:
        poziceRaketkyY = 0
    
    for NepritelClass in Nepratele:
        NepritelClass.PohybNepratel()
    
    okno.fill(barvaPozadí)
    
    for NepritelClass in Nepratele:
        NepritelClass.vykresleniNepratel()
        
    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.update() 