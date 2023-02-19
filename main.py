import pygame
from sys import exit
from classes import *
import json

pygame.init()
screen = pygame.display.set_mode((1280, 720), )  #pygame.FULLSCREEN
pygame.display.set_caption("Placeholder title")
clock = pygame.time.Clock()
game_active = False


def collision_sprite():
	for entity in pygame.sprite.spritecollide(player.sprite,level_groups,False):
		dist_bottom = player.sprite.rect.bottom - entity.rect.top
		dist_right = player.sprite.rect.right - entity.rect.left
		dist_left = entity.rect.right - player.sprite.rect.left
		dist_top = entity.rect.bottom - player.sprite.rect.top

		bottom_side = dist_bottom < dist_right and dist_bottom < dist_left
		top_side = dist_top < dist_right and dist_top < dist_left
		right_side = dist_right <= dist_bottom and dist_right <= dist_top
		left_side = dist_left <= dist_bottom and dist_left <= dist_top
		collision = bottom_side or top_side or right_side or left_side

		if entity in blocks.sprites():
			if right_side:
				for sprite in everything:
					sprite.rect.x += dist_right
				player.sprite.rect.right = entity.rect.left
				player.sprite.velocity = 0
			elif left_side:
				for sprite in everything:
					sprite.rect.x -= dist_left
				player.sprite.rect.left = entity.rect.right
				player.sprite.velocity = 0
			# elif top_side:
			# 	for sprite in everything:
			# 		sprite.rect.y -= dist_top
			# 	player.sprite.rect.top = entity.rect.bottom
			# 	player.sprite.gravity = 0
			elif bottom_side:
				for sprite in everything:
					sprite.rect.y += dist_bottom
				player.sprite.rect.bottom = entity.rect.top
				player.sprite.gravity = 0
				player.sprite.on_ground = True
			else:
				player.sprite.on_ground = False

		if entity in spikes.sprites():
			global game_active
			game_active = False

		if entity in platforms.sprites():
			if bottom_side:
				if player.sprite.gravity >= 0:
					if player.sprite.gravity == 0 and not player.sprite.rect.bottom > entity.rect.top:
						for sprite in everything:
							sprite.rect.y += dist_bottom
						player.sprite.rect.bottom = entity.rect.top
						player.sprite.gravity = 0
						player.sprite.on_ground = True

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
blocks.add(Block([640, 700]))
blocks.add(Block([940, 700]))
blocks.add(Block([340, 700]))
blocks.add(Block([340, 400]))
blocks.add(Block([640, 150]))

spikes = pygame.sprite.Group()
spikes.add(Spike([1240, 700]))

platforms = pygame.sprite.Group()
platforms.add(Platform([940, 400]))

level_groups = pygame.sprite.Group()
level_groups.add(blocks)
level_groups.add(spikes)
level_groups.add(platforms)

everything = pygame.sprite.Group()
everything.add(player)
everything.add(blocks)
everything.add(platforms)
everything.add(spikes)

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
		collision_sprite()
		screen.blit(bg_surf, bg_rect)
		player.draw(screen)
		player.update()
		level_groups.draw(screen)
		level_groups.update()
	else:
		screen.blit(bg_surf, bg_rect)
		screen.blit(text_surf, text_rect)

	pygame.display.update()
	clock.tick(60)
