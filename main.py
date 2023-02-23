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
lb_active = False
height = 0
extra_time = None

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def collision_sprite():
	global last_surface
	total_list = []
	for list_object in pygame.sprite.spritecollide(player.sprite, level_groups, False):
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
						player.sprite.gravity = 0
						player.sprite.velocity = 0

						for sprite in everything:
							sprite.rect.x += dist_right
							sprite.rect.y += dist_bottom
						break

			if entity in platforms.sprites():
				if -20 < dist_bottom < 20:
					player.sprite.plat = True
				if player.sprite.last_jump == False and player.sprite.plat == True:
					if player.sprite.gravity >= 0:
						for sprite in everything:
							sprite.rect.y += dist_bottom
						player.sprite.rect.bottom = entity.rect.top
						player.sprite.gravity = 0
						player.sprite.on_ground = True
					else:
						player.sprite.on_ground = False
						player.sprite.plat = False

			if entity in platforms_disappearing.sprites():
				if -20 < dist_bottom < 20:
					player.sprite.plat = True
				if player.sprite.last_jump == False and player.sprite.plat == True and entity.active == True:
					if player.sprite.gravity >= 0:
						for sprite in everything:
							sprite.rect.y += dist_bottom
						player.sprite.rect.bottom = entity.rect.top
						player.sprite.gravity = 0
						player.sprite.on_ground = True
						if entity.touch_time == None:
							if entity.wait_time == None:
								entity.touch_time = time.time()
					else:
						player.sprite.on_ground = False
						player.sprite.plat = False

			if entity in checkpoints.sprites():
				if player.sprite.respawn <= entity.tag:
					player.sprite.respawn = entity.tag
					entity.image = pygame.transform.scale(entity.check_surf2, (150, 375))

			if entity in win_trigger.sprites():
				global win_bool, end_time, username_status
				if win_bool == False:
					end_time = time.time()
					win_bool = True
					player.sprite.win_bool = True
					entity.image = pygame.transform.scale(entity.image, (0,0))

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
					player.sprite.gravity = -25
					entity.index = 0

			if entity in winds.sprites():
				if entity.direction == "right":
					player.sprite.velocity += entity.speed
				elif entity.direction == "left":
					player.sprite.velocity += -1 * entity.speed
				elif entity.direction == "up":
					player.sprite.gravity += -1 * entity.speed
				elif entity.direction == "down":
					player.sprite.gravity += entity.speed

	except:
		pass
	funny_list = total_list
	for entityf in funny_list:
		if entityf in blocks.sprites() or entityf in platforms.sprites() or entityf in platforms_disappearing.sprites():
			player.sprite.on_ground = True
			player.sprite.jump_index = 0
			player.sprite.fall_index = 0
			break
		else:
			player.sprite.on_ground = False

def setup():
	player.empty()
	player.add(Player())

	blocks.empty()
	blocks.add(Block([0, 150], "full"))
	blocks.add(Block([150, 150], "full"))
	blocks.add(Block([300, 150], "full"))
	blocks.add(Block([450, 150], "full"))
	blocks.add(Block([600, 150], "full"))
	blocks.add(Block([0, 300], "full"))
	blocks.add(Block([150, 300], "full"))
	blocks.add(Block([300, 300], "full"))
	blocks.add(Block([450, 300], "full"))
	blocks.add(Block([600, 300], "full"))
	blocks.add(Block([750, 300], "full"))
	blocks.add(Block([900, 300], "full"))
	blocks.add(Block([1050, 300], "full"))
	blocks.add(Block([1050, 300], "full"))
	blocks.add(Block([1200, 150], "full"))
	blocks.add(Block([1200, 300], "full"))

	spikes.empty()
	spikes.add(Spike([1240, 550]))

	platforms.empty()
	platforms.add(Platform([940, 400]))

	platforms_disappearing.empty()
	# platforms_disappearing.add(Platform_disappearing([0, -80]))

	checkpoints.empty()
	checkpoints.add(Checkpoint([0, -113], 0))
	# checkpoints.add(Checkpoint([450, -113], 1))

	win_trigger.empty()
	win_trigger.add(Win_trigger([150, 24]))

	mushrooms.empty()
	# mushrooms.add(Mushroom([150, 0]))

	winds.empty()
	# winds.add(Wind([300, 0], "up", 1))

	level_groups.empty()
	level_groups.add(blocks)
	level_groups.add(spikes)
	level_groups.add(platforms)
	level_groups.add(platforms_disappearing)
	level_groups.add(checkpoints)
	level_groups.add(win_trigger)
	level_groups.add(mushrooms)
	level_groups.add(winds)

	everything.empty()
	everything.add(player)
	everything.add(blocks)
	everything.add(spikes)
	everything.add(platforms)
	everything.add(platforms_disappearing)
	everything.add(checkpoints)
	everything.add(win_trigger)
	everything.add(mushrooms)
	everything.add(winds)


test_font = pygame.font.Font("resources/Early GameBoy.ttf", 50)
test_font_s = pygame.font.Font("resources/Early GameBoy.ttf", 30)

with open('leaderboard.json', 'r') as json_file:
	leader_dict = json.load(json_file)
leader_sorted_list = sorted(leader_dict.items(), key=lambda x: x[1])
leaderboard = dict(leader_sorted_list)

start_text_surf = test_font.render("ENTER", False, "Black")
start_text_rect = start_text_surf.get_rect(center=(640, 560))

input_text_surf = test_font.render("Enter username:", False, "Black")
input_text_rect = input_text_surf.get_rect(center=(640, 325))

continue_text = test_font.render("Press ENTER to restart", False, "Black")
continue_rect = continue_text.get_rect(midtop=(640, 325))

gg_text_surf = test_font.render("Good game!", False, "Black")
gg_text_rect1 = gg_text_surf.get_rect(center=(640, 360))
gg_text_rect2 = gg_text_surf.get_rect(center=(640, 325))

username = ""
username_status = False
username_text_surf = test_font.render(username, False, "Black")
username_text_rect = username_text_surf.get_rect(center=(640, 360))

game_bg_surf = pygame.image.load("resources/bg.png").convert()
game_bg_surf = pygame.transform.scale(game_bg_surf, (1280, 720))
game_bg_rect = game_bg_surf.get_rect(center=(640, 360))

bg_surf = pygame.image.load("resources/bgmain.png").convert()
bg_surf = pygame.transform.scale(bg_surf, (1280, 720))
bg_rect = bg_surf.get_rect(center=(640, 360))

slime_king = pygame.image.load("resources/logo.png").convert_alpha()
slime_king = pygame.transform.scale(slime_king, (640, 360))
slime_rect = slime_king.get_rect(center=(640, 280))

start_button = pygame.image.load("resources/button3.png").convert_alpha()
start_button = pygame.transform.scale(start_button, (250, 90))
start_rect = start_button.get_rect(center=(640, 560))

start_button_r = pygame.image.load("resources/button2.png").convert_alpha()
start_button_r = pygame.transform.scale(start_button_r, (90, 90))
start_rect_r = start_button_r.get_rect(center=(750, 560))

start_button_l = pygame.image.load("resources/button1.png").convert_alpha()
start_button_l = pygame.transform.scale(start_button_l, (90, 90))
start_rect_l = start_button_l.get_rect(center=(520, 560))

lb_corner1 = pygame.transform.scale(pygame.image.load("resources/ui1.png").convert_alpha(), (90, 90))
lb_corner2 = pygame.transform.scale(pygame.image.load("resources/ui2.png").convert_alpha(), (90, 90))
lb_corner3 = pygame.transform.scale(pygame.image.load("resources/ui3.png").convert_alpha(), (90, 90))
lb_corner4 = pygame.transform.scale(pygame.image.load("resources/ui4.png").convert_alpha(), (90, 90))
lb_top = pygame.transform.scale(pygame.image.load("resources/ui5.png").convert_alpha(), (90, 90))
lb_bot = pygame.transform.scale(pygame.image.load("resources/ui6.png").convert_alpha(), (90, 90))
lb_left = pygame.transform.scale(pygame.image.load("resources/ui7.png").convert_alpha(), (90, 90))
lb_right = pygame.transform.scale(pygame.image.load("resources/ui8.png").convert_alpha(), (90, 90))
lb_mid = pygame.transform.scale(pygame.image.load("resources/ui9.png").convert_alpha(), (90, 90))
lb_1r = pygame.transform.scale(pygame.image.load("resources/button2.png").convert_alpha(), (90, 90))
lb_1l = pygame.transform.scale(pygame.image.load("resources/button1.png").convert_alpha(), (90, 90))
lb_1m = pygame.transform.scale(pygame.image.load("resources/button3.png").convert_alpha(), (90, 90))

player = pygame.sprite.GroupSingle()
blocks = pygame.sprite.Group()
spikes = pygame.sprite.Group()
platforms = pygame.sprite.Group()
platforms_disappearing = pygame.sprite.Group()
checkpoints = pygame.sprite.Group()
win_trigger = pygame.sprite.GroupSingle()
mushrooms = pygame.sprite.Group()
winds = pygame.sprite.Group()
level_groups = pygame.sprite.Group()
everything = pygame.sprite.Group()

while True:
	mouse_pos = [0, 0]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
		if event.type == pygame.KEYDOWN and username_status == True:
			if event.key == pygame.K_BACKSPACE:
				username = username[:-1]
			if event.key == pygame.K_RETURN:
				username_status = False
				lb_active = True
				if username in leaderboard.keys():
					if end_time - start_time < leaderboard.get(username):
						leaderboard[username] = end_time - start_time
				else:
					leaderboard[username] = end_time - start_time

				with open('leaderboard.json', 'w') as outfile:
					json.dump(leaderboard, outfile)
			else:
				username += event.unicode
	if game_active and not win_bool:
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
	presed_keys = pygame.mouse.get_pressed()

	if (start_text_rect.collidepoint(mouse_pos) or keys[pygame.K_RETURN]) and game_active == False:
		setup()
		last_surface = None
		end_time = None
		start_time = None
		win_bool = False
		lb_active = False
		height = 0
		extra_time = None
		username = ""

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
		screen.blit(game_bg_surf, game_bg_rect)
		level_groups.draw(screen)
		level_groups.update()
		winds.update()
		player.draw(screen)
		player.update()
		timer_text_surf = test_font.render(
			str(round(time.time() - start_time, 2)), False, "Black")
		timer_text_rect = timer_text_surf.get_rect(topleft=(60, 60))
		screen.blit(render(str(round(time.time() - start_time, 2)), test_font), timer_text_rect)
	elif win_bool:

		collision_sprite()
		screen.blit(game_bg_surf, game_bg_rect)
		level_groups.draw(screen)
		level_groups.update()
		player.draw(screen)
		player.update()
		username_text_surf = test_font.render(username, False, "Black")
		username_text_rect = username_text_surf.get_rect(center=(640, 395))
		timer_text_surf = test_font.render(("Time: " + str(round(end_time - start_time, 2))), False, "Black")
		timer_text_rect = timer_text_surf.get_rect(center=(640, 395))

		if lb_active:
			lb_list = []

			if len(leaderboard) <= 6:
				for item in leaderboard.items():
					lb_list.append(item)
			else:
				for item in leaderboard.items():
					lb_list.append(item)
				lb_list = lb_list[:6]
			height = 550 / len(lb_list)
			
			for blin in lb_list:
				if blin == lb_list[0] and blin == lb_list[-1]:
					screen.blit(lb_1l, lb_1l.get_rect(midtop=(460, height)))
					screen.blit(lb_1m, lb_1m.get_rect(midtop=(550, height)))
					screen.blit(lb_1m, lb_1m.get_rect(midtop=(640, height)))
					screen.blit(lb_1m, lb_1m.get_rect(midtop=(730, height)))
					screen.blit(lb_1r, lb_1r.get_rect(midtop=(820, height)))
					screen.blit(render("1. " + str(blin[0]) + ", " + str(round(blin[1], 2)), test_font_s), (460, height+25))
				elif blin == lb_list[0]:
					screen.blit(lb_corner1, lb_corner1.get_rect(midtop=(460, height)))
					screen.blit(lb_top, lb_top.get_rect(midtop=(550, height)))
					screen.blit(lb_top, lb_top.get_rect(midtop=(640, height)))
					screen.blit(lb_top, lb_top.get_rect(midtop=(730, height)))
					screen.blit(lb_corner2, lb_corner2.get_rect(midtop=(820, height)))
					screen.blit(render(str(lb_list.index(blin)+1) + ". " + str(blin[0]) + ", " + str(round(blin[1], 2)), test_font_s), (460, height+25))
				elif blin == lb_list[-1]:
					screen.blit(lb_corner4, lb_corner4.get_rect(midtop=(460, height)))
					screen.blit(lb_bot, lb_bot.get_rect(midtop=(550, height)))
					screen.blit(lb_bot, lb_bot.get_rect(midtop=(640, height)))
					screen.blit(lb_bot, lb_bot.get_rect(midtop=(730, height)))
					screen.blit(lb_corner3, lb_corner3.get_rect(midtop=(820, height)))
					screen.blit(render(str(lb_list.index(blin)+1) + ". " + str(blin[0]) + ", " + str(round(blin[1], 2)), test_font_s), (460, height+25))
				else:
					screen.blit(lb_left, lb_left.get_rect(midtop=(460, height)))
					screen.blit(lb_mid, lb_mid.get_rect(midtop=(550, height)))
					screen.blit(lb_mid, lb_mid.get_rect(midtop=(640, height)))
					screen.blit(lb_mid, lb_mid.get_rect(midtop=(730, height)))
					screen.blit(lb_right, lb_right.get_rect(midtop=(820, height)))
					screen.blit(render(str(lb_list.index(blin)+1) + ". " + str(blin[0]) + ", " + str(round(blin[1], 2)), test_font_s), (460, height+25))
				height += 90
			if extra_time == None:
				extra_time = time.time()
			if time.time() > extra_time+2:
				screen.blit(render("Press ENTER to continue", test_font), continue_text.get_rect(midtop=(640, height+20)))
				game_active = False
		elif time.time() > end_time + 5:
			screen.blit(render("Input username:", test_font), input_text_rect)
			screen.blit(render(username, test_font), username_text_rect)
			username_status = True
		elif time.time() > end_time + 3:
			screen.blit(render(("Time: " + str(round(end_time - start_time, 2))), test_font), timer_text_rect)
			screen.blit(render("Good game!", test_font), gg_text_rect2)

		elif time.time() > end_time + 1:
			screen.blit(render("Good game!", test_font), gg_text_rect1)

	else:
		screen.blit(bg_surf, bg_rect)
		screen.blit(slime_king, slime_rect)
		screen.blit(start_button, start_rect)
		screen.blit(start_button_r, start_rect_r)
		screen.blit(start_button_l, start_rect_l)
		screen.blit(render("ENTER", test_font), start_text_rect)

	pygame.display.update()
	clock.tick(60)
