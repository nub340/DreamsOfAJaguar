import pygame, sys

WIDTH = 800
HEIGTH = 600
FPS = 60

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Mayan Tower Defense (CS50P Final)')
		self.clock = pygame.time.Clock()
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			pygame.display.update()
			self.clock.tick(FPS)