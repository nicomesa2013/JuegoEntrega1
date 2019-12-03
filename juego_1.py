import pygame
import random
import configparser
import sys
from pygame.locals import *

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

def Menu(opcion):
    fondoMenu = pygame.image.load('Images/Menu/FondoMenu.jpeg').convert()
    fuente = pygame.font.Font('Fuentes/FuenteP.ttf',90)
    titulo = fuente.render('THE WITCHER',True,BLANCO)
    pantalla.blit(fondoMenu,[0,0])
    pantalla.blit(titulo,[300,100])

    if opcion == 1:
        iniciarJuego, pos1 = TextoMenu("Iniciar Juego",[500,300],ROJO)
        salir, pos2 = TextoMenu("Salir",[500,400],NEGRO)
    elif opcion == 2:
        iniciarJuego, pos1 = TextoMenu("Iniciar Juego",[500,300],NEGRO)
        salir, pos2 = TextoMenu("Salir",[500,400],ROJO)
    else:
        iniciarJuego, pos1 = TextoMenu("Iniciar Juego",[500,300],NEGRO)
        salir, pos2 = TextoMenu("Salir",[500,400],NEGRO)
    pantalla.blit(iniciarJuego,pos1)
    pantalla.blit(salir,pos2)

def GameOver():
    fondoMenu = pygame.image.load('Images/Menu/FondoMenu.jpeg').convert()
    fuente = pygame.font.Font('Fuentes/FuenteP.ttf',90)
    titulo = fuente.render('Game Over',True,ROJO)
    pantalla.blit(titulo,[300,100])
    pygame.display.flip()

def Congratulations():
    fondoMenu = pygame.image.load('Images/Menu/FondoMenu.jpeg').convert()
    fuente = pygame.font.Font('Fuentes/FuenteP.ttf',90)
    titulo = fuente.render('Congratulations',True,ROJO)
    pantalla.blit(titulo,[300,100])
    pygame.display.flip()

def Pausa():
    fondoMenu = pygame.image.load('Images/Menu/FondoMenu.jpeg').convert()
    fuente = pygame.font.Font('Fuentes/FuenteP.ttf',60)
    titulo = fuente.render('Presione una tecla para continuar',True,ROJO)
    pantalla.blit(titulo,[120,100])
    pygame.display.flip()

def TextoMenu(texto,pos,color):
    fuente = pygame.font.Font('Fuentes/FuenteP.ttf',60)
    salida = pygame.font.Font.render(fuente, texto, True, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = pos[0]
    salida_rect.centery = pos[1]
    return salida, salida_rect

class Jugador(pygame.sprite.Sprite):
    def __init__(self,m):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 0
        self.con=0
        self.lim = [8,8,7,7]
        self.image = self.m[self.con][self.accion]

        self.rect=self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 875
        self.velx=0
        self.vely=0
        self.movimiento=5
        self.csalto = 8

        self.sonido_pasos=pygame.mixer.Sound('audio/pasos.ogg')
        self.sonido_proyectil=pygame.mixer.Sound('audio/proyectil_j.ogg')
        self.sonido_mejora_proyectil=pygame.mixer.Sound('audio/mejora_proyectil.ogg')
        self.sonido_pocion=pygame.mixer.Sound('audio/sonido_pocion.ogg')
        self.sonido_vida=pygame.mixer.Sound('audio/sonido_vida.ogg')
        self.sonido_jugador=pygame.mixer.Sound('audio/sonido_jugador.ogg')

        self.cont_enemigos = 0


        self.puntos_de_vida = pygame.image.load('vida.png')
        self.vidas = 3

        self.mejora = pygame.image.load('proyectil_j1.png')
        self.mejora_pocion = pygame.image.load('proyectil_j1.png')

        self.obtener_mejora = False
        self.obtener_pocion = False

        self.proyectil_tipo = 0

        self.derecha = True
        self.cont = 0

        self.nivel = None

        self.actualizacion_damage = pygame.time.get_ticks()


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
            self.vely = -j.csalto

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
            pygame.sprite.Sprite.kill(self)
            GameOver()



        if self.obtener_mejora == True:
            #pantalla.blit(self.image,[10,42])
            pantalla.blit(self.mejora,[40,50])
        if self.obtener_pocion == True:
            pantalla.blit(self.mejora_pocion,[10,50])

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
            if self.vely == 1 and self.con != 0:
                self.sonido_pasos.play()
            self.con = 0


    def col_enemigo(self):
        if self.actualizacion_damage + 1250 < pygame.time.get_ticks():
            self.sonido_jugador.play()
            self.vidas -= 1
            self.actualizacion_damage = pygame.time.get_ticks()

        '''while self.cont < 20:
            self.cont += 1
            self.velx = n
            self.rect.x += self.velx
            self.mov()
        self.cont = 0
        self.velx = n*-1'''


class Proyectil(pygame.sprite.Sprite):
    def __init__(self,pos,n,imagen_proyectil):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen_proyectil
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]+20
        self.con = self.rect.x
        self.velx = n

    def update(self):
        self.rect.x+=self.velx

class Enemigo1(pygame.sprite.Sprite):
    jugador = None
    def __init__(self,m,posX, posY):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 0
        self.con=0
        self.lim = [7,3,7,3]
        self.image = self.m[self.con][self.accion]

        self.actualizacion = pygame.time.get_ticks()
        self.actualizacion2 = pygame.time.get_ticks()

        self.estado = True
        self.vidas = 3

        self.sonido_enemigo1=pygame.mixer.Sound('audio/sonido_enemigo1.ogg')

        self.rect=self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY

        self.proyectil_e1 = pygame.image.load('Projectil_e1.png')
        self.proyectil_e2 = pygame.image.load('Projectil_e2.png')

        self.izquierda = True
        self.cont = 0

    def posjugador(self):
        if self.rect.x < self.jugador.rect.x:
            self.izquierda = True
        else:
            self.izquierda = False

    def update(self):
        self.posjugador()
        self.ataque()
        '''Seleccion de sprite'''
        self.mov()

    def pos(self):
        p=[self.rect.x,self.rect.y]
        return p

    def ataque(self):
        #proyectil enemigo1
        if self.actualizacion2 + 4000 < pygame.time.get_ticks() and self.estado == True:
            e = self.pos()
            if self.izquierda == True:
                self.accion = 3
                self.con = 0
                disparo2=Proyectil([e[0]+20,e[1]],5,self.proyectil_e1)
                proyectil_enemigo.add(disparo2)
            else:
                self.accion = 1
                self.con = 0
                disparo2=Proyectil([e[0]+20,e[1]],-5,self.proyectil_e2)
                proyectil_enemigo.add(disparo2)
            self.actualizacion2 = pygame.time.get_ticks()
    def mov(self):
        if self.actualizacion + 75 < pygame.time.get_ticks():
            self.image = self.m[self.con][self.accion]
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                if self.izquierda == True:
                    self.accion = 2
                else:
                    self.accion = 0
                self.con = 0
            self.actualizacion= pygame.time.get_ticks()

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

        self.sonido_damage=pygame.mixer.Sound('audio/spider.ogg')
        self.sonido_damage2=pygame.mixer.Sound('audio/spider2.ogg')

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
                self.jugador.col_enemigo()

        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left < self.jugador.rect.x:
                self.jugador.rect.left = self.rect.right
                self.jugador.col_enemigo()

    def col_der(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left < self.jugador.rect.right:
                self.jugador.rect.right = self.rect.left
                self.jugador.col_enemigo()

        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.rect.left > self.jugador.rect.x:
                self.jugador.rect.left = self.rect.right
                self.jugador.col_enemigo()

    def col_top(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            if self.jugador.rect.bottom > self.rect.top:
                self.jugador.rect.bottom = self.rect.top
                self.jugador.col_enemigo()

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

        self.col_top()
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
        self.image = imagen
        self.rect=self.image.get_rect()
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
        '''if self.velx > 0:
            self.velx -= 100'''

class Spawner(pygame.sprite.Sprite):
    def __init__(self,m,posX,posY,tipo,jugador):
        pygame.sprite.Sprite.__init__(self)
        self.m=m
        self.accion = 2
        self.con=0
        self.lim = [7,7,5]
        self.image = self.m[self.con][self.accion]
        self.vidas = 3
        self.rect=self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.actualizacion = pygame.time.get_ticks()
        self.actualizacion_spawn = pygame.time.get_ticks()

        #self.enemigos = pygame.sprite.Group()

        imagen_enemigo2 = pygame.image.load('enemigo2.png')
        self.recorte_enemigo2=Recortar(imagen_enemigo2,66,40,0)

        imagenenemigo1 = pygame.image.load('enemigo1.png')
        self.recorte_enemigo1=Recortar(imagenenemigo1,64,64,0)

        self.jugador = jugador

        self.tipo = tipo
        self.cont = 0

    def mov(self):
        if self.actualizacion + 100 < pygame.time.get_ticks():
            self.image = self.m[self.con][self.accion]
            if self.con < self.lim[self.accion]:
                self.con +=1
            else:
                self.con = 0
            self.actualizacion = pygame.time.get_ticks()

    def kill(self):
        pygame.sprite.Sprite.kill(self)

    def rem(self):
        if self.con < self.lim[self.accion]:
            self.con +=1
            self.image = self.m[self.con][self.accion]
        if self.con == 5:
            self.kill()

    def update(self):
        if self.vidas == 0:
            self.rem()
        else:
            self.mov()

class Modificadores(pygame.sprite.Sprite):
    jugador = None
    def __init__(self,pos,imagen,tipo):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagen
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.tipo = tipo
    def kill(self):
        pygame.sprite.Sprite.kill(self)
    def mejora_proyectil(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_mejora_proyectil.play()
            self.kill()
            j.obtener_mejora = True
            j.proyectil_tipo = 1

    def mejora_vida(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_vida.play()
            self.kill()
            j.vidas += 1

    def pocion_damage(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_pocion.play()
            self.kill()
            j.vidas -= 1


    def pocion_slow(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_pocion.play()
            self.kill()
            j.movimiento = 2
            j.mejora_pocion = self.image
            j.obtener_pocion = True

    def pocion_speed(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_pocion.play()
            self.kill()
            j.movimiento = 8
            j.csalto = 12
            j.mejora_pocion = self.image
            j.obtener_pocion = True

    def pocion_snormal(self):
        hit = pygame.sprite.collide_rect(self, self.jugador)
        if hit:
            j.sonido_pocion.play()
            self.kill()
            j.movimiento = 5
            j.csalto = 8
            j.mejora_pocion = self.image
            j.obtener_pocion = True


    def update(self):
        if self.tipo == 1:
            self.mejora_proyectil()
        if self.tipo == 2:
            self.mejora_vida()
        if self.tipo == 3:
            self.pocion_damage()
        if self.tipo == 4:
            self.pocion_slow()
        if self.tipo == 5:
            self.pocion_speed()
        if self.tipo == 6:
            self.pocion_snormal()


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
        #self.enemigo1 = pygame.image.load("enemigo1.png")
        #info = background.get_rect()
        self.fx = 0
        self.fy = -397
        self.fvelx = 0
        self.fvely = 0
        self.limderecha = ANCHO-200
        self.limizq = 100
        self.limabajo = ALTO-100
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

    def enscenario_desplazar_y(self,desplazar_y):
        self.fy += desplazar_y

        #Movemos todas las listas de sprites
        for plataforma in self.listade_bloques:
            plataforma.rect.y += desplazar_y


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
                '''if d == 'piso movil':
                    fl = int(self.mapa.get('m','fil'))
                    cl = int(self.mapa.get('m','col'))
                    bm = Bloque_Movimiento([c*32,f*32],[32,32],self.mM[fl][cl])
                    bm.limite_inferior = bm.rect.centery - 100
                    bm.limite_superior = bm.rect.centery + 100
                    #print 'limite_inferior:',bm.limite_inferior,'limite superior',bm.limite_superior
                    #print 'bottom:',bm.rect.bottom,  'top',bm.rect.top
                    bm.vely = 2
                    bm.jugador = self.jugador
                    self.listade_bloques.add(bm)'''
                c+=1
            f += 1
            c = 0

if __name__ == '__main__':
    '''Programa principal'''
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])

    musica_juego=pygame.mixer.Sound('audio/musica_juego.ogg')
    musica_juego.set_volume(0.9)
    musica_juego.play()

    imagenProtagonista = pygame.image.load('personajev2.png')
    #info = imagenProtagonista.get_rect()
    mJ = Recortar(imagenProtagonista,32,56,3) #Matriz sprite Jugador
    j=Jugador(mJ)
    jugadores = pygame.sprite.Group()
    jugadores.add(j)

    vitas = pygame.sprite.Group()
    enemigos1 = pygame.sprite.Group()
    imagenenemigo1 = pygame.image.load('enemigo1.png')
    recorte_enemigo1=Recortar(imagenenemigo1,64,64,0)
    enemigo1A = Enemigo1(recorte_enemigo1,150,670)
    enemigo1A.jugador = j
    enemigo1B = Enemigo1(recorte_enemigo1,120,420)
    enemigo1B.jugador = j
    enemigo1C = Enemigo1(recorte_enemigo1,1500,850)
    enemigo1C.jugador = j
    enemigo1D = Enemigo1(recorte_enemigo1,2220,750)
    enemigo1D.jugador = j
    enemigo1E = Enemigo1(recorte_enemigo1,2450,750)
    enemigo1E.jugador = j
    enemigo1F = Enemigo1(recorte_enemigo1,2150,600)
    enemigo1F.jugador = j
    enemigo1G = Enemigo1(recorte_enemigo1,2500,600)
    enemigo1G.jugador = j
    enemigos1.add(enemigo1A)
    enemigos1.add(enemigo1B)
    enemigos1.add(enemigo1C)
    enemigos1.add(enemigo1D)
    enemigos1.add(enemigo1E)
    enemigos1.add(enemigo1F)
    enemigos1.add(enemigo1G)


    enemigos2 = pygame.sprite.Group()
    imagenenemigo2 = pygame.image.load('enemigo2.png')
    recorte_enemigo2=Recortar(imagenenemigo2,66,40,0)
    enemigo2A = Enemigo2(recorte_enemigo2,1000,790)
    enemigo2A.jugador = j
    enemigos2.add(enemigo2A)
    enemigo2B = Enemigo2(recorte_enemigo2,1500,730)
    enemigo2B.jugador = j
    enemigos2.add(enemigo2B)
    enemigo2C = Enemigo2(recorte_enemigo2,1700,730)
    enemigo2C.jugador = j
    enemigos2.add(enemigo2C)
    enemigo2D = Enemigo2(recorte_enemigo2,2000,505)
    enemigo2D.jugador = j
    enemigos2.add(enemigo2D)


    proyectil=pygame.sprite.Group()
    proyectil_j1 = pygame.image.load('proyectil_j1.png')
    proyectil_j2 = pygame.image.load('proyectil_j2.png')

    proyectil1_j1 = pygame.image.load('proyectil2_j1.png')
    proyectil1_j2 = pygame.image.load('proyectil2_j2.png')
    proyectil_enemigo=pygame.sprite.Group()

    modificadores = pygame.sprite.Group()
    item_mejora = Modificadores([325,275],proyectil_j2,1)
    item_mejora.jugador = j
    modificadores.add(item_mejora)

    vida_imagen = pygame.image.load('vida.png')
    item_vida = Modificadores([1325,790],vida_imagen,2)
    item_vida.jugador = j
    item_vida2 = Modificadores([2550,500],vida_imagen,2)
    item_vida2.jugador = j
    modificadores.add(item_vida)
    modificadores.add(item_vida2)

    imagen_pocion_damage = pygame.image.load('pocion_damage.png')
    item_pocion_damage = Modificadores([1000,900],imagen_pocion_damage,3)
    item_pocion_damage.jugador = j
    modificadores.add(item_pocion_damage)

    imagen_pocion_slow = pygame.image.load('pocion_slow.png')
    item_pocion_slow = Modificadores([1600,900],imagen_pocion_slow,4)
    item_pocion_slow.jugador = j
    modificadores.add(item_pocion_slow)

    imagen_pocion_speed = pygame.image.load('pocion_speed.png')
    item_pocion_speed = Modificadores([130,705],imagen_pocion_speed,5)
    item_pocion_speed.jugador = j
    item_pocion_speed2 = Modificadores([2000,900],imagen_pocion_speed,5)
    item_pocion_speed2.jugador = j
    modificadores.add(item_pocion_speed)
    modificadores.add(item_pocion_speed2)

    imagen_pocion_snormal = pygame.image.load('pocion_snormal.png')
    item_pocion_snormal = Modificadores([560,755],imagen_pocion_snormal,6)
    item_pocion_snormal.jugador = j
    item_pocion_snormal2 = Modificadores([1550,735],imagen_pocion_snormal,6)
    item_pocion_snormal2.jugador = j
    modificadores.add(item_pocion_snormal)
    modificadores.add(item_pocion_snormal2)


    portales = pygame.sprite.Group()
    portal_mago = pygame.image.load('portal_mago.png')
    recorte_portal_mago=Recortar(portal_mago,32,64,0)
    portal_magos = Spawner(recorte_portal_mago,1800,500,0,j)

    portal_arana = pygame.image.load('portal_arana.png')
    recorte_arana=Recortar(portal_arana,32,64,0)
    portal_aranas = Spawner(recorte_arana,2200,500,1,j)

    #portales.add(portal_magos)
    #portales.add(portal_aranas)
    opcion = 1

    fin = False
    reloj=pygame.time.Clock()
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    opcion -=1

                if event.key == pygame.K_DOWN:
                    opcion +=1

                if event.key == pygame.K_RETURN:
                    if opcion == 1:
                        fin = True
                    elif opcion == 2:
                        sys.exit()

        #nivel.update()
        #nivel.escenario_desplazar()
        Menu(opcion)
        pygame.display.flip()

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
                    j.velx=j.movimiento
                    j.accion = 0
                    j.derecha = True
                if event.key == pygame.K_LEFT:
                    j.velx=-j.movimiento
                    j.accion = 1
                    j.derecha = False
                if event.key == pygame.K_UP:
                    #j.velx=0
                    j.Saltar()

                '''if event.key == pygame.K_DOWN:
                    j.velx=0
                    j.vely=5'''
                if event.key == pygame.K_x:
                    #golpe
                    j.accion=2
                    j.con = 0
                    if j.derecha == True:
                        disparo=Proyectil(j.pos(),5,proyectil1_j1)
                        disparo.rect.x += 20
                        j.accion=2
                        j.con = 0
                    else:
                        disparo=Proyectil(j.pos(),-5,proyectil1_j2)
                        disparo.rect.x -= 20
                        j.accion=3
                        j.con = 0
                    proyectil.add(disparo)
                if event.key == pygame.K_c:
                    #patada
                    if j.derecha == True:
                        if j.proyectil_tipo == 0:
                            disparo=Proyectil(j.pos(),5,proyectil1_j1)
                            j.sonido_proyectil.play()
                        else:
                            disparo=Proyectil(j.pos(),5,proyectil_j1)
                            j.sonido_proyectil.play()
                        disparo.rect.x += 20
                        j.accion=2
                        j.con = 0
                    else:
                        if j.proyectil_tipo == 0:
                            disparo=Proyectil(j.pos(),-5,proyectil1_j2)
                            j.sonido_proyectil.play()
                        else:
                            disparo=Proyectil(j.pos(),-5,proyectil_j2)
                            j.sonido_proyectil.play()

                        disparo.rect.x -= 20
                        j.accion=3
                        j.con = 0
                    proyectil.add(disparo)

                if event.key == pygame.K_p:
                    '''Pause'''
                    pausa = True
                    while pausa:
                        Pausa()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                pausa = False



            if event.type == pygame.KEYUP:
                j.velx=0
                nivel.fvelx = 0
                nivel.fvely = 0

        '''Vemos si le quedan vidas'''
        if j.vidas == 0:
            GameOver()
            pygame.time.delay(1500)
            fin = True

        '''Fin de juego'''
        if j.cont_enemigos == 11:
            Congratulations()
            pygame.time.delay(1500)
            fin = True



        # Si el jugador se aproxima a la derecha
        if j.rect.x > nivel.limderecha:
            diff = j.rect.x - nivel.limderecha
            j.rect.x = nivel.limderecha
            nivel.enscenario_desplazar(-diff)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.x += -diff
            for enemigo_2 in enemigos2:
                enemigo_2.rect.x += -diff
            for proyectil1_j in proyectil:
                proyectil1_j.rect.x += -diff
            for proyectil1_e in proyectil_enemigo:
                proyectil1_e.rect.x += -diff
            for port in portales:
                port.rect.x += -diff
            for mod in modificadores:
                mod.rect.x += -diff
        # Si el jugador se aproxima a la derecha
        if j.rect.x < nivel.limizq:
            diff = nivel.limizq - j.rect.x
            j.rect.x = nivel.limizq
            nivel.enscenario_desplazar(diff)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.x += diff
            for enemigo_2 in enemigos2:
                enemigo_2.rect.x += diff
            for proyectil1_j in proyectil:
                proyectil1_j.rect.x += diff
            for proyectil1_e in proyectil_enemigo:
                proyectil1_e.rect.x += diff
            for port in portales:
                port.rect.x += diff
            for mod in modificadores:
                mod.rect.x += diff

        #sube
        if j.rect.top > nivel.limabajo:
            dif = j.rect.y - nivel.limabajo
            j.rect.y = nivel.limabajo
            nivel.enscenario_desplazar_y(-dif)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.y += -dif
            for enemigo_2 in enemigos2:
                enemigo_2.rect.y += -dif
            for proyectil1_j in proyectil:
                proyectil1_j.rect.y += -dif
            for proyectil1_e in proyectil_enemigo:
                proyectil1_e.rect.y += -dif
            for port in portales:
                port.rect.y += -dif
            for mod in modificadores:
                mod.rect.y += -dif

		#baja
        if j.rect.top < nivel.limarriba:
            dif = nivel.limarriba - j.rect.y
            j.rect.y = nivel.limarriba
            nivel.enscenario_desplazar_y(dif)
            for enemigo_1 in enemigos1:
                enemigo_1.rect.y += dif
            for enemigo_2 in enemigos2:
                enemigo_2.rect.y += dif
            for proyectil1_j in proyectil:
                proyectil1_j.rect.y += dif
            for proyectil1_e in proyectil_enemigo:
                proyectil1_e.rect.y += dif
            for port in portales:
                port.rect.y += dif
            for mod in modificadores:
                mod.rect.y += dif


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
                j.sonido_jugador.play()
                j.vidas -= 1

        #proyectil en enemigo1
        for e_fantasma in enemigos1:
            ls_enemigo = pygame.sprite.spritecollide(e_fantasma,proyectil,True)
            for proyectil_jugador in ls_enemigo:
                proyectil.remove(proyectil_jugador)
                if j.proyectil_tipo == 0:
                    e_fantasma.vidas -= 1
                    e_fantasma.sonido_enemigo1.play()
                else:
                    e_fantasma.vidas = 0
                if e_fantasma.vidas == 0:
                    e_fantasma.estado = False
                    enemigos1.remove(e_fantasma)
                    j.cont_enemigos += 1
                    #print(j.cont_enemigos)
        #proyectil en enemigo2
        for e_arana in enemigos2:
            ls_enemigo2 = pygame.sprite.spritecollide(e_arana,proyectil,True)
            for proyectil_jugador in ls_enemigo2:
                proyectil.remove(proyectil_jugador)
                if j.proyectil_tipo == 0:
                    e_arana.vidas -= 1
                    e_arana.sonido_damage.play()
                else:
                    e_arana.vidas = 0
                if e_arana.vidas == 0:
                    enemigos2.remove(e_arana)
                    e_arana.sonido_damage2.play()
                    j.cont_enemigos += 1
                    #print(j.cont_enemigos)
        #proyectil en portal/s.pawner
        for e_portal in portales:
            ls_portales = pygame.sprite.spritecollide(e_portal,proyectil,True)
            for proyectil_jugador in ls_portales:
                proyectil.remove(proyectil_jugador)
                e_portal.vidas -= 1
                if e_portal.vidas == 0:
                    e_portal.accion = 2
                    e_portal.con = 0

        #Zona de dibujado
        nivel.draw(pantalla)
        jugadores.draw(pantalla)
        proyectil.draw(pantalla)
        proyectil_enemigo.draw(pantalla)
        enemigos1.draw(pantalla)
        enemigos2.draw(pantalla)
        portales.draw(pantalla)
        modificadores.draw(pantalla)
        #refresco de pantalla
        jugadores.update()
        proyectil.update()
        proyectil_enemigo.update()
        enemigos1.update()
        enemigos2.update()
        portales.update()
        modificadores.update()

        #nivel.update()
        #nivel.escenario_desplazar()
        pygame.display.flip()
        reloj.tick(30)
