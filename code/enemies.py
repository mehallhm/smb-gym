from abc import abstractclassmethod
import pygame
import constants as c

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, size, tileset) -> None:
		super().__init__()
		self.image = pygame.Surface((size[0], size[1]))
		self.image.blit(pygame.image.load(tileset).convert_alpha(), (0, 0), (0, 0, size[0], size[1]))
		self.rect = self.image.get_rect(topleft = pos)

	def update(self, x_shift) -> None:
		self.rect.x += x_shift
		self.move()
	
	@abstractclassmethod
	def move(self) -> None:
		pass

	@abstractclassmethod
	def collide(self, direction, level, player):
		pass
	
	@abstractclassmethod
	def animate(self) -> None:
		pass

class Goomba(Enemy):
	def __init__(self, pos, size, tileset) -> None:
		super().__init__(pos, size, tileset)
	
	def move(self):
		self.rect.x -= 1
	
	def collide(self, direction, level, player):
		if direction == c.LEFT or direction == c.RIGHT or direction == c.STAND:
			player.kill()
		if direction == c.TOP:
			self.kill()
