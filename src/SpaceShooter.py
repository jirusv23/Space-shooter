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
reloadCheck = 1 #kolik mili. sekund do dalsi strely

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
        if self.existuje == True:
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
                True, #existuje
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
        if self.naObrazovce:
            pygame.draw.rect(okno, self.barvaKulky,(self.poziceX + sirkaRaketky, self.poziceY + vyskaRaketky/2, self.velikost, self.velikost))

    def pohybKulek(self):
        self.poziceX += self.rychlost

    def kontrolaKulkyNaObrazovce(self):
        if self.poziceX > (sirkaObrazovky + self.velikost): 
            self.naObrazovce = False #pokuď přejde obrazovku smaže všechny kulky co jsou False
            for i, o in enumerate(listKulek):
                if o.naObrazovce == False:
                    del listKulek[i]
                    break
#NEFUNGUJE
    def KontrolaKolize(self):
        for nep in Nepratele:
            for kul in listKulek:
                #nested loop

                if nep.poziceY < kul.poziceY < nep.poziceY + nep.vyskaNepratele:
                    if nep.poziceX < kul.poziceX < nep.poziceX + nep.sirkaNepratele:
                        #zkontroluje zda kulka je na neprateli
                        print(f"hit \npozice kulky X,Y: {round(kul.poziceX)},{round(kul.poziceY)} \npozice nepratele X,Y {round(nep.poziceX)},{round(nep.poziceY)}")
                        nep.existuje = False


            


def PridaniKulky(list):
        list.append(Kulky(poziceRaketkyX, #poziceX
                          poziceRaketkyY, #poziceY
                          3, #rychlost
                          True, #naobrazovce
                          7.5 #velikost
                          )) 
        return list



clock = pygame.time.Clock()
framerate = (60)

run = True
while run:
    pygame.time.delay(10)
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
    
    reloadCheck -= 1
    if stisknuteKlavesy[pygame.K_SPACE] and reloadCheck <= 1:
        pocetKulek += 1 #Přidá kulku do listu 
        listKulek = PridaniKulky(listKulek) 
        reloadCheck = 200
       
    

    
    
    okno.fill(barvaPozadí)

    for NepritelClass in Nepratele: #fuknce nepřátel
        NepritelClass.vykresleniNepratel()
        NepritelClass.PohybNepratel()

    for i in listKulek: #Funkčnost kulek
        i.vykresleniStrel()
        i.pohybKulek()
        i.kontrolaKulkyNaObrazovce()
        i.KontrolaKolize()
    

            
    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.update() 
    

print()