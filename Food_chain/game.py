import pygame
from models import Bambi, Lion

class FoodChain:
	BLOCK_SIZE = 20
	
	def __init__(self):
		self._init_pygame()
		self.screen = pygame.display.set_mode((480, 480))
		self.clock = pygame.time.Clock()
		self.sheep = Bambi((100, 100), (self.BLOCK_SIZE, self.BLOCK_SIZE))
		self.lion = Lion((140, 140), (self.BLOCK_SIZE, self.BLOCK_SIZE))

	def main_loop(self):
		while True:
			self._process_game_logic()
			self._draw()

	def _init_pygame(self):
		pygame.init()
		pygame.display.set_caption("Food chain")

	def _process_game_logic(self):
		self.sheep.move()
		self.lion.move()
		self.sheep.look(self._get_game_objects())
		self.lion.look(self._get_game_objects())
		self.sheep.think()

	def _draw(self):
		self.screen.fill((255, 255, 255))
		self.sheep.draw(self.screen)
		self.lion.draw(self.screen)
		pygame.display.flip()
		self.clock.tick(self.BLOCK_SIZE)

	def _get_game_objects(self):
		return [self.sheep, self.lion]
		