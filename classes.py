import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self):
	    super().__init__()
	    self.image = pygame.image.load("").convert_alpha()
	    self.image = pygame.transform.scale(self.image, (val1, val2))
	    self.rect = self.image.get_rect(topright=(val1, val2))
	    self.gravity = 0
	    self.velocity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_W]:
            self.gravity = -6
        if keys[pygame.K_A] and self.velocity <= 30:
        	self.velocity += 1
        elif keys[pygame.K_A] and self.velocity >= -30:
        	self.velocity -= 1
        else:
        	if self.velocity < 0:
        		self.velocity += 4
        	elif self.velocity > 0:
        		self.velocity -= 4

    def apply_gravity(self):
        self.gravity += 0.1
        self.rect.y += self.gravity

    def update(self):
        self.player_input()
        self.apply_gravity()

class Block(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
        self.image = pygame.image.load("").convert_alpha()
        self.image = pygame.transform.scale(self.image, (val1, val2))
        self.rect = self.image.get_rect(topright=(val1, val2))
