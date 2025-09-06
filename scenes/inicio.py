import pygame

from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)

from elements.jorge import Player

from elements.bug import Enemy

from elements.mira import Mirilla


def pantalla_inicio():
    pygame.init()
    #fuentes de la pantalla
    letra_inicio=pygame.font.SysFont("Algerian", 40)
    letra_titulo=pygame.font.SysFont("Algerian", 70)

    #botones de inicio y cerrar
    boton_jugar=pygame.Rect(1000/2-100, 700/2-50, 200, 50)
    boton_cerrar=pygame.Rect(1000/2-100, 700/2+50, 200, 50)

    texto_jugar= letra_inicio.render("JUGAR",True,(255,255,255))
    texto_cerrar=letra_inicio.render("SALIR",True,(255,255,255))
    texto_titulo=letra_titulo.render("JORGE V/S BUGS", True, (255,255,255))

    ''' Creamos y editamos la ventana de pygame (escena) '''
    ''' 1.-definir el tamaño de la ventana'''
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    ''' 2.- crear el objeto pantalla'''
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pantalla de inicio")


    ''' Preparamos el gameloop '''
    ''' 1.- creamos el reloj del juego'''

    clock = pygame.time.Clock()

    #creamos el loop siguiendo la misma logica, para cuando se omime escape o se cierra la ventana
    running=True
    accion=0
    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                running=False
                accion="salir"
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    running=False
                    accion="salir"
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    running=False
                    accion="jugar"
                elif boton_cerrar.collidepoint(event.pos):
                    running=False
                    accion="salir"
        
        #dibujamos la pantalla
        screen.fill((0,0,0))
        screen.blit(texto_titulo,(SCREEN_WIDTH//2-texto_titulo.get_width()//2, 200))

        pygame.draw.rect(screen, (30,255,0),boton_jugar)
        pygame.draw.rect(screen, (255,0,0),boton_cerrar)
        screen.blit(texto_jugar,(boton_jugar.centerx-texto_jugar.get_width()//2, boton_jugar.centery-texto_jugar.get_height()//2))

        screen.blit(texto_cerrar,(boton_cerrar.centerx-texto_cerrar.get_width()//2, boton_cerrar.centery-texto_cerrar.get_height()//2))
        
        pygame.display.flip()

        clock.tick(40)
    
    return accion