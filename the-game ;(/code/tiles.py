from abc import abstractclassmethod
import pygame
import constants as c

class Tile(pygame.sprite.Sprite):
	def __init__(self) -> None:
		super().__init__()
	
	def update(self, x_shift) -> None:
		self.rect.x += x_shift
		try:
			self.update_block_state()
		except:
			return
	
	@abstractclassmethod 
	def animate(self):
		pass
	
	@abstractclassmethod 
	def bump(self):
		pass

	@abstractclassmethod
	def collide(self, direction, level, player):
		pass

class Block(Tile):
	def __init__(self, pos, asset) -> None:
		super().__init__()
		self.image = pygame.Surface((16, 16))
		self.image.blit(pygame.image.load(asset).convert(), (0, 0))
		self.rect = self.image.get_rect(topleft = pos)

class Brick_block(Block):
	def __init__(self, pos, art):
		super().__init__(pos, art)
		self.rest_height = pos[1]
		self.gravity = 1.2
		self.y_vel = 0
		self.bumped = False
		self.broke = False

	def update_block_state(self):
		if (self.bumped):
			self.rect.y += self.y_vel
			self.y_vel += self.gravity

			if self.rect.y >= self.rest_height - 2:
				self.rect.y = self.rest_height

				self.bumped = False
				if self.broke:
					self.kill()
	
	# def bump(self, mario_state, player):
	# 	if not self.bumped:
	# 		self.y_vel = -3
	# 		self.bumped = True
	# 		if mario_state > 0:
	# 			self.broke = True
	
	def collide(self, direction, level, player):
		if direction == c.BOTTOM and not self.bumped:
			self.y_vel = -3
			self.bumped = True
			if player.state > 0:
				self.broke = True
		
class Question_block(Tile):
	def __init__(self, pos, tileset):
		super().__init__()
		self.broken = False
		self.image = pygame.Surface((16, 16))
		self.image.blit(pygame.image.load(tileset).convert_alpha(), (0, 0), (0, 0, 16, 16))
		self.rect = self.image.get_rect(topleft = pos)
		self.tileset = tileset
		self.animation_speed = 0.07
		self.animation_index = 0

		self.rest_height = pos[1]
		self.gravity = 1.2
		self.y_vel = 0
		self.bumped = False	

	def update_block_state(self):
		if (self.bumped):
			self.rect.y += self.y_vel
			self.y_vel += self.gravity

			if self.rect.y >= self.rest_height - 2:
				self.rect.y = self.rest_height

				self.broken = True
				self.image.blit(pygame.image.load("../graphics/environment/flat.png").convert(), (0, 0))

				self.bumped = False
	
	# def bump(self, mario_state, player):
	# 	if not self.broken and not self.bumped :
	# 		self.y_vel = -3
	# 		self.bumped = True
	
	def collide(self, direction, level, player):
		if direction == c.BOTTOM and not self.broken and not self.bumped :
			self.y_vel = -3
			self.bumped = True

	def animate(self):
		if not self.broken:
			self.animation_index += self.animation_speed
			anim_index = int(self.animation_index)
			self.image.blit(pygame.image.load(self.tileset).convert_alpha(), (0, 0), (0 + anim_index * 16, 0, 16, 16))
			if self.animation_index > 3:
				self.animation_index = 0

class Coin(Tile):
	def __init__(self, pos, tileset):
		super().__init__()
		self.image = pygame.Surface((10, 14))
		self.image.blit(pygame.image.load(tileset).convert_alpha(), (0, 0), (0, 0, 10, 14))
		self.rect = self.image.get_rect(topleft = pos)
		self.tileset = tileset
		self.animation_speed = 0.07
		self.animation_index = 0

	def collide(self, direction, level, player):
		self.kill()
		return True
	
	def animate(self):	
		self.animation_index += self.animation_speed
		anim_index = int(self.animation_index)
		self.image.blit(pygame.image.load(self.tileset).convert_alpha(), (0, 0), (0 + anim_index * 16, 0, 10, 14))
		if self.animation_index > 3:
			self.animation_index = 0
