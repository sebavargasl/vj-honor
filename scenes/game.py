'''
Hola este es modulo game,
este modulo manejara la escena donde ocurre nuestro juego
'''

if __name__ == "__main__": # Solo para que no ejecutes este archivo
    import sys
    print(
        "\033[38;2;255;0;0mESTE MODULO NO DEBE EJECUTARSE. EJECUTAR main.py\033[0m\n"
        * 3
    )
    sys.exit()

import pygame

from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT)

from elements.jorge import Player

from elements.bug import Enemy

from elements.mira import Mirilla

from scenes.muerte import gameOver

from elements.cronometro import Tiempo

from scenes.inicio import pantalla_inicio

from elements.enemigo2 import Enemy2

from elements.enemigo3 import Enemy3

from elements.velocidad import Speed
powerups=pygame.sprite.Group()

from elements.vidaextra import Life

from elements.boss import Boss

from scenes.victoria import pantalla_victoria



def gameLoop():
    ''' iniciamos los modulos de pygame'''
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    fuente=pygame.font.SysFont("impact",30)
    mensaje_vidas=""
    vidas_tiempo=0
    mensaje_velocidad=""
    velocidad_tiempo=0

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    ''' 2.- crear el objeto pantalla'''
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    accion=pantalla_inicio()
    if accion=="salir":
        pygame.quit()
        return
    
    if pygame.mixer.get_init():
        pygame.mixer.music.load("assets/musica/musica.mp3")
        pygame.mixer.music.play(-1)

    sonido_powerup=pygame.mixer.Sound("assets/musica/powerup.mp3")
    sonido_disparo=pygame.mixer.Sound("assets/musica/disparo.mp3")
    sonido_victoria=pygame.mixer.Sound("assets/musica/victoria.mp3")

    ''' Creamos y editamos la ventana de pygame (escena) '''
    ''' 1.-definir el tamaño de la ventana'''
    
    background_image = pygame.image.load("assets/pixelBackground.jpg").convert()

    ''' Preparamos el gameloop '''
    #creamos las imagenes de los corazones, convert_alpha le quita el fondo negro a la imagen
    corazon=pygame.image.load("assets/corazon.png").convert_alpha()
    corazon=pygame.transform.scale(corazon,(50,50))

    ''' 1.- creamos el reloj del juego'''

    clock = pygame.time.Clock()
    ''' 2.- generador de enemigos'''

    ADDENEMY1 = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY1, 600)

    ADDENEMY2 = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMY2, 4500)

    ADDENEMY3 = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDENEMY3, 3000)

    ADDPOWER=pygame.USEREVENT+4
    pygame.time.set_timer(ADDPOWER, 6000)

    ADDLIFE=pygame.USEREVENT+5
    pygame.time.set_timer(ADDLIFE,9000)

    ''' 3.- creamos la instancia de jugador'''
    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

    ''' 4.- contenedores de enemigos y jugador'''
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    #creacion de la mira
    mira=Mirilla(SCREEN_WIDTH,SCREEN_HEIGHT)
    all_sprites.add(mira)

    #creamos el cronometro
    cronometro= Tiempo()

    #creamos el puntaje
    puntaje=0
    letra_puntaje= pygame.font.SysFont("algerian", 25)

    #variables para ver cuando aparece el boss
    boss=0
    aparicion_boss=False
    muerte_boss=False
    tiempo_victoria=0

    ''' hora de hacer el gameloop '''
    # variable booleana para manejar el loop
    running = True

    # loop principal del juego

    while running:

        screen.blit(background_image, [0, 0])
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        # POR HACER (2.5): Pintar proyectiles en pantalla
        for projectile in player.projectiles:
            screen.blit(projectile.surf,projectile.rect)
        
        #tenemos en pantalla la cantidad de vidas que tiene el jugador, las imagenes las separamos entre 50 
        for i in range(player.vidas):
            screen.blit(corazon, (10+i*50,10))
        
        # POR HACER (2.5): Eliminar bug si colisiona con proyectil
        #tomamos el sistema de eliminaciones y lo vamos sumando al puntaje cada vez que matamos a un enemigo
        eliminaciones=pygame.sprite.groupcollide(enemies,player.projectiles,True,True)
        puntaje+=len(eliminaciones)


        #si se llega a score 100 y aun no hay boss
        if puntaje>=100 and aparicion_boss==False:
            boss= Boss(SCREEN_WIDTH, SCREEN_HEIGHT, player)
            all_sprites.add(boss)
            aparicion_boss=True
        
        #si aparece el boss, spawnean menos enemigos
        if aparicion_boss==True:
            pygame.time.set_timer(ADDENEMY1,2000)
            pygame.time.set_timer(ADDENEMY2,2000)
            pygame.time.set_timer(ADDENEMY3,2000)
        
 

        
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        powerups.update()
        #actualizar la mira con el movimiento
        mira.update()
        if player.invencible and pygame.time.get_ticks()>player.invencible_hasta:
            player.invencible=False
        if player.chico != 0 and pygame.time.get_ticks()>player.chico:
            a, b = player.normal
            player.surf=pygame.transform.scale(player.imagen,(a,b))
            centro=player.rect.center
            player.rect=player.surf.get_rect(center=centro)
            player.chico=0
        
        if aparicion_boss==True and boss!=0:
            boss.update()
            screen.blit(boss.surf,boss.rect)
            if player.rect.colliderect(boss.rect) and player.invulnerable==False:
                player.perder_vida()
                player.invulnerable=True
                player.tiempo_invulnerable=30
                
                if player.vidas<=0:
                    #si tiene 0 vidad se termina el juego
                    player.kill()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/perder/perder.mp3")
                    pygame.mixer.music.play(-1)
                    running = False
                #si se muere, se empieza el loop de la escena de muerte
                    accion2=gameOver()
                    if accion2=="jugar":
                        #si se quiere volver a jugar, debemos reiciar los datos
                        player=Player(SCREEN_WIDTH,SCREEN_HEIGHT)
                        enemies.empty()
                        all_sprites.empty()
                        all_sprites.add(player)
                        all_sprites.add(mira)
                        boss=0
                        aparicion_boss=False
                        muerte_boss=False
                        tiempo_victoria=0
                        puntaje=0
                        cronometro=Tiempo()
                        running=True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("assets/musica/musica.mp3")
                        pygame.mixer.music.play(-1)
                    else:
                        running=False

            for disparo in player.projectiles:
                if boss.rect.colliderect(disparo.rect):
                    boss.perder_vida()
                    disparo.kill()
                    if boss.vidas==0:
                        boss.kill()
                        boss=0
                        muerte_boss=True
                        tiempo_victoria=pygame.time.get_ticks()
            
        if muerte_boss==True:
            if pygame.time.get_ticks()-tiempo_victoria>=4000:
                accion3= pantalla_victoria()
                sonido_victoria.play()
                if accion3=="jugar":
                    player=Player(SCREEN_WIDTH,SCREEN_HEIGHT)
                    enemies.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(mira)
                    boss=0
                    aparicion_boss=False
                    muerte_boss=False
                    tiempo_victoria=0
                    puntaje=0
                    cronometro=Tiempo()
                    running=True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/musica/musica.mp3")
                    pygame.mixer.music.play(-1)
                else:
                    running=False

    


        choque= pygame.sprite.spritecollideany(player, enemies)
        if choque:
            #matamos al enemigo con el que choca y restamos una vida
            choque.kill()
            player.perder_vida()

            if player.vidas<=0:
                #si tiene 0 vidad se termina el juego
                player.kill()
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/perder/perder.mp3")
                pygame.mixer.music.play(-1)
                running = False
            #si se muere, se empieza el loop de la escena de muerte
                accion2=gameOver()
                if accion2=="jugar":
                    #si se quiere volver a jugar, debemos reiciar los datos
                    player=Player(SCREEN_WIDTH,SCREEN_HEIGHT)
                    enemies.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(mira)
                    boss=0
                    aparicion_boss=False
                    muerte_boss=False
                    tiempo_victoria=0
                    puntaje=0
                    cronometro=Tiempo()
                    running=True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("assets/musica/musica.mp3")
                    pygame.mixer.music.play(-1)
                else:
                    running=False
        
        choque2= pygame.sprite.spritecollideany(player, powerups)
        if choque2:
            if isinstance(choque2,Speed):
                player.speed_time=pygame.time.get_ticks()+5000
                player.velocidades_recolectadas += 1
                if player.velocidades_recolectadas==5:
                    player.velocidades_recolectadas=0
                    player.invencible=True
                    player.invencible_hasta=pygame.time.get_ticks()+5000
                    mensaje_velocidad="5 boosts de velocidad: Inmune por 5 segundos!"
                    velocidad_tiempo=pygame.time.get_ticks()+3000
            elif isinstance(choque2, Life):
                player.vidas += 1
                player.vidas_recolectadas += 1
                if player.vidas_recolectadas==3:
                    player.vidas_recolectadas=0
                    player.chico=pygame.time.get_ticks()+5000
                    a, b=player.normal
                    chico=pygame.transform.scale(player.imagen,(a//2,b//2))
                    player.surf=chico
                    centro=player.rect.center
                    player.rect=player.surf.get_rect(center=centro)
                    mensaje_vidas="3 vidas extra: Pequeño por 5 segundos!"
                    vidas_tiempo=pygame.time.get_ticks()+3000
            sonido_powerup.play()
            choque2.kill()
            
        cronometro.imagen(screen)

        #dibujamos el puntaje abajo de los corazones
        score=letra_puntaje.render(f"Score: {puntaje}", True, (255,255,255))
        screen.blit(score, (10, 60))

        if pygame.time.get_ticks()<vidas_tiempo and mensaje_vidas:
            texto=fuente.render(mensaje_vidas,True,(255,0,255))
            screen.blit(texto,(SCREEN_WIDTH//2-texto.get_width()//2,10))
        
        if pygame.time.get_ticks()<velocidad_tiempo and mensaje_velocidad:
            texto2=fuente.render(mensaje_velocidad,True,(128,0,128))
            screen.blit(texto2,(SCREEN_WIDTH//2-texto2.get_width()//2,SCREEN_HEIGHT-40))

        pygame.display.flip()
        
        # iteramos sobre cada evento en la cola
        for event in pygame.event.get():
            # se presiono una tecla?
            if event.type == KEYDOWN:
                # era la tecla de escape? -> entonces terminamos
                if event.key == K_ESCAPE:
                    running = False

            # fue un click al cierre de la ventana? -> entonces terminamos
            elif event.type == QUIT:
                running = False
            
            elif event.type == ADDENEMY1:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == ADDENEMY2:
                new_enemy = Enemy2(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type == ADDENEMY3:
                new_enemy = Enemy3(SCREEN_WIDTH, SCREEN_HEIGHT)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            
            elif event.type==ADDPOWER:
                s=Speed(SCREEN_WIDTH,SCREEN_HEIGHT)
                powerups.add(s)
                all_sprites.add(s)
            
            elif event.type==ADDLIFE:
                v=Life(SCREEN_WIDTH,SCREEN_HEIGHT)
                powerups.add(v)
                all_sprites.add(v)
            
            # POR HACER (2.4): Agregar evento disparo proyectil
            elif event.type==pygame.MOUSEBUTTONDOWN:
                player.shoot(pygame.mouse.get_pos())
                sonido_disparo.play()


        clock.tick(40)
