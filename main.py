import pygame
from sys import exit
from classes import *
import json
import time
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720), )  #pygame.FULLSCREEN
pygame.display.set_caption("Placeholder title")
clock = pygame.time.Clock()
game_active = False
last_surface = None
end_time = None
start_time = None
win_bool = False

def collision_sprite():
	global last_surface
	total_list = []
	for list_object in pygame.sprite.spritecollide(player.sprite,level_groups,False):
		total_list.append(list_object)
	total_list.append(last_surface)
	try:
		for entity in total_list:
			dist_bottom = player.sprite.rect.bottom - entity.rect.top
			dist_right = player.sprite.rect.right - entity.rect.left
			dist_left = entity.rect.right - player.sprite.rect.left
			dist_top = entity.rect.bottom - player.sprite.rect.top

			bottom_side = dist_bottom < dist_right and dist_bottom < dist_left
			top_side = dist_top < dist_right and dist_top < dist_left
			right_side = dist_right <= dist_bottom and dist_right <= dist_top
			left_side = dist_left <= dist_bottom and dist_left <= dist_top
			collision = bottom_side or top_side or right_side or left_side
			# funny_list = total_list.pop(last_suface)
			# for entityf in funny_list:
			# print(total_list)
			# if not "<Block Sprite(in 3 groups)>" in total_list :#and not entity in platforms.sprites() and not entity in platforms_disappearing.sprites()
			# 	print("yahoo")
			# 	player.sprite.on_ground = False

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
				elif top_side:
					for sprite in everything:
						sprite.rect.y -= dist_top
					player.sprite.rect.top = entity.rect.bottom
					player.sprite.gravity = 0
				elif bottom_side:
					for sprite in everything:
						sprite.rect.y += dist_bottom
					player.sprite.rect.bottom = entity.rect.top
					player.sprite.gravity = 0
					last_suface = entity
					player.sprite.on_ground = True
				else:
					player.sprite.on_ground = False

			if entity in spikes.sprites():
				for checkpoint in checkpoints.sprites():
					if checkpoint.tag == player.sprite.respawn:
						dist_right = player.sprite.rect.right - checkpoint.rect.right
						dist_bottom = player.sprite.rect.bottom - checkpoint.rect.bottom
						player.sprite.rect.bottom = checkpoint.rect.bottom
						player.sprite.rect.right = checkpoint.rect.right

						for sprite in everything:
							sprite.rect.x += dist_right
							sprite.rect.y += dist_bottom
						break

			if entity in platforms.sprites():
				# if entity != last_suface:
				if -20 < dist_bottom < 20:
					player.sprite.plat = True
				if player.sprite.last_jump == False and player.sprite.plat == True:
					if player.sprite.gravity >= 0:
						for sprite in everything:
							sprite.rect.y += dist_bottom
						player.sprite.rect.bottom = entity.rect.top
						player.sprite.gravity = 0
						last_suface = entity
						player.sprite.on_ground = True
					else:
						player.sprite.on_ground = False
						player.sprite.plat = False

			if entity in platforms_disappearing.sprites():
				# if entity != last_suface:
				if -20 < dist_bottom < 20:
					player.sprite.plat = True
				if player.sprite.last_jump == False and player.sprite.plat == True and entity.active == True:
					if player.sprite.gravity >= 0:
						for sprite in everything:
							sprite.rect.y += dist_bottom
						player.sprite.rect.bottom = entity.rect.top
						player.sprite.gravity = 0
						last_suface = entity
						player.sprite.on_ground = True
						if entity.touch_time == None:
							if entity.wait_time == None:
								entity.touch_time = time.time()
					else:
						player.sprite.on_ground = False
						player.sprite.plat = False

			if entity in checkpoints.sprites():
				if player.sprite.respawn < entity.tag:
					player.sprite.respawn = entity.tag

			if entity in win_trigger.sprites():
				global win_bool, end_time, username_status
				if win_bool == False:
					end_time = time.time()
					win_bool = True
					username_status = True

			if entity in mushrooms.sprites():
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
				elif top_side:
					for sprite in everything:
						sprite.rect.y -= dist_top
					player.sprite.rect.top = entity.rect.bottom
					player.sprite.gravity = 0
				elif bottom_side:
					for sprite in everything:
						sprite.rect.y += dist_bottom
					player.sprite.rect.bottom = entity.rect.top
					player.sprite.gravity = -80
					last_suface = entity

			if entity in winds.sprites():
				if entity.direction == "right":
					player.sprite.velocity += entity.speed
				elif entity.direction == "left":
					player.sprite.velocity += -1*entity.speed
				elif entity.direction == "up":
					player.sprite.gravity += -1*entity.speed
				elif entity.direction == "down":
					player.sprite.gravity += entity.speed
			# if entity in platforms_moving.sprites():
			# 	# if entity != last_suface:
			# 	if -20 < dist_bottom < 20:
			# 		player.sprite.plat = True
			# 	if player.sprite.last_jump == False and player.sprite.plat == True:
			# 		if player.sprite.gravity >= 0:
			# 			for sprite in everything:
			# 				sprite.rect.y += dist_bottom
			# 			player.sprite.rect.bottom = entity.rect.top
			# 			player.sprite.gravity = 0
			# 			last_suface = entity
			# 			player.sprite.on_ground = True
			# 		else:
			# 			player.sprite.on_ground = False
			# 			player.sprite.plat = False
	except:
		pass

test_font = pygame.font.Font(None, 50)

with open('leaderboard.json', 'r') as json_file:
	leader_dict = json.load(json_file)
leader_sorted_list = sorted(leader_dict.items(), key=lambda x:x[1])
leaderboard = dict(leader_sorted_list)

print(leaderboard)

start_text_surf = test_font.render("Press ENTER to play", False, "Black")
start_text_rect = start_text_surf.get_rect(center=(640, 360))

input_text_surf = test_font.render("Enter username:", False, "Black")
input_text_rect = input_text_surf.get_rect(center=(640, 300))

username = ""
username_status = False
username_text_surf = test_font.render(username, False, "Black")
username_text_rect = username_text_surf.get_rect(center=(640, 360))

bg_surf = pygame.image.load("resources/background.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))
bg_rect = bg_surf.get_rect(center=(640, 360))

player = pygame.sprite.GroupSingle()
player.add(Player())

blocks = pygame.sprite.Group()
for i in range(20):
	blocks.add(Block([40 + i*150, 700]))
blocks.add(Block([640, 150]))

spikes = pygame.sprite.Group()
spikes.add(Spike([1240, 550]))

platforms = pygame.sprite.Group()
platforms.add(Platform([940, 400]))

# platforms_moving = pygame.sprite.Group()
# platforms_moving.add(Platform_moving([340, 400], 100
# 	))

platforms_disappearing = pygame.sprite.Group()
platforms_disappearing.add(Platform_disappearing([340, 400]))

checkpoints = pygame.sprite.Group()
checkpoints.add(Checkpoint([640, 550], 0))
checkpoints.add(Checkpoint([340, 550], 1))

win_trigger = pygame.sprite.GroupSingle()
win_trigger.add(Win_trigger([1540, 550]))

mushrooms = pygame.sprite.Group()
mushrooms.add(Mushroom([1840, 550]))

winds = pygame.sprite.Group()
winds.add(Wind([2140, 550], "up", 2))

level_groups = pygame.sprite.Group()
level_groups.add(blocks)
level_groups.add(spikes)
level_groups.add(platforms)
level_groups.add(platforms_disappearing)
level_groups.add(checkpoints)
level_groups.add(win_trigger)
level_groups.add(mushrooms)
level_groups.add(winds)
# level_groups.add(platforms_moving)

everything = pygame.sprite.Group()
everything.add(player)
everything.add(blocks)
everything.add(spikes)
everything.add(platforms)
everything.add(platforms_disappearing)
everything.add(checkpoints)
everything.add(win_trigger)
everything.add(mushrooms)
everything.add(winds)
# everything.add(platforms_moving)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.KEYDOWN and username_status == True:
			if event.key == pygame.K_BACKSPACE:
				username = username[:-1]
			if event.key == pygame.K_RETURN:
				username_status = False
				if username in leaderboard.keys():
					if end_time - start_time < leaderboard.get(username):
						leaderboard[username] = end_time - start_time
				else:
					leaderboard[username] = end_time - start_time

				with open('leaderboard.json','w') as outfile:
  					json.dump(leaderboard, outfile)
			else:
				username += event.unicode

	if player.sprites()[0].rect.x > 639:
		for sprite in everything:
			sprite.rect.x -= player.sprites()[0].velocity
			# if sprite in platforms_moving:
			# 	sprite.interval += player.sprites()[0].velocity

	if player.sprites()[0].rect.x < 641:
		for sprite in everything:
			sprite.rect.x -= player.sprites()[0].velocity
			# if sprite in platforms_moving:
			# 	sprite.interval += player.sprites()[0].velocity

	if player.sprites()[0].rect.y < 321:
		for sprite in everything:
			sprite.rect.y -= player.sprites()[0].gravity

	if player.sprites()[0].rect.y > 319:
		for sprite in everything:
			sprite.rect.y -= player.sprites()[0].gravity

	keys = pygame.key.get_pressed()
	if keys[pygame.K_RETURN] and game_active == False:
		game_active = True
		start_time = time.time()
		for checkpoint in checkpoints.sprites():
			if checkpoint.tag == player.sprite.respawn:
				dist_right = player.sprite.rect.right - checkpoint.rect.right
				dist_bottom = player.sprite.rect.bottom - checkpoint.rect.bottom
				player.sprite.rect.bottom = checkpoint.rect.bottom
				player.sprite.rect.right = checkpoint.rect.right

				for sprite in everything:
					sprite.rect.x += dist_right
					sprite.rect.y += dist_bottom
				break


	if game_active and not win_bool:
		collision_sprite()
		screen.blit(bg_surf, bg_rect)
		level_groups.draw(screen)
		level_groups.update()
		player.draw(screen)
		player.update()
		timer_text_surf = test_font.render(str(round(time.time()-start_time, 2)), False, "Black")
		timer_text_rect = timer_text_surf.get_rect(topleft=(60, 60))
		screen.blit(timer_text_surf, timer_text_rect)
	elif game_active and win_bool:
		collision_sprite()
		screen.blit(bg_surf, bg_rect)
		level_groups.draw(screen)
		player.draw(screen)
		username_text_surf = test_font.render(username, False, "Black")
		username_text_rect = username_text_surf.get_rect(center=(640, 360))
		timer_text_surf = test_font.render(str(round(end_time-start_time, 2)), False, "Black")
		timer_text_rect = timer_text_surf.get_rect(topleft=(60, 60))
		screen.blit(timer_text_surf, timer_text_rect)
		screen.blit(input_text_surf, input_text_rect)
		screen.blit(username_text_surf, username_text_rect)
	else:
		screen.blit(bg_surf, bg_rect)
		screen.blit(start_text_surf, start_text_rect)

	pygame.display.update()
	clock.tick(60)
