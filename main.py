import pygame
from sys import exit
from classes import *
import json

pygame.init()
screen = pygame.display.set_mode((1280, 720), )  #pygame.FULLSCREEN
pygame.display.set_caption("Placeholder title")
clock = pygame.time.Clock()
game_active = False

test_font = pygame.font.Font(None, 50)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    game_active = True

  if game_active:
  	pass
  else:
  	pass

  pygame.display.update()
  clock.tick(60)
