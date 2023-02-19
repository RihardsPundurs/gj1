import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self):
        super().__init__()
        self.image = pygame.image.load("").convert_alpha()
        self.image = pygame.transform.scale(self.image, (val1, val2))
        self.rect = self.image.get_rect(topright=(val1, val2))

class Block(pygame.sprite.Sprite):
	def __init__(self, cords):
		super().__init__()
		self.cords = cords
        self.image = pygame.image.load("").convert_alpha()
        self.image = pygame.transform.scale(self.image, (val1, val2))
        self.rect = self.image.get_rect(topright=(val1, val2))
