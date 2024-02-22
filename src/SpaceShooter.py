import pygame, sys, random, time
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
 
pocitadloWave = 0
 
pocetKulek = 0
reloadCheck = 1 #počitá dobu mezi střelami

#zaklad
okno = pygame.display.set_mode(rozliseniObrazovky, display=0)
pygame.display.set_caption("Space Shooter")

#Nepřátelé

class NepritelClass:
    def __init__(self, poziceX, poziceY, vyskaNepratele, sirkaNepratele, rychlostStrelby, rychlostKulky, barvaNepratel,existuje, reloadSpeed):
        self.poziceX = poziceX
        self.poziceY = random.randint(0,(vyskaObrazovky-vyskaNepratele))
        
        self.vyskaNepratele = vyskaNepratele
        self.sirkaNepratele = sirkaNepratele
        
        self.rychlostPohybu = sirkaNepratele/vyskaNepratele # větší rychlost čím tenší je
        self.rychlostStrelby = rychlostStrelby
        self.rychlostKulky = rychlostKulky
        self.barvaNepratel = barvaNepratel 
        self.existuje = existuje
        self.reloadSpeed = reloadSpeed

    def vykresleniNepratel(self):
        pygame.draw.rect(okno, self.barvaNepratel, (self.poziceX, self.poziceY, self.sirkaNepratele, self.vyskaNepratele))

    def PohybNepratel(self):
        self.poziceX -= self.rychlostPohybu
    
    
Nepratele = []

def ZacatekWave():
    global pocitadloWave
    for i in range(pocetNepratel): 
        Nepratele.append(
            NepritelClass(
                (sirkaObrazovky + random.randint(50,200)), #poziceX - posune je za obrazovku o nahodnou hodnotu
                random.randint(10,(vyskaObrazovky - vyskaRaketky)), #poziceY
                random.randint(25,50), # VýškaNepřátel
                random.randint(25,100), # ŠířkaNepřátel
                
                2, #Rychlost Střelby
                2, #Rychlost Kulky
                (0,0,255), #barvaNepřítele
                True,
                2 #reload speed
        ))
    pocitadloWave += 1
    print(pocitadloWave)
ZacatekWave()


listKulek = []

class Kulky:
    def __init__(self, poziceX, poziceY, rychlost, naObrazovce, velikost):
        self.poziceX = poziceRaketkyX
        self.poziceY = poziceRaketkyY
        self.rychlost = rychlost
        self.naObrazovce = naObrazovce
        self.velikost = velikost
        
        
        self.barvaKulky = (255,100,0)
        
    def vykresleniStrel(self):
        pygame.draw.circle(okno, self.barvaKulky,(self.poziceX + sirkaRaketky, self.poziceY + vyskaRaketky/2), self.velikost)

    def pohybKulek(self):
        self.poziceX += self.rychlost



def PridaniKulky(list):
        list.append(Kulky(poziceRaketkyX, poziceRaketkyY, 1, True, 5))
        return list



def Střelba():
    global reloadCheck, pocetKulek, listKulek
    if stisknuteKlavesy[pygame.K_SPACE] and reloadCheck == 1: #Sťrelba
        pocetKulek += 1 #Přidá kulku do listu
        listKulek = PridaniKulky(listKulek)
        reloadCheck = 0
        timer(2000)
    else:
        print(reloadCheck)
        
def timer(delka):
    global timeEnd,reloadCheck

    timeEnd = time.time() + (delka/1000)
    if time.time() < timeEnd:
        reloadCheck = 1
       


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
        poziceRaketkyY = vyskaObrazovky - vyskaRaketky #teleport z okrajů
    elif poziceRaketkyY >= vyskaObrazovky - vyskaRaketky: #ochrana spodního kraje
        poziceRaketkyY = 0
    
    
    okno.fill(barvaPozadí)

    for NepritelClass in Nepratele: #fuknce nepřátel
        NepritelClass.vykresleniNepratel()
        NepritelClass.PohybNepratel()

    for i in listKulek: #Funkčnost kulek
        i.vykresleniStrel()
        i.pohybKulek()
    '''    
    if stisknuteKlavesy[pygame.K_SPACE] and reloadCheck == 1: #Sťrelba
        pocetKulek += 1 #Přidá kulku do listu
        listKulek = PridaniKulky(listKulek)
        reloadCheck = 0
        print(reloadCheck)
    else:
        print(reloadCheck)
'''
    Střelba()
            
    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.update() 

print()