import pygame, sys, random, time
pygame.init()
pygame.font.init()

#images

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
countdownWavy = 3000
obtisnost = 1
Konec = False
UpgradMiridla = True

rychlostStrileni = 150
barvaCary = 8
count = 0 
tutorialCompleted = False

bylaStrela = 0
bylPohybNahoru = 0
bylPohybDolu = 0
odpocetTutorialu = 10

#zaklad
okno = pygame.display.set_mode(rozliseniObrazovky, display=0)
pygame.display.set_caption("Space Shooter")

listUpgradu = []

class Upgrady:
    def __init__(self, poziceX, poziceY, velikost):
        self.typ = random.randint(1,3)

        self.poziceX = poziceX
        self.poziceY = poziceY
        self.rychlostPadani = 3
        self.velikost = velikost
    
    def padaniUpgradu(self):
        self.poziceX -= self.rychlostPadani
        
    def VykresleniUpgradu(self):
        pygame.draw.circle(okno, (255,255,0), (self.poziceX, self.poziceY), self.velikost)
        
    def kontrolaUpgradulNaObrazovce(self):
        if self.poziceX < -100: 
            for i, o in enumerate(listUpgradu):
                    del listUpgradu[i]
                    break

        
def VypadnutiUpgradu(poziceZniceniX, poziceZniceniY):
    listUpgradu.append(
        Upgrady(
            poziceZniceniX,
            poziceZniceniY,
            15
        )
    )
    

#Nepřátelé
Nepratele = []
class NepritelClass:
    def __init__(self, poziceX, poziceY, vyskaNepratele, sirkaNepratele, rychlostPohybu,barvaNepratel,existuje, reloadSpeed):
        self.poziceX = poziceX
        self.poziceY = random.randint(50,(vyskaObrazovky-vyskaNepratele-50))
        
        self.vyskaNepratele = vyskaNepratele
        self.sirkaNepratele = sirkaNepratele
        
        self.rychlostPohybu = rychlostPohybu

        self.barvaNepratel = barvaNepratel
        self.existuje = existuje
        self.reloadSpeed = reloadSpeed

    def vykresleniNepratel(self):
        if self.existuje == True:
                pygame.draw.rect(okno, self.barvaNepratel, (self.poziceX, self.poziceY, self.sirkaNepratele, self.vyskaNepratele))

    def PohybNepratel(self):
        self.poziceX -= self.rychlostPohybu

    def kontrolaNepratelNaObrazovce(self):
        global Skore
        if self.poziceX < -100: 
            self.existuje = False #pokuď přejde obrazovku smaže všechny kulky co jsou False
            for i, o in enumerate(Nepratele):
                if o.existuje == False:
                    del Nepratele[i]
                    Skore -= obtisnost
                    break

def ZacatekWave(difficulty):
    listBarev = [(121,69,135), (87,212,110), (49,30,176), (255,73,141), (138,26,81), (83,250,170), (175,68,201), (255,73,46), (185,166,61), (196,251,15), (205,71,114), (193,65,232), (239,137,98), (104,18,174), (217,227,188), (196,255,18), (18,96,30), (73,90,222), (119,126,128), (199,58,10), (23,64,40),(118,240,41),(142,209,108)]
    global pocitadloWave
    if Konec == False:
        for i in range(round(pocetNepratel)):
            Nepratele.append(
                NepritelClass(
                    (sirkaObrazovky + random.randint(50,200)), #poziceX - posune je za obrazovku o nahodnou hodnotu
                    random.randint(10,(vyskaObrazovky - vyskaRaketky)), #poziceY
                    
                    random.randint(25,50), # VýškaNepřátel
                    random.randint(25,100), # ŠířkaNepřátel
                    
                    1.3**difficulty, #rychlostPohybu
                        
                    random.choice(listBarev), #barvaNepřítele
                    True, #existuje
                    2 #reload speed
            ))
                
            pocitadloWave += 1





listKulek = []

class Kulky:
    def __init__(self, rychlost, naObrazovce, vyskaKulky, sirkaKulky):
        self.poziceX = poziceRaketkyX
        self.poziceY = poziceRaketkyY
        self.rychlost = rychlost
        self.naObrazovce = naObrazovce
        
        self.sirkaKulky = sirkaKulky
        self.vyskaKulky = vyskaKulky
        
        self.barvaKulky = (255,100,0)
        
    def vykresleniStrel(self):
        if self.naObrazovce:
            pygame.draw.rect(okno, self.barvaKulky,(self.poziceX + sirkaRaketky, self.poziceY + vyskaRaketky/2, self.sirkaKulky, self.vyskaKulky))

    def pohybKulek(self):
        self.poziceX += self.rychlost


    def kontrolaKulkyNaObrazovce(self):
        if self.poziceX > (sirkaObrazovky + self.vyskaKulky): 
            self.naObrazovce = False #pokuď přejde obrazovku smaže všechny kulky co jsou False
            for i, o in enumerate(listKulek):
                if o.naObrazovce == False:
                    del listKulek[i]
                    break
                
def PridaniKulky(list):
        list.append(Kulky(10, #rychlost
                          True, #naobrazovce
                          7.5, #velikost
                          37.5
                          )) 
        return list

def kolizeHraceUpgradu():
    global rychlostStrileni, barvaCary, rychlostRaketky
    for upg in listUpgradu:
        if  poziceRaketkyX <= upg.poziceX <= poziceRaketkyX + sirkaRaketky:
            if poziceRaketkyY <= upg.poziceY <= poziceRaketkyY + upg.velikost :
                if upg.typ == 1:
                    rychlostStrileni -= 25
                    listUpgradu.remove(upg)
                elif upg.typ == 2:
                    barvaCary += 8
                    listUpgradu.remove(upg)
                elif upg.typ == 3:
                    rychlostRaketky += 1
                    listUpgradu.remove(upg)



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
        bylPohybNahoru = 1
    
    if stisknuteKlavesy[pygame.K_DOWN]: #POHYB DOLŮ
        poziceRaketkyY = poziceRaketkyY + rychlostRaketky
        bylPohybDolu = 1
    
    if poziceRaketkyY <= 0: #Ochrana horniho kraje
        poziceRaketkyY = vyskaObrazovky - vyskaRaketky #teleport z okrajů
    elif poziceRaketkyY >= vyskaObrazovky - vyskaRaketky: #ochrana spodního kraje
        poziceRaketkyY = 0

    reloadCheck -= 1
    if stisknuteKlavesy[pygame.K_SPACE] and reloadCheck <= 1:
        pocetKulek += 1 #Přidá kulku do listu 
        listKulek = PridaniKulky(listKulek) 
        reloadCheck = rychlostStrileni
        
        bylaStrela = 1
        

       
    for nep in Nepratele: #odstraneneni
        for kul in listKulek:
            
            nepRect = pygame.Rect(nep.poziceX, nep.poziceY, nep.sirkaNepratele, nep.vyskaNepratele)
            kulRect = pygame.Rect(kul.poziceX, kul.poziceY, kul.sirkaKulky, kul.vyskaKulky)
            
            if pygame.Rect.colliderect(nepRect, kulRect):
                count += 1
                nep.existuje = False
                Nepratele.remove(nep)
                Skore += 1
                if random.randint(1,4) == 1:
                    VypadnutiUpgradu(nep.poziceX, nep.poziceY)
                    
                    

                    
    if rychlostStrileni < 100:
        rychlostStrileni = 100

    kolizeHraceUpgradu()

    okno.fill(barvaPozadí)

    if UpgradMiridla:
        pygame.draw.line(okno, (barvaCary, barvaCary, barvaCary),
                         (poziceRaketkyX  + sirkaRaketky/2, poziceRaketkyY + vyskaRaketky/2), 
                         (poziceRaketkyX  + sirkaRaketky/2 + sirkaObrazovky, poziceRaketkyY + vyskaRaketky/2))


    if tutorialCompleted == False: 
        if bylPohybNahoru == 1:
            pygame.draw.rect(okno, (0, 204, 0), (250,250, 50,50)) #up
        else:
            pygame.draw.rect(okno, (191, 191, 191), (250,250, 50,50)) 
         
        if bylPohybDolu == 1:
            pygame.draw.rect(okno, (0, 204, 0), (250,310, 50,50)) #down
        else:
            pygame.draw.rect(okno, (191, 191, 191), (250,310, 50,50))
        
        if bylaStrela == 1:
            pygame.draw.rect(okno, (0, 204, 0), (310,280, 50,50)) #space
        else:
            pygame.draw.rect(okno, (191, 191, 191), (310,280, 50,50))

    if bylaStrela == 1 and bylPohybDolu == 1 and bylPohybNahoru == 1:
        if odpocetTutorialu == 0:
            tutorialCompleted = True
        else:
            odpocetTutorialu -= 1



    for i in listKulek: #Funkčnost kulek
        i.vykresleniStrel()
        i.pohybKulek()
        i.kontrolaKulkyNaObrazovce()
        
    
    for j in Nepratele: #fuknce nepřátel
        j.vykresleniNepratel()
        j.PohybNepratel()
        j.kontrolaNepratelNaObrazovce()

    for l in listUpgradu:
        l.padaniUpgradu()
        l.VykresleniUpgradu()
        l.kontrolaUpgradulNaObrazovce()


        
    if len(Nepratele) == 0 and len(listKulek) == 0 and len(listUpgradu) == 0 and tutorialCompleted == 1:
        obtisnost += 1
        pocetNepratel += 0.3
        ZacatekWave(obtisnost)


    if Skore < 0:
        listKulek.clear()
        Nepratele.clear()
        score_text = font.render("Prohrál jsi", True, (255,0,0))
        okno.blit(score_text, (sirkaObrazovky/2, vyskaObrazovky/2))
        Konec = True
        
    else:
        score_text = font.render(f'Score: {Skore}     Rychlost Střelby {rychlostStrileni}      dotek:{count}  {odpocetTutorialu}', True, (255, 255, 255))
        okno.blit(score_text, (10, 10))

    pygame.draw.rect(okno, barvaRaketky, (poziceRaketkyX, poziceRaketkyY, sirkaRaketky, vyskaRaketky))
    pygame.display.flip() 
    