import pygame 
from imports import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface):
		super().__init__()
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		# self.image = self.animations['idle'][self.frame_index]
		self.image = pygame.image.load('../graphics/mario.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.ground_y = 2 * 16

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 1
		self.gravity = 0.4
		self.jump_speed = -6
		self.walk_speed = 0.4

		# player status
		self.status = 'idle'
		self.facing_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.state = 1

	def import_character_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		# animation = self.animations[self.status]

		# # loop over frame index 
		# self.frame_index += self.animation_speed
		# if self.frame_index >= len(animation):
		# 	self.frame_index = 0

		# image = animation[int(self.frame_index)]

		if self.state == 1:
			image = pygame.image.load('../graphics/bigmario.png').convert_alpha()
			self.rect = image.get_rect(topleft = self.rect.topleft)
		else:
			image = pygame.image.load('../graphics/mario.png').convert_alpha()
			self.rect = image.get_rect(topleft = self.rect.topleft)

		if self.facing_right:
			self.image = image
		else:
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		# set the rect
		# if self.on_ground and self.on_right:
		# 	self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		# elif self.on_ground and self.on_left:
		# 	self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		# elif self.on_ground:
		# 	self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		# elif self.on_ceiling and self.on_right:
		# 	self.rect = self.image.get_rect(topright = self.rect.topright)
		# elif self.on_ceiling and self.on_left:
		# 	self.rect = self.image.get_rect(topleft = self.rect.topleft)
		# elif self.on_ceiling:
		# 	self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = self.walk_speed
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -self.walk_speed
			self.facing_right = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump()
		
		# prevent player from going past screen edge
		self.rect.clamp_ip(pygame.Rect((0,0), pygame.display.get_window_size()))

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		