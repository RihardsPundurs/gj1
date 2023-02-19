import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("resources/blobbyG1.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (150, 150))
		self.rect = self.image.get_rect(center=(640, 360))
		self.gravity = 0
		self.velocity = 0

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] or keys[pygame.K_w]:
			self.gravity = -10
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
	def __init__(self, cords = None):
		super().__init__()
		self.cords = cords
		self.image = pygame.image.load("resources/girrafe.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (300, 300))
		self.rect = self.image.get_rect(topright=(500, 300))
