import pygame
import random
import configparser

ANCHO = 640
ALTO = 480
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
ROJO=[255,0,0]

def Recortar(imagen,a,b):
    info = imagen.get_rect()
    print info
    #c = info[2]/a
    #d = info[3]/b
    m=[]
    x = 0
    while x < info[2]:
        y = 0
        ls=[]
        while y < info[3]:
            cuadro = imagen.subsurface(x,y,a,b)
            ls.append(cuadro)
            y+=b
        m.append(ls)
        x+=a
    return m

def Recortar_Mapa(imagen,a,b):
    info = imagen.get_rect()
    m=[]
    y = 0
    while y < info[3]:
        x = 0
        ls=[]
        while x < info[2]:
            cuadro = imagen.subsurface(x,y,a,b)
            ls.append(cuadro)
            x+=a
        m.append(ls)
        y+=b
    return m

class Jugador(pygame.sprite.Sprite):
    def __init__(self,m):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 11
        self.con=0
        self.lim = [6,6,6,6,7,7,7,7,8,8,8,8]
        self.image = self.m[self.con][self.accion]
        self.rect=self.image.get_rect()
        self.velx=0
        self.vely=400

        self.nivel = None

    def Gravedad(self):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += .50

        #Observamos si nos encontramos sobre el suelo
        if self.rect.y >= ALTO - self.rect.height and self.vely >= 0:
            self.vely = 0
            self.rect.y = ALTO - self.rect.height
    def Saltar(self):
        print 'Entro a salto'
        self.rect.y += 2
        #lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_plataformas, False)
        self.rect.y -= 2
        print self.rect.bottom
        if  self.rect.bottom >= ALTO:
            self.vely = -20

    def update(self):
        self.Gravedad()
        self.rect.x += self.velx
        self.rect.y += self.vely
        self.image=self.m[self.con][self.accion]
        if self.con < self.lim[self.accion] and self.velx != 0:
            self.con +=1
        else:
            self.con = 0
            self.accion=11



class Bloque(pygame.sprite.Sprite):
    def __init__(self,pto,size,imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([60,80])
        self.image = imagen
        self.rect=self.image.get_rect()
        self.grito=pygame.mixer.Sound('grito.ogg')
        self.rect.x=pto[0]
        self.rect.y=pto[1]
        self.velx=0

    def EnRango(self,posj,val):
        liminf = self.rect.bottom - val
        limsup = self.rect.bottom + val
        dentro = False
        if (liminf < posj) and (posj < limsup):
            dentro = True
        return dentro

    def update(self):
        self.rect.x += self.velx
        if self.velx > 0:
            self.velx -= 1




if __name__ == '__main__':
    '''Programa principal'''
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    jugadores=pygame.sprite.Group()
    bloques=pygame.sprite.Group()

    fondo = pygame.image.load("Fondo.jpg")
    mapa = configparser.ConfigParser()
    mapa.read('mapa_prueba.mpt')

    archivoMapa = mapa.get('info','img')
    imagenMapa = pygame.image.load(archivoMapa)
    imagenProtagonista = pygame.image.load('personaje.png')
    info = imagenProtagonista.get_rect()
    mJ = Recortar(imagenProtagonista,64,64) #Matriz sprite Jugador
    mM = Recortar_Mapa(imagenMapa,32,32) #Matriz sprite mapa
    j=Jugador(mJ)
    jugadores.add(j)



    mp = mapa.get('info','mapa')
    mp = mp.split('\n')#Fragmenta la matriz en filas



    '''cargar mapa'''
    s = []
    c = 0
    f = 0
    for e in mp:
        for i in e:
            d = mapa.get(i,'tipo')

            # if d == 'vacio':
            #     #image = pygame.Surface([32,32])
            #     #pantalla.blit(image, [c*32,f*32])
            #     #pygame.display.flip()
            # if d == 'muro':
            #     fl = int(mapa.get('#','fil'))
            #     cl = int(mapa.get('#','col'))
            #     pantalla.blit(mM[fl][cl],[c*32,f*32])
            #   imagenProtagonista  pygame.display.flip()
            # if d == 'agua':
            #     fl = int(mapa.get('a','fil'))
            #     cl = int(mapa.get('a','col'))
            #     pantalla.blit(mM[fl][cl],[c*32,f*32])
            #     pygame.display.flip()
            if d == 'piso':
                fl = int(mapa.get('p','fil'))
                cl = int(mapa.get('p','col'))
                b = Bloque([c*32,f*32],[32,32],mM[fl][cl])
                bloques.add(b)
                #p.blit(mM[fl][cl],[c*32,f*32])
                #pygame.display.flip()
            c+=1
        f += 1
        c = 0

    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx=10
                    j.vely=0
                if event.key == pygame.K_LEFT:
                    j.velx=-10
                    j.vely=0
                if event.key == pygame.K_UP:
                    j.velx=0
                    j.Saltar()

                if event.key == pygame.K_DOWN:
                    j.velx=0
                    j.vely=10
                if event.key == pygame.K_x:
                    #golpe
                    j.accion=2
                    j.con = 0
                if event.key == pygame.K_c:
                    #patada
                    j.accion=6
                    j.con = 0
            if event.type == pygame.KEYUP:
                j.velx=0
                j.vely=0

        #colision
        ls_col=pygame.sprite.spritecollide(j,bloques,False)
        for b in ls_col:
            if j.velx>0:
                if j.accion == 2:
                    if b.EnRango(j.rect.bottom,20):
                        b.velx=8
                        b.grito.play()
                if j.accion == 6:
                    if b.EnRango(j.rect.bottom,20):
                        b.velx=16
                        b.grito.play()

        #refresco de pantalla
        bloques.update()
        jugadores.update()
        pantalla.blit(fondo,[0,0])
        bloques.draw(pantalla)
        jugadores.draw(pantalla)
        pygame.display.flip()
        reloj.tick(10)
