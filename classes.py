import pygame

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

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] or keys[pygame.K_w]:
			if self.last_jump == False:
				print("jumped2")
				if self.on_ground == True:
					self.gravity = -20
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
		self.image = pygame.transform.scale(self.image, (300, 300))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))

class Spike(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/spike.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (300, 300))
		self.rect = self.image.get_rect(center=(cords[0], cords[1]))
