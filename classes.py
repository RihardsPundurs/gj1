import pygame
import time

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_surf1 = pygame.image.load("resources/Blobber1.png").convert_alpha()
		player_surf2 = pygame.image.load("resources/Blobber2.png").convert_alpha()
		player_surf3 = pygame.image.load("resources/Blobber3.png").convert_alpha()
		player_surf4 = pygame.image.load("resources/Blobber4.png").convert_alpha()
		player_surf5 = pygame.image.load("resources/Blobber5.png").convert_alpha()
		player_surf6 = pygame.image.load("resources/Blobber6.png").convert_alpha()
		player_surf7 = pygame.image.load("resources/Blobber7.png").convert_alpha()
		player_surf8 = pygame.image.load("resources/BlobberCrown.png").convert_alpha()

		self.player_jump = [player_surf1, player_surf2, player_surf3, player_surf4, player_surf5]
		self.jump_index = 0

		self.player_fly = [player_surf6, player_surf7]
		self.fly_index = 0

		self.player_fall = [player_surf4, player_surf3, player_surf2, player_surf1]
		self.fall_index = 0

		self.player_stand = [player_surf1, player_surf2]
		self.stand_index = 0
		self.player_win = player_surf8

		self.image = self.player_stand[0]
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(640, 360))
		self.gravity = 0
		self.flip = False
		self.velocity = 0
		self.on_ground = False
		self.last_jump = False
		self.plat = False
		self.respawn = 0

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] or keys[pygame.K_w]:
			if self.last_jump == False:
				if self.on_ground == True:
					self.gravity = -20
			self.last_jump = True
		else:
			self.last_jump = False

		if keys[pygame.K_d] and self.velocity <= 30:
			self.velocity += 1
		elif keys[pygame.K_a] and self.velocity >= -30:
			self.velocity -= 1
		else:
			if self.velocity < 0:
				self.velocity += 1
			elif self.velocity > 0:
				self.velocity -= 1

	def animation_state(self):
		# print(self.gravity)
		# print(self.velocity)
		if self.gravity == 1 and self.on_ground == True:
			if self.velocity == 0:
				if self.flip == False:
					self.image = pygame.transform.scale(self.player_stand[round(self.stand_index)%2], (150, 150))
				else:
					self.image = pygame.transform.flip(pygame.transform.scale(self.player_stand[round(self.stand_index)%2], (150, 150)), True, False)
				self.stand_index += 0.05
			elif self.velocity < 0:
				self.flip = True
				self.image = pygame.transform.flip(pygame.transform.scale(self.player_stand[round(self.stand_index)%2], (150, 150)), True, False)
				self.stand_index += 0.05
			elif self.velocity > 0:
				self.flip = False
				self.image = pygame.transform.scale(self.player_stand[round(self.stand_index)%2], (150, 150))
				self.stand_index += 0.05

		# if self.gravity > 1:
		# 	if self.fall_index <= 3:
		# 		if self.velocity == 0:
		# 			if self.flip == False:
		# 				self.image = pygame.transform.scale(self.player_fall[round(self.fall_index)%4], (150, 150))
		# 			else:
		# 				self.image = pygame.transform.flip(pygame.transform.scale(self.player_fall[round(self.fall_index)%4], (150, 150)), True, False)
		# 			self.fall_index += 1
		# 		elif self.velocity < 0:
		# 			self.flip = True
		# 			self.image = pygame.transform.flip(pygame.transform.scale(self.player_fall[round(self.fall_index)%4], (150, 150)), True, False)
		# 			self.fall_index += 1
		# 		elif self.velocity > 0:
		# 			self.flip = False
		# 			self.image = pygame.transform.scale(self.player_fall[round(self.fall_index)%4], (150, 150))
		# 			self.fall_index += 1

		else:
			if self.jump_index <= 4:
				if self.velocity == 0:
					if self.flip == False:
						self.image = pygame.transform.scale(self.player_jump[round(self.jump_index)%5], (150, 150))
					else:
						self.image = pygame.transform.flip(pygame.transform.scale(self.player_jump[round(self.jump_index)%5], (150, 150)), True, False)
					self.jump_index += 1
				elif self.velocity < 0:
					self.flip = True
					self.image = pygame.transform.flip(pygame.transform.scale(self.player_jump[round(self.jump_index)%5], (150, 150)), True, False)
					self.jump_index += 1
				elif self.velocity > 0:
					self.flip = False
					self.image = pygame.transform.scale(self.player_jump[round(self.jump_index)%5], (150, 150))
					self.jump_index += 1
			else:
				if self.velocity == 0:
					if self.flip == False:
						self.image = pygame.transform.scale(self.player_fly[round(self.fly_index)%2], (150, 150))
					else:
						self.image = pygame.transform.flip(pygame.transform.scale(self.player_fly[round(self.fly_index)%2], (150, 150)), True, False)
					self.fly_index += 0.1
				elif self.velocity < 0:
					self.flip = True
					self.image = pygame.transform.flip(pygame.transform.scale(self.player_fly[round(self.fly_index)%2], (150, 150)), True, False)
					self.fly_index += 0.1
				elif self.velocity > 0:
					self.flip = False
					self.image = pygame.transform.scale(self.player_fly[round(self.fly_index)%2], (150, 150))
					self.fly_index += 0.1


		# else:
		# 	self.player_index += 0.02
		# 	if self.player_index >= len(self.player_surface_list):self.player_index = 0
		# 	self.image = self.player_surface_list[int(self.player_index)]

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		self.rect.x += self.velocity

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Block(pygame.sprite.Sprite):
	def __init__(self, cords, type):
		super().__init__()
		self.cords = cords
		if type == "topleft":
			self.image = pygame.image.load("resources/Ground1.png").convert_alpha()
		if type == "topright":
			self.image = pygame.image.load("resources/Ground2.png").convert_alpha()
		if type == "bottomright":
			self.image = pygame.image.load("resources/Ground3.png").convert_alpha()
		if type == "bottomleft":
			self.image = pygame.image.load("resources/Ground4.png").convert_alpha()
		if type == "top":
			self.image = pygame.image.load("resources/Ground5.png").convert_alpha()
		if type == "right":
			self.image = pygame.image.load("resources/Ground6.png").convert_alpha()
		if type == "bottom":
			self.image = pygame.image.load("resources/Ground7.png").convert_alpha()
		if type == "left":
			self.image = pygame.image.load("resources/Ground8.png").convert_alpha()
		if type == "full":
			self.image = pygame.image.load("resources/Ground9.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Spike(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/spike.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Platform(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/cloudplatform.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 75))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

# class Platform_moving(pygame.sprite.Sprite):
# 	def __init__(self, cords, interval):
# 		super().__init__()
# 		self.cords = cords
# 		self.interval = interval
# 		self.speed = 2
# 		self.distance = 0
# 		self.image = pygame.image.load("resources/branch.png").convert_alpha()
# 		self.image = pygame.transform.scale(self.image, (150, 150))
# 		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

# 	def update(self):
# 		if self.rect.x > self.cords[0] + self.interval*-1 and self.rect.x > self.cords[0] + self.interval and self.speed > 0:
# 			self.speed = -2
# 		elif self.rect.x < self.cords[0] + self.interval*-1 and self.rect.x < self.cords[0] + self.interval and self.speed < 0:
# 			self.speed = 2

# 		self.distance += self.speed
# 		self.rect.x += self.speed
# 		print(self.rect.x)
# 		print(self.speed)
# 		print(self.rect.x - self.cords[0] - self.interval*-1 - self.distance)
# 		print(self.rect.x + self.interval*-1)
# 		print(self.interval)

class Platform_disappearing(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.touch_time = None
		self.touch_duration = 0.5
		self.wait_time = None
		self.wait_duration = 5
		self.active = True
		self.image = pygame.image.load("resources/disscloud.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 75))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

	def update(self):
		if self.touch_time != None:
			if self.touch_time+self.touch_duration <= time.time():
				self.touch_time = None
				self.active = False
				self.wait_time = time.time()
		if self.wait_time != None:
			if self.wait_time+self.wait_duration <= time.time():
				self.wait_time = None
				self.active = True

class Checkpoint(pygame.sprite.Sprite):
	def __init__(self, cords, tag):
		super().__init__()
		self.cords = cords
		self.tag = tag
		self.image = pygame.image.load("resources/CheckpointLit.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Win_trigger(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/Log.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Mushroom(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/shroom1.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Wind(pygame.sprite.Sprite):
	def __init__(self, cords, direction, speed):
		super().__init__()
		self.direction = direction
		self.speed = speed
		self.cords = cords
		self.image = pygame.image.load("resources/Wind1.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))
