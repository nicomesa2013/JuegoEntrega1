import pygame
import random
import configparser

ANCHO = 1000
ALTO = 600
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
ROJO=[255,0,0]

def Recortar(imagen,a,b):
    info = imagen.get_rect()
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
        self.rect.x = 700
        self.rect.y = 400
        self.velx=0
        self.vely=0

        self.nivel = None

    def Gravedad(self):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += .35

        #Observamos si nos encontramos sobre el suelo
        if self.rect.y >= ALTO - self.rect.height and self.vely >= 0:
            self.vely = 0
            self.rect.y = ALTO - self.rect.height
    def Saltar(self):
        self.rect.y += 2
        lista_impactos_plataforma = pygame.sprite.spritecollide(self, self.nivel.listade_bloques, False)
        self.rect.y -= 2
        if len(lista_impactos_plataforma) > 0 or self.rect.bottom >= ALTO:
            self.vely = -10

    def update(self):
        self.Gravedad()
        self.rect.x += self.velx

        '''Seleccion de sprite'''
        self.image=self.m[self.con][self.accion]
        if self.con < self.lim[self.accion] and self.velx != 0:
            self.con +=1
        else:
            self.con = 0
            #self.accion=11
        '''Revision de impactos de juador con entorno'''
        lista_impactos_bloque = pygame.sprite.spritecollide(self, self.nivel.listade_bloques,False)
        for bloque in lista_impactos_bloque:
            '''Si estamos en desplazamiento a la derecha'''
            if self.velx > 0 :
                self.rect.right = bloque.rect.left
            elif self.velx < 0:
                self.rect.left = bloque.rect.right

        self.rect.y +=self.vely
        lista_impactos_bloque = pygame.sprite.spritecollide(self, self.nivel.listade_bloques,False)
        for bloque in lista_impactos_bloque:
            '''Si estamos desplazando en vertical'''
            if self.vely > 0:
                self.rect.bottom = bloque.rect.top
            elif self.vely < 0:
                self.rect.top = bloque.rect.bottom
            self.vely = 0


class Bloque(pygame.sprite.Sprite):
    def __init__(self,pto,size,imagen):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([60,80])
        self.image = imagen
        self.rect=self.image.get_rect()
        self.grito=pygame.mixer.Sound('grito.ogg')
        self.rect.x=pto[0]
        self.rect.y=pto[1]
        self.velx = 0
        self.vely = 0

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

class Bloque_Movimiento(Bloque):
    limite_superior = 0
    limite_inferior = 0
    limite_izquierdo = 0
    limite_derecho = 0


    jugador = None
    nivel = None
    def __init__(self,pto,size,imagen):
        super(Bloque_Movimiento,self).__init__(pto,size,imagen)

    def update(self):

        '''Mueve de izquierda/derecha'''
        self.rect.x += self.velx

        '''Colision con el jugador horizontal'''
        impacto = pygame.sprite.collide_rect(self,self.jugador)
        if impacto:
            '''Vemos si impactamos al jugador y lo desplazamos'''
            if self.velx < 0:
                self.jugador.rect.right = self.rect.left
            else:
                self.jugador.rect.left = self.rect.right

        '''Mueve de arriba/abajo vertical'''
        self.rect.y += self.vely

        '''Colision con el jugador vertical'''
        impacto = pygame.sprite.collide_rect(self,self.jugador)

        if impacto:
            '''Vemos si impactamos al jugador y lo desplazamos'''
            if self.vely < 0:
                self.jugador.rect.bottom = self.rect.top
            else:
                self.jugador.rect.top = self.rect.bottom

        if self.rect.bottom < self.limite_inferior or self.rect.top > self.limite_superior:
            self.vely *= -1



class Nivel(object):
    def __init__(self, jugador):
        self.listade_bloques = pygame.sprite.Group()
        self.listade_bloques_movi = pygame.sprite.Group()
        self.listade_enemigos = pygame.sprite.Group()

        self.jugador = jugador
        #Imagen de fondo
        self.imagende_fondo = pygame.image.load('Fondo.jpg')

        self.mapa = configparser.ConfigParser()
        self.mapa.read('mapa_prueba.mpt')
        archivoMapa = self.mapa.get('info','img')
        imagenMapa = pygame.image.load(archivoMapa)
        self.mM = Recortar_Mapa(imagenMapa,32,32)
        '''Limite/desplazamiento del nivel'''
        self.desplazar_escenario = 0
        self.limitedel_nivel = -1000


    def update(self):
        self.listade_bloques.update()
        self.listade_enemigos.update()

    def draw(self,pantalla):
        '''Dibujamos todo en el nivel'''

        '''Cargar imagen de fondo de mapa'''
        pantalla.blit(self.imagende_fondo,[0,0])

        '''Cargar todas las listas de sprites que teniamos'''
        self.listade_bloques.draw(pantalla)
        self.listade_bloques_movi.draw(pantalla)
        self.listade_enemigos.draw(pantalla)

    def enscenario_desplazar(self,desplazar_x):
        '''Hacer desplazamiento del escenario Izquierda/Derecha'''
        self.desplazar_escenario += desplazar_x

        '''Movemos todas las listas de sprites'''
        for plataforma in self.listade_bloques:
            plataforma.rect.x += desplazar_x

        for enemigo in self.listade_enemigos:
            enemigo.rec.x += desplazar_x

    def cargarMapa(self,pantalla):
        mp = self.mapa.get('info','mapa')
        mp = mp.split('\n')#Fragmenta la matriz en filas
        s = []
        c = 0
        f = 0
        for e in mp:
            for i in e:
                d = self.mapa.get(i,'tipo')

                # if d == 'vacio':
                #     #image de sistemas= pygame.Surface([32,32])
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
                    fl = int(self.mapa.get('p','fil'))
                    cl = int(self.mapa.get('p','col'))
                    b = Bloque([c*32,f*32],[32,32],self.mM[fl][cl])
                    self.listade_bloques.add(b)
                if d == 'piso movil':

                    fl = int(self.mapa.get('m','fil'))
                    cl = int(self.mapa.get('m','col'))
                    bm = Bloque_Movimiento([c*32,f*32],[32,32],self.mM[fl][cl])
                    bm.limite_inferior = bm.rect.centery - 100
                    bm.limite_superior = bm.rect.centery + 100
                    print 'limite_inferior:',bm.limite_inferior,'limite superior',bm.limite_superior
                    print 'bottom:',bm.rect.bottom,  'top',bm.rect.top
                    bm.vely = 2
                    bm.jugador = self.jugador
                    self.listade_bloques.add(bm)
                c+=1
            f += 1
            c = 0

if __name__ == '__main__':
    '''Programa principal'''
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    jugadores=pygame.sprite.Group()

    imagenProtagonista = pygame.image.load('personaje.png')
    info = imagenProtagonista.get_rect()
    mJ = Recortar(imagenProtagonista,64,64) #Matriz sprite Jugador
    j=Jugador(mJ)
    jugadores = pygame.sprite.Group()
    jugadores.add(j)

    nivel = Nivel(j)
    j.nivel = nivel
    nivel.cargarMapa(pantalla)


    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx=5
                    j.vely=0
                    j.accion = 11
                if event.key == pygame.K_LEFT:
                    j.velx=-5
                    j.vely=0
                    j.accion = 9
                if event.key == pygame.K_UP:
                    j.velx=0
                    j.Saltar()

                if event.key == pygame.K_DOWN:
                    j.velx=0
                    j.vely=5
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



        #refresco de pantalla
        jugadores.update()
        nivel.update()

        ''' Si el jugador se aproxima a la derecha'''
        if j.rect.x >= 800:
            diff = j.rect.x - 800
            j.rect.x = 800
            nivel.enscenario_desplazar(-diff)

        ''' Si el jugador se aproxima a la derecha'''
        if j.rect.x <= 200:
            diff = 200 - j.rect.x
            j.rect.x = 200
            nivel.enscenario_desplazar(diff)

        '''Zona de dibujado'''
        nivel.draw(pantalla)
        jugadores.draw(pantalla)

        pygame.display.flip()
        reloj.tick(60)
