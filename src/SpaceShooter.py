import pygame, sys, random, time
pygame.init()
pygame.font.init()

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

Skore = 0


#zaklad
okno = pygame.display.set_mode(rozliseniObrazovky, display=0)
pygame.display.set_caption("Space Shooter")

listUpgradu = []
class upgrady:
    def __init__(self, poziceX, poziceY, rychlostStrelby, zrychleni, velikostStrely, zvetseni, barva):
        self.poziceX = poziceX
        self.poziceY = poziceY
        
        
        self.rychlostStrelby = rychlostStrelby
        self.zrychleni = zrychleni
        
        self.velikostStrely = velikostStrely
        self.zvetseni = zvetseni
        
        self.barva = barva

#Nepřátelé
Nepratele = []
class NepritelClass:
    def __init__(self, poziceX, poziceY, vyskaNepratele, sirkaNepratele, barvaNepratel,existuje, reloadSpeed):
        self.poziceX = poziceX
        self.poziceY = random.randint(50,(vyskaObrazovky-vyskaNepratele-50))
        
        self.vyskaNepratele = vyskaNepratele
        self.sirkaNepratele = sirkaNepratele
        
        self.rychlostPohybu = sirkaNepratele/vyskaNepratele + 2 # větší rychlost čím tenší je

        self.barvaNepratel = barvaNepratel 
        self.existuje = existuje
        self.reloadSpeed = reloadSpeed

    def vykresleniNepratel(self):
        if self.existuje == True:
            pygame.draw.rect(okno, self.barvaNepratel, (self.poziceX, self.poziceY, self.sirkaNepratele, self.vyskaNepratele))

    def PohybNepratel(self):
        self.poziceX -= self.rychlostPohybu
        
    def vypadnutiUpgradu(self):
        nahodnost = random.randint(1,9)
        if nahodnost == 1: #upgrade rychlosti strelby
            listUpgradu.append(
                upgrady(
                self.poziceX,
                self.poziceY,
                1,#rychlostStrelby
                1,#zrychleni
        
                0,#velikostStrely
                0,#zvetseni
                (0, 255, 0)
            ))
        elif nahodnost == 2: #upgrade velikosti strelby
            listUpgradu.append(
                upgrady(
                self.poziceX,
                self.poziceY,
                
                0,#rychlostStrelby
                0,#zrychleni
        
                1,#velikostStrely
                1,#zvetseni
                (255, 255, 255)
                ))

    def kontrolaNaObrazovce(self):
        if self.poziceX < 0 - self.sirkaNepratele - 20:
            Nepratele.remove(nep)
            
def ZacatekWave():
    global pocitadloWave
    for i in range(pocetNepratel):
        Nepratele.append(
            NepritelClass(
                (sirkaObrazovky + random.randint(50,200)), #poziceX - posune je za obrazovku o nahodnou hodnotu
                random.randint(10,(vyskaObrazovky - vyskaRaketky)), #poziceY
                random.randint(25,50), # VýškaNepřátel
                random.randint(25,100), # ŠířkaNepřátel
                (0,0,255), #barvaNepřítele
                True, #existuje
                2 #reload speed
        ))
            
        pocitadloWave += 1
        print(pocitadloWave)
ZacatekWave()


listKulek = []

class Kulky:
    def __init__(self, rychlost, naObrazovce, velikost):
        self.poziceX = poziceRaketkyX
        self.poziceY = poziceRaketkyY
        self.rychlost = rychlost
        self.naObrazovce = naObrazovce
        self.velikost = velikost
        
        
        self.barvaKulky = (255,100,0)
        
    def vykresleniStrel(self):
        if self.naObrazovce:
            pygame.draw.circle(okno, self.barvaKulky,(self.poziceX + sirkaRaketky, self.poziceY + vyskaRaketky/2,), self.velikost)

    def pohybKulek(self):
        self.poziceX += self.rychlost

    def kontrolaKulkyNaObrazovce(self):
        if self.poziceX > (sirkaObrazovky + self.velikost): 
            self.naObrazovce = False #pokuď přejde obrazovku smaže všechny kulky co jsou False
            for i, o in enumerate(listKulek):
                if o.naObrazovce == False:
                    del listKulek[i]
                    break

    def KontrolaKolize(self, rect):
        circle_rect = pygame.Rect(self.poziceX - self.velikost, self.poziceY - self.velikost, self.velikost * 2, self.velikost * 2)
        return circle_rect.colliderect(rect)
        

def PridaniKulky(list):
        list.append(Kulky(3, #rychlost
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

    font = pygame.font.Font(None, 36)
    
    if stisknuteKlavesy[pygame.K_ESCAPE] == True: #Escape vypne všechno
        pygame.quit()
        sys.exit()
        
    if stisknuteKlavesy[pygame.K_p]:
        pass

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
        reloadCheck = 100
    
    for nep in Nepratele: #ničení nepřátel
            for kul in listKulek:
                if kul.KontrolaKolize(pygame.Rect(nep.poziceX, nep.poziceY, nep.sirkaNepratele, nep.vyskaNepratele)): 
                    nep.existuje = False
                    if nep.existuje == False:
                        nep.vypadnutiUpgradu()

                    Nepratele.remove(nep)
                    #removes the instance when it overlaps
                    Skore += 1

    okno.fill(barvaPozadí)

    for i in listKulek: #Funkčnost kulek
        i.vykresleniStrel()
        i.pohybKulek()
        i.kontrolaKulkyNaObrazovce()
        
    
    for j in Nepratele: #fuknce nepřátel
        j.vykresleniNepratel()
        j.PohybNepratel()

        
    if len(Nepratele) == 0 and len(listKulek) == 0:
        ZacatekWave()
            
    score_text = font.render(f'Score: {Skore}', True, (255, 255, 255))
    okno.blit(score_text, (10, 10))

    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.flip() 
    