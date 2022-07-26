import math
import pygame, sys
from settings import * 
from level import Level

# Pygame setup
pygame.init()


window = pygame.display.set_mode([screen_width * 2, screen_height * 2])
w = pygame.Surface([screen_width, screen_height])

# def draw():
	

# screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
# level = Level(level_map,screen)
level = Level(level_map,w)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	level.run()

	pygame.display.set_caption(f'SMB Gym - FPS:{math.floor(clock.get_fps())}')
	frame = pygame.transform.scale(w, (screen_width * 2, screen_height * 2))
	window.blit(frame, frame.get_rect())
	# w.fill(pygame.Color(0,0,0,0))
	w.fill('#6A96FC')
	pygame.display.update()

	clock.tick(60)