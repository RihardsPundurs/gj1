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

with open('devlvl.json') as json_file:
  python_dict = json.load(json_file)
  
print(python_dict.get('Level'))

text_surf = test_font.render("Press ENTER to play", False, "White")
text_rect = text_surf.get_rect(center=(640, 360))

bg_surf = pygame.image.load("resources/background.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))
bg_rect = bg_surf.get_rect(center=(640, 360))

player = pygame.sprite.GroupSingle()
player.add(Player())

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

  keys = pygame.key.get_pressed()
  if keys[pygame.K_RETURN]:
    game_active = True

  if game_active:
    screen.blit(bg_surf, bg_rect)
	player.draw(screen)
	player.update()
  else:
    screen.blit(bg_surf, bg_rect)
    screen.blit(text_surf, text_rect)

  pygame.display.update()
  clock.tick(60)
