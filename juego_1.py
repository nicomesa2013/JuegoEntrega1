import pygame
import random
import configparser

ANCHO = 1000
ALTO = 600
VERDE=[0,255,0]
BLANCO=[255,255,255]
NEGRO=[0,0,0]
AZUL=[0,0,255]
ROJO=[255,0,0]

def Recortar(imagen,a,b,n):
    info = imagen.get_rect()
    #c = info[2]/a
    #d = info[3]/b
    m=[]
    x = 0
    while x < info[2]:
        y = 0
        ls=[]
        while y < info[3]:
            cuadro = imagen.subsurface(x,y,a,b-n)
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
        self.accion = 1
        self.con=0
        self.lim = [8,8,7,7]
        self.image = self.m[self.con][self.accion]

        self.rect=self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 456
        self.velx=0
        self.vely=0

        self.puntos_de_vida = pygame.image.load('vida.png')
        self.vidas = 3

        self.derecha = True
        self.cont = 0

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
            self.vely = -8

    def update(self):
        self.rect.x += self.velx
        self.Gravedad()
        self.mov()

        '''Revision de impactos de juador con entorno'''
        lista_impactos_bloque = pygame.sprite.spritecollide(self, self.nivel.listade_bloques,False)
        for bloque in lista_impactos_bloque:
            '''Si estamos en desplazamiento a la derecha'''
            if self.velx > 0 :
                self.rect.right = bloque.rect.left
            if self.velx < 0:
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

        v = 0
        espacio_vidas = 10
        while v < self.vidas:
            pantalla.blit(j.puntos_de_vida,[espacio_vidas,10])
            espacio_vidas += 37
            v += 1

        if self.vidas == 0:
            jugadores.remove(j)

    def pos(self):
        p=[self.rect.x,self.rect.y]
        return p

    def mov(self):
        '''Seleccion de sprite'''
        self.image=self.m[self.con][self.accion]
        if self.con < self.lim[self.accion] and self.velx != 0:
            self.con +=1
        elif self.accion == 2:
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                self.accion = 0
        elif self.accion == 3:
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                self.accion = 1
        else:
            self.con = 0

    def col_enemigo(self,n):
        while self.cont < 20:
            self.cont += 1
            self.velx = n
            self.rect.x += self.velx
            self.mov()
        self.cont = 0
        self.velx = n*-1


class Proyectil(pygame.sprite.Sprite):
    def __init__(self,pos,n,COLOR):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,15])
        self.image.fill(COLOR)
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]+20
        self.con = self.rect.x
        self.velx = n

    def update(self):
        self.rect.x+=self.velx

class Enemigo1(pygame.sprite.Sprite):
    def __init__(self,m,posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 0
        self.con=0
        self.lim = [7,3,7,3]
        self.image = self.m[self.con][self.accion]

        self.actualizacion = pygame.time.get_ticks()

        self.estado = True
        self.vidas = 3

        self.rect=self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.cont = 0

    def update(self):
        '''Seleccion de sprite'''
        if self.actualizacion + 75 < pygame.time.get_ticks():
            self.image = self.m[self.con][self.accion]
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                self.con = 0
                self.accion = 0
            self.actualizacion= pygame.time.get_ticks()

    def pos(self):
        p=[self.rect.x,self.rect.y]
        return p

class Enemigo2(pygame.sprite.Sprite):
    jugador = None
    def __init__(self,m,posX,posY):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 0
        self.con=0
        self.lim = [2,2]
        self.image = self.m[self.con][self.accion]

        self.actualizacion = pygame.time.get_ticks()

        self.estado = True
        self.vidas = 3

        self.rect=self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.limite = 50
        self.limiteizquierda = 50
        self.limitederecha = 0
        self.cont1 = 0
        self.cont2 = 50
        self.izquierda = True
        self.evelx = -2

    def col_iz(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left > self.jugador.rect.right:
                self.jugador.rect.right = self.rect.left
                self.jugador.col_enemigo(3)
                self.jugador.vidas -= 1

        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left < self.jugador.rect.x:
                self.jugador.rect.left = self.rect.right
                self.jugador.col_enemigo(3)
                self.jugador.vidas -= 1

    def col_der(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left < self.jugador.rect.right:
                self.jugador.rect.right = self.rect.left
                self.jugador.col_enemigo(-3)
                self.jugador.vidas -= 1

        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left > self.jugador.rect.x:
                self.jugador.rect.left = self.rect.right
                self.jugador.col_enemigo(-3)
                self.jugador.vidas -= 1

    def update(self):
        if self.izquierda == True:
            if self.cont1 < self.limite:
                self.cont1 += 1
                self.rect.x += self.evelx
            if self.cont1 == self.limite:
                self.evelx = 2
                self.cont1 = 0
                self.accion = 1
                self.izquierda = False
        if self.izquierda == False:
            if self.cont1 < self.limite:
                self.cont1 += 1
                self.rect.x += self.evelx
            if self.cont1 == self.limite:
                self.evelx = -2
                self.cont1 = 0
                self.accion = 0
                self.izquierda = True

        self.col_iz()
        self.col_der()



        if self.actualizacion + 150 < pygame.time.get_ticks():
            self.image = self.m[self.con][self.accion]
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                self.con = 0
            self.actualizacion= pygame.time.get_ticks()

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
        self.imagende_fondo = pygame.image.load("background.png")
        self.enemigo1 = pygame.image.load("enemigo1.png")
        #info = background.get_rect()
        self.fx = -100
        self.fy = -850
        self.fvelx = 0
        self.fvely = 0
        self.limderecha = ANCHO-100
        self.limizq = 100
        self.limabajo = ALTO
        self.limarriba = 100

        self.info = self.imagende_fondo.get_rect()
        self.anf = self.info[2]
        self.alf = self.info[3]

        self.mapa = configparser.ConfigParser()
        self.mapa.read('mapa_prueba.mpt')
        archivoMapa = self.mapa.get('info','img')
        imagenMapa = pygame.image.load(archivoMapa)
        self.mM = Recortar_Mapa(imagenMapa,32,32)
        #Limite/desplazamiento del nivel
        self.desplazar_escenario = 0
        self.limitedel_nivel = -1000


    '''def update(self):
        self.listade_bloques.update()
        self.listade_enemigos.update()'''


    def draw(self,pantalla):
        '''Dibujamos todo en el nivel'''
        '''Cargar imagen de fondo de mapa'''
        pantalla.blit(self.imagende_fondo,[self.fx,self.fy])

        '''Cargar todas las listas de sprites que teniamos'''
        self.listade_bloques.draw(pantalla)
        self.listade_bloques_movi.draw(pantalla)
        self.listade_enemigos.draw(pantalla)

    def enscenario_desplazar(self,desplazar_x):
        self.fx += desplazar_x

        #Movemos todas las listas de sprites
        for plataforma in self.listade_bloques:
            plataforma.rect.x += desplazar_x


    def cargarMapa(self,pantalla):
        mp = self.mapa.get('info','mapa')
        mp = mp.split('\n')#Fragmenta la matriz en filas
        s = []
        c = 0
        f = 0
        for e in mp:
            for i in e:
                d = self.mapa.get(i,'tipo')

                if d == 'vacio':
                    #image de sistemas= pygame.Surface([32,32])
                    #pantalla.blit(image, [c*32,f*32])
                    pygame.display.flip()
                if d == 'terreno1':
                    fl = int(self.mapa.get('!','fil'))
                    cl = int(self.mapa.get('!','col'))
                    b = Bloque([c*32,f*32],[32,32],self.mM[fl][cl])
                    self.listade_bloques.add(b)
                if d == 'terreno2':
                    fl = int(self.mapa.get('@','fil'))
                    cl = int(self.mapa.get('@','col'))
                    b = Bloque([c*32,f*32],[32,32],self.mM[fl][cl])
                    self.listade_bloques.add(b)
                if d == 'terreno3':
                    fl = int(self.mapa.get('#','fil'))
                    cl = int(self.mapa.get('#','col'))
                    b = Bloque([c*32,f*32],[32,32],self.mM[fl][cl])
                    self.listade_bloques.add(b)
                if d == 'terreno4':
                    fl = int(self.mapa.get('$','fil'))
                    cl = int(self.mapa.get('$','col'))
                    b = Bloque([c*32,f*32],[32,32],self.mM[fl][cl])
                    self.listade_bloques.add(b)
                if d == 'piso movil':
                    fl = int(self.mapa.get('m','fil'))
                    cl = int(self.mapa.get('m','col'))
                    bm = Bloque_Movimiento([c*32,f*32],[32,32],self.mM[fl][cl])
                    bm.limite_inferior = bm.rect.centery - 100
                    bm.limite_superior = bm.rect.centery + 100
                    #print 'limite_inferior:',bm.limite_inferior,'limite superior',bm.limite_superior
                    #print 'bottom:',bm.rect.bottom,  'top',bm.rect.top
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

    imagenProtagonista = pygame.image.load('personajev2.png')
    #info = imagenProtagonista.get_rect()
    mJ = Recortar(imagenProtagonista,32,56,3) #Matriz sprite Jugador
    j=Jugador(mJ)
    jugadores = pygame.sprite.Group()
    jugadores.add(j)

    enemigos1 = pygame.sprite.Group()
    imagenenemigo1 = pygame.image.load('enemigo1.png')
    recorte_enemigo1=Recortar(imagenenemigo1,64,64,0)
    enemigo1A = Enemigo1(recorte_enemigo1,100,450)
    enemigo1B = Enemigo1(recorte_enemigo1,1000,450)
    enemigos1.add(enemigo1A)
    enemigos1.add(enemigo1B)
    proyectil=pygame.sprite.Group()
    proyectil_enemigo=pygame.sprite.Group()

    enemigos2 = pygame.sprite.Group()
    imagenenemigo1 = pygame.image.load('enemigo2.png')
    recorte_enemigo2=Recortar(imagenenemigo1,66,40,0)
    enemigo2A = Enemigo2(recorte_enemigo2,800,470)
    enemigo2A.jugador = j
    enemigos2.add(enemigo2A)

    nivel = Nivel(j)
    j.nivel = nivel
    nivel.cargarMapa(pantalla)

    actualizacion = pygame.time.get_ticks()


    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    j.velx=5
                    j.accion = 0
                    j.derecha = True
                if event.key == pygame.K_LEFT:
                    j.velx=-5
                    j.accion = 1
                    j.derecha = False
                if event.key == pygame.K_UP:
                    #j.velx=0
                    j.Saltar()

                if event.key == pygame.K_DOWN:
                    j.velx=0
                    j.vely=5
                if event.key == pygame.K_x:
                    #golpe
                    j.accion=2
                    j.con = 0
                    if j.derecha == True:
                        disparo=Proyectil(j.pos(),5,ROJO)
                        disparo.rect.x += 20
                        j.accion=2
                        j.con = 0
                    else:
                        disparo=Proyectil(j.pos(),-5,ROJO)
                        j.accion=3
                        j.con = 0
                    proyectil.add(disparo)
                if event.key == pygame.K_c:
                    #patada
                    if j.derecha == True:
                        disparo=Proyectil(j.pos(),5,ROJO)
                        disparo.rect.x += 20
                        j.accion=2
                        j.con = 0
                    else:
                        disparo=Proyectil(j.pos(),-5,ROJO)
                        j.accion=3
                        j.con = 0
                    proyectil.add(disparo)
            if event.type == pygame.KEYUP:
                j.velx=0
                nivel.fvelx = 0
                nivel.fvely = 0

        # Si el jugador se aproxima a la derecha
        if j.rect.x > nivel.limderecha:
            diff = j.rect.x - nivel.limderecha
            j.rect.x = nivel.limderecha
            nivel.enscenario_desplazar(-diff)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.x += -diff
            for enemigo_2 in enemigos2:
                enemigo_2.rect.x += -diff


        # Si el jugador se aproxima a la derecha
        if j.rect.x < nivel.limizq:
            diff = nivel.limizq - j.rect.x
            j.rect.x = nivel.limizq
            nivel.enscenario_desplazar(diff)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.x += diff
            for enemigo_2 in enemigos2:
                enemigo_2.rect.x += diff
                #enemigo_2.distancia += diff


        #colision de proyectil con bloque
        for b in nivel.listade_bloques:
            ls=pygame.sprite.spritecollide(b,proyectil,True)
            for b in ls:
                #print ('colision')
                proyectil.remove(b)
        #colision de proyectil enemigo con bloque
        for proyectil_colision in nivel.listade_bloques:
            ls=pygame.sprite.spritecollide(proyectil_colision,proyectil_enemigo,True)
            for proyectil_colision in ls:
                #print ('colision')
                proyectil.remove(proyectil_colision)

        #proyectil enemigo1 en jugador
        for be in proyectil_enemigo:
            ls_pro=pygame.sprite.spritecollide(j,proyectil_enemigo,True)
            for be in ls_pro:
                j.vidas -= 1

        #proyectil en enemigo1
        for e_fantasma in enemigos1:
            ls_enemigo = pygame.sprite.spritecollide(e_fantasma,proyectil,True)
            for proyectil_jugador in ls_enemigo:
                proyectil.remove(proyectil_jugador)
                e_fantasma.vidas -= 1
                if e_fantasma.vidas == 0:
                    e_fantasma.estado = False
                    enemigos1.remove(e_fantasma)
        #proyectil en enemigo2
        for e_arana in enemigos2:
            ls_enemigo2 = pygame.sprite.spritecollide(e_arana,proyectil,True)
            for proyectil_jugador in ls_enemigo2:
                proyectil.remove(proyectil_jugador)
                e_arana.vidas -= 1
                if e_arana.vidas == 0:
                    enemigos2.remove(e_arana)


        #proyectil enemigo1
        if actualizacion + 4000 < pygame.time.get_ticks() and enemigo1A.estado == True:
            e = enemigo1A.pos()
            enemigo1A.accion = 3
            enemigo1A.con = 0
            disparo2=Proyectil([e[0]+20,e[1]],5 ,AZUL)
            proyectil_enemigo.add(disparo2)
            actualizacion = pygame.time.get_ticks()

        #Zona de dibujado
        nivel.draw(pantalla)
        jugadores.draw(pantalla)
        proyectil.draw(pantalla)
        proyectil_enemigo.draw(pantalla)
        enemigos1.draw(pantalla)
        enemigos2.draw(pantalla)
        #refresco de pantalla
        jugadores.update()
        proyectil.update()
        proyectil_enemigo.update()
        enemigos1.update()
        enemigos2.update()
        #nivel.update()
        #nivel.escenario_desplazar()
        pygame.display.flip()
        reloj.tick(30)
