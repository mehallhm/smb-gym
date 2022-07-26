from abc import abstractclassmethod
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, tileset) -> None:
        super().__init__()
        self.image = pygame.Surface((size[0], size[1]))
        self.image.blit(pygame.image.load(tileset).convert(), (0, 0), (0, 0, size[0], size[1]))
        self.rect = self.image.get_rect(topleft = pos)

