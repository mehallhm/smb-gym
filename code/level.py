import pygame 
from tiles import * 
from settings import tile_size, screen_width
from player import Player

class Level:
	def __init__(self, level_data, surface):
		
		# level setup
		self.display_surface = surface 
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()

		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				x = col_index * 16
				y = row_index * 16
				
				if cell == 'X':
					tile = Block((x, y), '../graphics/environment/block.png')
					self.tiles.add(tile)
				if cell == 'L':
					tile = Brick_block((x, y), '../graphics/environment/brick.png')
					self.tiles.add(tile)
				if cell == '?':
					tile = Question_block((x, y), '../graphics/environment/q_block_tilemap.png')
					self.tiles.add(tile)
				if cell == 'C':
					# tile = Coin((x,y), ['../graphics/environment/coin.png', '../graphics/environment/coin2.png', '../graphics/environment/coin3.png', '../graphics/environment/coin4.png'])
					tile = Coin((x,y), '../graphics/environment/coin_tilemap.png')
					self.tiles.add(tile)
				if cell == 'P':
					player_sprite = Player((x,y),self.display_surface)
					self.player.add(player_sprite)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x > screen_width - (screen_width / 2) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					if not sprite.collide(): 
						player.rect.left = sprite.rect.right
						player.on_left = True
						self.current_x = player.rect.left
				elif player.direction.x > 0:
					if not sprite.collide():
						player.rect.right = sprite.rect.left
						player.on_right = True
						self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			sprite.animate()
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					if not sprite.collide():
						player.rect.bottom = sprite.rect.top
						player.direction.y = 0
						player.on_ground = True
				elif player.direction.y < 0:
					if not sprite.collide():
						player.rect.top = sprite.rect.bottom
						player.direction.y = -1
						player.on_ceiling = True
						sprite.bump(player.state, player)
					

		if player.on_ground and (player.direction.y < 0 or player.direction.y > 1):
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def run(self):
		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()


		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)
		
