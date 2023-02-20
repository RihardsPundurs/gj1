import pygame
import time

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("resources/blobbyG1.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(640, 360))
		self.gravity = 0
		self.velocity = 0
		self.on_ground = False
		self.last_jump = False
		self.plat = False
		self.respawn = 0

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] or keys[pygame.K_w]:
			if self.last_jump == False:
				print("jumped2")
				if self.on_ground == True:
					self.gravity = -40
					print("jumped1")
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

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		self.rect.x += self.velocity

	def update(self):
		self.player_input()
		self.apply_gravity()

class Block(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/girrafe.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Spike(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/spike.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Platform(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/branch.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
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
		self.image = pygame.image.load("resources/branch.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
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
		self.image = pygame.image.load("resources/Log.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))
