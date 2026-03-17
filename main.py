import os, sys
import pygame
from lib import Peloton, Destinos

pygame.init()
WIDTH, HEIGHT = 960, 540 #1920//2, 1080//2
ventana = pygame.display.set_mode((WIDTH, HEIGHT))
reloj = pygame.time.Clock()
fondo = pygame.image.load(f"imagenes/fondo.png")
fondo = pygame.transform.smoothscale(fondo, (960, 540))

tmp = False
msj = iter(Destinos())
destino = next(msj)
peloton = Peloton(3000, ventana, destino)

musica = "whats-going-on-272859.mp3"
if os.path.exists(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not peloton.en_movimiento:
            tmp = True

        if event.type == pygame.MOUSEBUTTONUP and tmp:
            tmp = False
            peloton.cargar_destinos(next(msj))

    reloj.tick(20)
    ventana.fill((255,255,255))
    ventana.blit(fondo, (0,0))

    peloton.mover()
    peloton.mostrar(ventana)

    pygame.display.update()