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
blocks = pygame.sprite.Group()
blocks.add(Block())

everything = pygame.sprite.Group()
everything.add(player)
everything.add(blocks)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	if player.sprites()[0].rect.x > 639:
		for sprite in everything:
			sprite.rect.x -= player.sprites()[0].velocity

	if player.sprites()[0].rect.x < 641:
		for sprite in everything:
			sprite.rect.x -= player.sprites()[0].velocity

	if player.sprites()[0].rect.y < 321:
		for sprite in everything:
			sprite.rect.y -= player.sprites()[0].gravity

	if player.sprites()[0].rect.y > 319:
		for sprite in everything:
			sprite.rect.y -= player.sprites()[0].gravity

	keys = pygame.key.get_pressed()
	if keys[pygame.K_RETURN]:
		game_active = True

	if game_active:
		screen.blit(bg_surf, bg_rect)
		player.draw(screen)
		player.update()
		blocks.draw(screen)
		blocks.update()
	else:
		screen.blit(bg_surf, bg_rect)
		screen.blit(text_surf, text_rect)

	pygame.display.update()
	clock.tick(60)
