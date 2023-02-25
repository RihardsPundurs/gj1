import pygame
from sys import exit
from classes import *
import json
import time
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)  #
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
					player.sprite.gravity = -30
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
	blocks.empty()
	winds.empty()
	spikes.empty()
	platforms.empty()
	platforms_disappearing.empty()
	checkpoints.empty()
	win_trigger.empty()
	mushrooms.empty()
	level_groups.empty()
	everything.empty()
	player.add(Player())

	blocks.add(Block([0, 150*1], "full"))
	blocks.add(Block([150*1, 150*1], "full"))
	blocks.add(Block([150*2, 150*1], "full"))
	blocks.add(Block([150*3, 150*1], "full"))
	blocks.add(Block([150*4, 150*1], "full"))
	blocks.add(Block([150*-1, 150*1], "full"))
	blocks.add(Block([150*-1, 0], "full"))
	blocks.add(Block([150*-1, 150*-1], "full"))
	blocks.add(Block([150*-1, 150*-2], "full"))
	blocks.add(Block([150*5, 150*2], "full"))
	blocks.add(Block([150*6, 150*2], "full"))
	blocks.add(Block([150*7, 150*2], "full"))
	blocks.add(Block([150*8, 150*2], "full"))
	blocks.add(Block([150*4, 150*2], "full"))
	blocks.add(Block([150*9, 150*2], "full"))
	blocks.add(Block([150*9, 150*1], "full"))
	blocks.add(Block([150*10, 150*1], "full"))
	blocks.add(Block([150*11, 150*1], "full"))
	blocks.add(Block([150*12, 150*1], "full"))
	blocks.add(Block([150*13, 150*1], "full"))
	blocks.add(Block([150*14, 150*1], "full"))
	blocks.add(Block([150*14, 150*2], "full"))
	blocks.add(Block([150*15, 150*2], "full"))
	blocks.add(Block([150*16, 150*2], "full"))
	blocks.add(Block([150*17, 150*2], "full"))
	blocks.add(Block([150*18, 150*2], "full"))
	spikes.add(Spike([150*15+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*15, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*7, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*8, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*9, 150*1+50*1]))
	spikes.add(Spike([150*15+ 50*10, 150*1+50*1]))
	blocks.add(Block([150*19, 150*1], "full"))
	blocks.add(Block([150*19, 150*2], "full"))
	blocks.add(Block([150*20, 150*1], "full"))
	blocks.add(Block([150*21, 150*1], "full"))
	blocks.add(Block([150*22, 150*1], "full"))
	blocks.add(Block([150*23, 150*1], "full"))
	blocks.add(Block([150*24, 150*1], "full"))
	blocks.add(Block([150*25, 150*1], "full"))
	blocks.add(Block([150*26, 150*1], "full"))
	blocks.add(Block([150*26, 150*2], "full"))
	blocks.add(Block([150*27, 150*2], "full"))
	blocks.add(Block([150*28, 150*2], "full"))
	blocks.add(Block([150*29, 150*2], "full"))
	blocks.add(Block([150*30, 150*2], "full"))
	blocks.add(Block([150*31, 150*2], "full"))
	blocks.add(Block([150*32, 150*2], "full"))
	blocks.add(Block([150*32, 150*1], "full"))
	spikes.add(Spike([150*27+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*27, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*7, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*8, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*9, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*10, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*11, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*12, 150*1+50*1]))
	spikes.add(Spike([150*27+ 50*13, 150*1+50*1]))
	blocks.add(Block([150*33, 150*1], "full"))
	blocks.add(Block([150*34, 150*1], "full"))
	blocks.add(Block([150*35, 150*1], "full"))
	blocks.add(Block([150*36, 150*1], "full"))
	blocks.add(Block([150*37, 150*1], "full"))
	blocks.add(Block([150*38, 150*1], "full"))
	blocks.add(Block([150*39, 150*1], "full"))
	blocks.add(Block([150*39, 150*2], "full"))
	blocks.add(Block([150*40, 150*2], "full"))
	blocks.add(Block([150*41, 150*2], "full"))
	blocks.add(Block([150*42, 150*2], "full"))
	blocks.add(Block([150*43, 150*1], "full"))
	blocks.add(Block([150*43, 150*2], "full"))
	spikes.add(Spike([150*40+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*40, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*40+ 50*7, 150*1+50*1]))
	blocks.add(Block([150*44, 150*1], "full"))
	blocks.add(Block([150*45, 150*1], "full"))
	blocks.add(Block([150*45, 150*2], "full"))
	blocks.add(Block([150*46, 150*2], "full"))
	blocks.add(Block([150*47, 150*2], "full"))
	blocks.add(Block([150*48, 150*2], "full"))
	blocks.add(Block([150*49, 150*2], "full"))
	blocks.add(Block([150*50, 150*2], "full"))
	blocks.add(Block([150*51, 150*1], "full"))
	blocks.add(Block([150*51, 150*2], "full"))
	spikes.add(Spike([150*46+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*46, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*7, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*8, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*9, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*10, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*11, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*12, 150*1+50*1]))
	spikes.add(Spike([150*46+ 50*13, 150*1+50*1]))
	blocks.add(Block([150*52, 150*1], "full"))
	blocks.add(Block([150*53, 150*1], "full"))
	blocks.add(Block([150*53, 150*2], "full"))
	blocks.add(Block([150*54, 150*2], "full"))
	blocks.add(Block([150*55, 150*2], "full"))
	blocks.add(Block([150*56, 150*2], "full"))
	blocks.add(Block([150*57, 150*2], "full"))
	blocks.add(Block([150*57, 150*1], "full"))
	spikes.add(Spike([150*54+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*54, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*54+ 50*7, 150*1+50*1]))
	blocks.add(Block([150*58, 150*1], "full"))
	blocks.add(Block([150*59, 150*1], "full"))
	blocks.add(Block([150*60, 150*1], "full"))
	blocks.add(Block([150*61, 150*1], "full"))
	blocks.add(Block([150*62, 150*1], "full"))
	blocks.add(Block([150*63, 150*1], "full"))
	checkpoints.add(Checkpoint([150*63, -113], 1))	
	blocks.add(Block([150*64, 150*1], "full"))
	blocks.add(Block([150*65, 150*1], "full"))
	blocks.add(Block([150*66, 150*1], "full"))
	blocks.add(Block([150*67, 150*1], "full"))
	blocks.add(Block([150*68, 150*1], "full"))
	blocks.add(Block([150*68, 150*2], "full"))
	blocks.add(Block([150*69, 150*2], "full"))
	blocks.add(Block([150*70, 150*2], "full"))
	blocks.add(Block([150*71, 150*2], "full"))
	blocks.add(Block([150*72, 150*2], "full"))
	blocks.add(Block([150*73, 150*2], "full"))
	blocks.add(Block([150*73, 150*1], "full"))
	spikes.add(Spike([150*69+ 50*-1, 150*1+50*1]))
	spikes.add(Spike([150*69, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*1, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*2, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*3, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*4, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*5, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*6, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*7, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*8, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*9, 150*1+50*1]))
	spikes.add(Spike([150*69+ 50*10, 150*1+50*1]))
	blocks.add(Block([150*74, 150*1], "full"))
	blocks.add(Block([150*75, 150*1], "full"))
	blocks.add(Block([150*76, 150*1], "full"))
	blocks.add(Block([150*77, 150*1], "full"))
	blocks.add(Block([150*78, 150*1], "full"))
	blocks.add(Block([150*79, 150*1], "full"))
	blocks.add(Block([150*80, 150*1], "full"))
	spikes.add(Spike([150*79+ 50*-1, 50*1]))
	spikes.add(Spike([150*79, 50*1]))
	spikes.add(Spike([150*79+ 50*1, 50*1]))
	blocks.add(Block([150*81, 150*1], "full"))
	blocks.add(Block([150*82, 150*1], "full"))
	blocks.add(Block([150*83, 150*1], "full"))
	blocks.add(Block([150*84, 150*1], "full"))
	spikes.add(Spike([150*84+ 50*-1, 50*1]))
	spikes.add(Spike([150*84, 50*1]))
	spikes.add(Spike([150*84+ 50*1, 50*1]))
	blocks.add(Block([150*85, 150*1], "full"))
	blocks.add(Block([150*86, 150*1], "full"))
	blocks.add(Block([150*87, 150*1], "full"))
	blocks.add(Block([150*88, 150*1], "full"))
	blocks.add(Block([150*89, 150*1], "full"))
	blocks.add(Block([150*90, 150*1], "full"))
	spikes.add(Spike([150*90+ 50*-1, 50*1]))
	spikes.add(Spike([150*90, 50*1]))
	spikes.add(Spike([150*90+ 50*1, 50*1]))
	blocks.add(Block([150*91, 150*1], "full"))
	blocks.add(Block([150*92, 150*1], "full"))
	blocks.add(Block([150*93, 150*1], "full"))
	blocks.add(Block([150*94, 150*1], "full"))
	blocks.add(Block([150*95, 150*1], "full"))
	blocks.add(Block([150*96, 150*1], "full"))
	spikes.add(Spike([150*96+ 50*-1, 50*1]))
	spikes.add(Spike([150*96, 50*1]))
	spikes.add(Spike([150*96+ 50*1, 50*1]))
	blocks.add(Block([150*97, 150*1], "full"))
	blocks.add(Block([150*98, 150*1], "full"))
	blocks.add(Block([150*99, 150*1], "full"))
	blocks.add(Block([150*100, 150*1], "full"))
	blocks.add(Block([150*101, 150*1], "full"))
	blocks.add(Block([150*102, 150*1], "full"))
	blocks.add(Block([150*103, 150*1], "full"))
	blocks.add(Block([150*104, 150*1], "full"))
	blocks.add(Block([150*105, 150*1], "full"))
	blocks.add(Block([150*106, 150*1], "full"))
	blocks.add(Block([150*107, 150*1], "full"))
	spikes.add(Spike([150*106+ 50*-1, 50*1]))
	spikes.add(Spike([150*106, 50*1]))
	spikes.add(Spike([150*106+ 50*1, 50*1]))
	spikes.add(Spike([150*106+ 50*2, 50*1]))
	spikes.add(Spike([150*106+ 50*3, 50*1]))
	spikes.add(Spike([150*106+ 50*4, 50*1]))
	blocks.add(Block([150*108, 150*1], "full"))
	blocks.add(Block([150*109, 150*1], "full"))
	blocks.add(Block([150*110, 150*1], "full"))
	blocks.add(Block([150*111, 150*1], "full"))
	blocks.add(Block([150*112, 150*1], "full"))
	blocks.add(Block([150*113, 150*1], "full"))
	spikes.add(Spike([150*112+ 50*-1, 50*1]))
	spikes.add(Spike([150*112, 50*1]))
	spikes.add(Spike([150*112+ 50*1, 50*1]))
	spikes.add(Spike([150*112+ 50*2, 50*1]))
	spikes.add(Spike([150*112+ 50*3, 50*1]))
	spikes.add(Spike([150*112+ 50*4, 50*1]))
	blocks.add(Block([150*114, 150*1], "full"))
	blocks.add(Block([150*115, 150*1], "full"))
	blocks.add(Block([150*116, 150*1], "full"))
	blocks.add(Block([150*117, 150*1], "full"))
	blocks.add(Block([150*118, 150*1], "full"))
	blocks.add(Block([150*119, 150*1], "full"))
	blocks.add(Block([150*120, 150*1], "full"))
	spikes.add(Spike([150*118+ 50*-1, 50*1]))
	spikes.add(Spike([150*118, 50*1]))
	spikes.add(Spike([150*118+ 50*1, 50*1]))
	spikes.add(Spike([150*118+ 50*2, 50*1]))
	spikes.add(Spike([150*118+ 50*3, 50*1]))
	spikes.add(Spike([150*118+ 50*4, 50*1]))
	spikes.add(Spike([150*118+ 50*5, 50*1]))
	spikes.add(Spike([150*118+ 50*6, 50*1]))
	blocks.add(Block([150*121, 150*1], "full"))
	blocks.add(Block([150*122, 150*1], "full"))
	blocks.add(Block([150*123, 150*1], "full"))
	blocks.add(Block([150*124, 150*1], "full"))
	blocks.add(Block([150*125, 150*1], "full"))
	blocks.add(Block([150*126, 150*1], "full"))
	checkpoints.add(Checkpoint([150*126, -113], 2))	
	blocks.add(Block([150*127, 150*1], "full"))
	blocks.add(Block([150*128, 150*1], "full"))
	blocks.add(Block([150*129, 150*1], "full"))
	blocks.add(Block([150*130, 150*1], "full"))
	blocks.add(Block([150*131, 150*1], "full"))
	platforms.add(Platform([150*132, -150]))
	blocks.add(Block([150*132, 150*1], "full"))
	blocks.add(Block([150*133, 150*1], "full"))
	blocks.add(Block([150*134, 150*1], "full"))
	platforms.add(Platform([150*135, -300]))
	blocks.add(Block([150*135, 150*1], "full"))
	blocks.add(Block([150*136, 150*1], "full"))
	blocks.add(Block([150*137, 150*1], "full"))
	platforms.add(Platform([150*138, -450]))
	blocks.add(Block([150*138, 150*1], "full"))
	blocks.add(Block([150*139, 150*1], "full"))
	blocks.add(Block([150*140, 150*1], "full"))
	blocks.add(Block([150*141, 150*1], "full"))
	blocks.add(Block([150*141, 0], "full"))
	blocks.add(Block([150*141, 150*-1], "full"))
	blocks.add(Block([150*141, 150*-2], "full"))
	blocks.add(Block([150*141, 150*-3], "full"))
	blocks.add(Block([150*142, 150*-3], "full"))
	blocks.add(Block([150*143, 150*-3], "full"))
	blocks.add(Block([150*144, 150*-3], "full"))
	blocks.add(Block([150*145, 150*-3], "full"))
	blocks.add(Block([150*145, 150*-2], "full"))
	blocks.add(Block([150*145, 150*-1], "full"))
	blocks.add(Block([150*146, 150*-1], "full"))
	blocks.add(Block([150*147, 150*-1], "full"))
	blocks.add(Block([150*148, 150*-1], "full"))
	blocks.add(Block([150*149, 150*-1], "full"))
	blocks.add(Block([150*150, 150*-1], "full"))
	blocks.add(Block([150*151, 150*-1], "full"))
	blocks.add(Block([150*152, 150*-1], "full"))
	blocks.add(Block([150*153, 150*-1], "full"))
	blocks.add(Block([150*154, 150*-1], "full"))
	blocks.add(Block([150*155, 150*-1], "full"))
	blocks.add(Block([150*156, 150*-1], "full"))
	blocks.add(Block([150*157, 150*-1], "full"))
	blocks.add(Block([150*158, 150*-1], "full"))
	blocks.add(Block([150*159, 150*-1], "full"))
	blocks.add(Block([150*160, 150*-1], "full"))
	blocks.add(Block([150*161, 150*-1], "full"))
	blocks.add(Block([150*162, 150*-1], "full"))
	blocks.add(Block([150*163, 150*-1], "full"))
	blocks.add(Block([150*164, 150*-1], "full"))
	blocks.add(Block([150*165, 150*-1], "full"))
	blocks.add(Block([150*165, 150*-2], "full"))
	blocks.add(Block([150*165, 150*-3], "full"))
	platforms.add(Platform([150*149, -450]))
	platforms.add(Platform([150*153, -450]))
	platforms.add(Platform([150*157, -450]))
	platforms.add(Platform([150*161, -450]))
	spikes.add(Spike([150*146+ 50*-1, 150*-2+50*1]))
	spikes.add(Spike([150*146, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*1, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*2, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*3, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*4, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*5, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*6, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*7, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*8, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*9, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*10, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*11, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*12, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*13, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*14, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*15, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*16, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*17, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*18, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*19, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*20, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*21, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*22, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*23, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*24, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*25, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*26, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*27, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*28, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*29, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*30, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*31, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*32, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*33, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*34, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*35, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*36, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*37, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*38, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*39, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*40, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*41, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*42, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*43, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*44, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*45, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*46, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*47, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*48, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*49, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*50, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*51, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*52, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*53, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*54, 150*-2+50*1]))
	spikes.add(Spike([150*146+ 50*55, 150*-2+50*1]))
	blocks.add(Block([150*166, 150*-3], "full"))
	blocks.add(Block([150*167, 150*-3], "full"))
	blocks.add(Block([150*168, 150*-3], "full"))
	blocks.add(Block([150*169, 150*-3], "full"))
	blocks.add(Block([150*169, 150*-2], "full"))
	blocks.add(Block([150*170, 150*-2], "full"))
	blocks.add(Block([150*171, 150*-2], "full"))
	blocks.add(Block([150*172, 150*-2], "full"))
	blocks.add(Block([150*173, 150*-2], "full"))
	blocks.add(Block([150*174, 150*-2], "full"))
	blocks.add(Block([150*175, 150*-2], "full"))
	blocks.add(Block([150*176, 150*-2], "full"))
	blocks.add(Block([150*177, 150*-2], "full"))
	blocks.add(Block([150*178, 150*-2], "full"))
	blocks.add(Block([150*179, 150*-2], "full"))
	blocks.add(Block([150*180, 150*-2], "full"))
	blocks.add(Block([150*181, 150*-2], "full"))
	blocks.add(Block([150*182, 150*-2], "full"))
	blocks.add(Block([150*183, 150*-2], "full"))
	blocks.add(Block([150*184, 150*-2], "full"))
	blocks.add(Block([150*185, 150*-2], "full"))
	blocks.add(Block([150*185, 150*-3], "full"))
	blocks.add(Block([150*185, 150*-4], "full"))
	blocks.add(Block([150*185, 150*-5], "full"))
	blocks.add(Block([150*185, 150*-6], "full"))
	blocks.add(Block([150*185, 150*-7], "full"))
	platforms.add(Platform([150*173, -750]))
	platforms.add(Platform([150*177, -750]))
	platforms.add(Platform([150*181, -750]))
	platforms.add(Platform([150*173, -1050]))
	platforms.add(Platform([150*177, -1050]))
	platforms.add(Platform([150*181, -1050]))
	platforms.add(Platform([150*173, -1350]))
	platforms.add(Platform([150*177, -1350]))
	spikes.add(Spike([150*170+ 50*-1, 150*-3+50*1]))
	spikes.add(Spike([150*170, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*1, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*2, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*3, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*4, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*5, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*6, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*7, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*8, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*9, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*10, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*11, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*12, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*13, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*14, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*15, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*16, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*17, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*18, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*19, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*20, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*21, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*22, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*23, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*24, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*25, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*26, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*27, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*28, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*29, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*30, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*31, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*32, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*33, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*34, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*35, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*36, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*37, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*38, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*39, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*40, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*41, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*42, 150*-3+50*1]))
	spikes.add(Spike([150*170+ 50*43, 150*-3+50*1]))
	spikes.add(Spike([150*177+ 50*-1, 150*-6+50*2]))
	spikes.add(Spike([150*177, 150*-6+50*2]))
	spikes.add(Spike([150*177+ 50*1, 150*-6+50*2]))
	spikes.add(Spike([150*177+ 50*-1, 150*-8+50*2]))
	spikes.add(Spike([150*177, 150*-8+50*2]))
	spikes.add(Spike([150*177+ 50*1, 150*-8+50*2]))
	spikes.add(Spike([150*181+ 50*-1, 150*-6+50*2]))
	spikes.add(Spike([150*181, 150*-6+50*2]))
	spikes.add(Spike([150*181+ 50*1, 150*-6+50*2]))
	blocks.add(Block([150*186, 150*-7], "full"))
	blocks.add(Block([150*187, 150*-7], "full"))
	blocks.add(Block([150*188, 150*-7], "full"))
	blocks.add(Block([150*189, 150*-7], "full"))
	blocks.add(Block([150*190, 150*-7], "full"))
	checkpoints.add(Checkpoint([150*190, -113 +150*-8], 3))	
	blocks.add(Block([150*191, 150*-7], "full"))
	blocks.add(Block([150*192, 150*-7], "full"))
	blocks.add(Block([150*193, 150*-7], "full"))
	blocks.add(Block([150*194, 150*-7], "full"))
	blocks.add(Block([150*195, 150*-7], "full"))
	blocks.add(Block([150*195, 150*-6], "full"))
	blocks.add(Block([150*195, 150*-5], "full"))
	blocks.add(Block([150*196, 150*-5], "full"))
	blocks.add(Block([150*197, 150*-5], "full"))
	blocks.add(Block([150*198, 150*-5], "full"))
	blocks.add(Block([150*199, 150*-5], "full"))
	blocks.add(Block([150*200, 150*-5], "full"))
	blocks.add(Block([150*201, 150*-5], "full"))
	blocks.add(Block([150*202, 150*-5], "full"))
	blocks.add(Block([150*203, 150*-5], "full"))
	blocks.add(Block([150*204, 150*-5], "full"))
	blocks.add(Block([150*205, 150*-5], "full"))
	blocks.add(Block([150*206, 150*-5], "full"))
	blocks.add(Block([150*207, 150*-5], "full"))
	blocks.add(Block([150*208, 150*-5], "full"))
	blocks.add(Block([150*209, 150*-5], "full"))
	blocks.add(Block([150*210, 150*-5], "full"))
	blocks.add(Block([150*211, 150*-5], "full"))
	blocks.add(Block([150*212, 150*-5], "full"))
	blocks.add(Block([150*213, 150*-5], "full"))
	blocks.add(Block([150*214, 150*-5], "full"))
	blocks.add(Block([150*215, 150*-5], "full"))
	blocks.add(Block([150*215, 150*-6], "full"))
	blocks.add(Block([150*215, 150*-7], "full"))
	platforms_disappearing.add(Platform_disappearing([150*199, -1050]))
	platforms_disappearing.add(Platform_disappearing([150*203, -1050]))
	platforms_disappearing.add(Platform_disappearing([150*207, -1050]))
	platforms_disappearing.add(Platform_disappearing([150*211, -1050]))
	spikes.add(Spike([150*196+ 50*-1, 150*-6+50*1]))
	spikes.add(Spike([150*196, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*1, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*2, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*3, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*4, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*5, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*6, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*7, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*8, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*9, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*10, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*11, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*12, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*13, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*14, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*15, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*16, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*17, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*18, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*19, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*20, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*21, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*22, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*23, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*24, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*25, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*26, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*27, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*28, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*29, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*30, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*31, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*32, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*33, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*34, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*35, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*36, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*37, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*38, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*39, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*40, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*41, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*42, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*43, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*44, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*45, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*46, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*47, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*48, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*49, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*50, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*51, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*52, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*53, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*54, 150*-6+50*1]))
	spikes.add(Spike([150*196+ 50*55, 150*-6+50*1]))
	blocks.add(Block([150*216, 150*-7], "full"))
	blocks.add(Block([150*217, 150*-7], "full"))
	blocks.add(Block([150*218, 150*-7], "full"))
	blocks.add(Block([150*219, 150*-7], "full"))
	blocks.add(Block([150*220, 150*-7], "full"))
	blocks.add(Block([150*221, 150*-7], "full"))
	checkpoints.add(Checkpoint([150*221, -113 +150*-8], 4))
	blocks.add(Block([150*222, 150*-7], "full"))
	blocks.add(Block([150*223, 150*-7], "full"))
	blocks.add(Block([150*224, 150*-7], "full"))
	blocks.add(Block([150*225, 150*-7], "full"))
	blocks.add(Block([150*226, 150*-7], "full"))
	blocks.add(Block([150*226, 150*-6], "full"))
	blocks.add(Block([150*226, 150*-5], "full"))
	blocks.add(Block([150*227, 150*-5], "full"))
	blocks.add(Block([150*228, 150*-5], "full"))
	blocks.add(Block([150*229, 150*-5], "full"))
	blocks.add(Block([150*230, 150*-5], "full"))
	blocks.add(Block([150*231, 150*-5], "full"))
	blocks.add(Block([150*232, 150*-5], "full"))
	blocks.add(Block([150*233, 150*-5], "full"))
	blocks.add(Block([150*234, 150*-5], "full"))
	blocks.add(Block([150*234, 150*-6], "full"))
	blocks.add(Block([150*234, 150*-7], "full"))
	winds.add(Wind([150*231, 150*-8], "right", 2))
	winds.add(Wind([150*231, 150*-9], "right", 2))
	spikes.add(Spike([150*227+ 50*-1, 150*-6+50*1]))
	spikes.add(Spike([150*227, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*1, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*2, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*3, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*4, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*5, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*6, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*7, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*8, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*9, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*10, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*11, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*12, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*13, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*14, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*15, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*16, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*17, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*18, 150*-6+50*1]))
	spikes.add(Spike([150*227+ 50*19, 150*-6+50*1]))
	blocks.add(Block([150*235, 150*-7], "full"))
	blocks.add(Block([150*236, 150*-7], "full"))
	blocks.add(Block([150*237, 150*-7], "full"))
	blocks.add(Block([150*238, 150*-7], "full"))
	blocks.add(Block([150*239, 150*-7], "full"))
	blocks.add(Block([150*240, 150*-7], "full"))
	blocks.add(Block([150*240, 150*-8], "full"))
	blocks.add(Block([150*240, 150*-9], "full"))
	blocks.add(Block([150*240, 150*-10], "full"))
	blocks.add(Block([150*240, 150*-11], "full"))
	winds.add(Wind([150*239, 150*-10], "up", 2))
	blocks.add(Block([150*241, 150*-11], "full"))
	blocks.add(Block([150*242, 150*-11], "full"))
	blocks.add(Block([150*243, 150*-11], "full"))
	blocks.add(Block([150*244, 150*-11], "full"))
	blocks.add(Block([150*245, 150*-11], "full"))
	checkpoints.add(Checkpoint([150*245, -113 +150*-12], 5))
	blocks.add(Block([150*246, 150*-11], "full"))
	blocks.add(Block([150*247, 150*-11], "full"))
	blocks.add(Block([150*248, 150*-11], "full"))
	blocks.add(Block([150*249, 150*-11], "full"))
	blocks.add(Block([150*250, 150*-11], "full"))
	blocks.add(Block([150*251, 150*-11], "full"))
	mushrooms.add(Mushroom([150*251, 150*-12]))
	blocks.add(Block([150*252, 150*-11], "full"))
	blocks.add(Block([150*253, 150*-11], "full"))
	blocks.add(Block([150*253, 150*-12], "full"))
	blocks.add(Block([150*253, 150*-13], "full"))
	blocks.add(Block([150*254, 150*-13], "full"))
	blocks.add(Block([150*255, 150*-13], "full"))
	mushrooms.add(Mushroom([150*255, 150*-14]))
	blocks.add(Block([150*256, 150*-13], "full"))
	blocks.add(Block([150*257, 150*-13], "full"))
	blocks.add(Block([150*257, 150*-14], "full"))
	blocks.add(Block([150*257, 150*-15], "full"))
	blocks.add(Block([150*258, 150*-15], "full"))
	blocks.add(Block([150*259, 150*-15], "full"))
	mushrooms.add(Mushroom([150*259, 150*-16]))
	blocks.add(Block([150*260, 150*-15], "full"))
	blocks.add(Block([150*261, 150*-15], "full"))
	blocks.add(Block([150*262, 150*-15], "full"))
	blocks.add(Block([150*262, 150*-16], "full"))
	blocks.add(Block([150*262, 150*-17], "full"))
	blocks.add(Block([150*263, 150*-17], "full"))
	blocks.add(Block([150*264, 150*-17], "full"))
	mushrooms.add(Mushroom([150*264, 150*-18]))
	blocks.add(Block([150*265, 150*-17], "full"))
	blocks.add(Block([150*266, 150*-17], "full"))
	blocks.add(Block([150*267, 150*-17], "full"))
	blocks.add(Block([150*267, 150*-18], "full"))
	blocks.add(Block([150*267, 150*-19], "full"))
	blocks.add(Block([150*268, 150*-19], "full"))
	blocks.add(Block([150*269, 150*-19], "full"))
	blocks.add(Block([150*270, 150*-19], "full"))
	blocks.add(Block([150*270, 150*-20], "full"))
	blocks.add(Block([150*270, 150*-21], "full"))
	blocks.add(Block([150*270, 150*-22], "full"))
	spikes.add(Spike([150*267+ 50*-1, 150*-20+50*1]))
	spikes.add(Spike([150*267, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*1, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*2, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*3, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*4, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*5, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*6, 150*-20+50*1]))
	spikes.add(Spike([150*267+ 50*7, 150*-20+50*1]))
	platforms.add(Platform([150*264, -3150]))
	platforms.add(Platform([150*265, -3150]))
	platforms.add(Platform([150*263, -3150]))
	mushrooms.add(Mushroom([150*264, 150*-22]))
	winds.add(Wind([150*268, 150*-25], "right", 2))
	blocks.add(Block([150*271, 150*-22], "full"))
	blocks.add(Block([150*272, 150*-22], "full"))
	blocks.add(Block([150*273, 150*-22], "full"))
	win_trigger.add(Win_trigger([150*273, 150*-23]))
	blocks.add(Block([150*274, 150*-22], "full"))
	blocks.add(Block([150*274, 150*-21], "full"))
	blocks.add(Block([150*274, 150*-20], "full"))
	blocks.add(Block([150*278, 150*-20], "full"))
	blocks.add(Block([150*278, 150*-21], "full"))
	blocks.add(Block([150*278, 150*-22], "full"))
	blocks.add(Block([150*278, 150*-23], "full"))
	blocks.add(Block([150*278, 150*-24], "full"))
	blocks.add(Block([150*278, 150*-25], "full"))
	blocks.add(Block([150*278, 150*-26], "full"))
	blocks.add(Block([150*277, 150*-20], "full"))
	blocks.add(Block([150*277, 150*-21], "full"))
	blocks.add(Block([150*277, 150*-22], "full"))
	blocks.add(Block([150*277, 150*-23], "full"))
	blocks.add(Block([150*277, 150*-24], "full"))
	blocks.add(Block([150*277, 150*-25], "full"))
	blocks.add(Block([150*277, 150*-26], "full"))

	# blocks.add(Block([150*, 150*], "full"))
	# blocks.add(Block([150*, 150*], "full"))
	# blocks.add(Block([150*, 150*], "full"))
	# blocks.add(Block([150*, 150*], "full"))
	# blocks.add(Block([150*, 150*], "full"))
	# blocks.add(Block([150*, 150*], "full"))

	# spikes.add(Spike([1240, 550]))

	# platforms.add(Platform([940, 400]))

	# platforms_disappearing.add(Platform_disappearing([0, -80]))

	checkpoints.add(Checkpoint([0, -113], 0))
	# checkpoints.add(Checkpoint([450, -113], 1))

	# win_trigger.add(Win_trigger([150, 24]))

	# mushrooms.add(Mushroom([150, 0]))

	# winds.add(Wind([300, 0], "up", 1))

	level_groups.add(blocks)
	level_groups.add(spikes)
	level_groups.add(platforms)
	level_groups.add(platforms_disappearing)
	level_groups.add(checkpoints)
	level_groups.add(win_trigger)
	level_groups.add(mushrooms)
	level_groups.add(winds)
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
			height = 1280/2 - len(lb_list) / 2 - 35
			
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
