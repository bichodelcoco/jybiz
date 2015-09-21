import pygame
from pygame.locals import *
from b2_classes import *
import geo

# class Map(object)
# 	def __init__(self, size, file):
# 		self.grid = [[0 for i in xrange(size[0])] for i in xrange(size[1])
# 		#open file and load contents into grid

# 	def draw(self):
# 		for i in xrange(self.size[0]):
# 			ID_Dictionnary[self.grid[]]

# class Locals(object):

#class GUI(object):

class testItem(pygame.sprite.Sprite):
	def __init__(self, topleft, size):
		pygame.sprite.Sprite.__init__(self, allGroup)
		
		self.image = pygame.Surface(size)
		self.image.fill(BLACK)
		self.rect = pygame.Rect(topleft, size)



class BuildRect(pygame.Rect):

	def __init__(self):
		self.mousePos = cursor.rect.topleft
		pygame.Rect.__init__(self, (0,0), (0,0))

	def mouseMotion(self):
		self.new_mousePos = cursor.rect.topleft

		offset = (self.new_mousePos[0]- self.mousePos[0], self.new_mousePos[1]- self.mousePos[1])
		# down
		if offset[1] >= 0:
			#right
			if offset[0] >= 0:
				self.topleft = self.mousePos[:]
				self.size = offset[:]
			#left
			else :
				self.topleft = (self.new_mousePos[0], self.mousePos[1])
				self.size = (geo.absolute(offset[0]),geo.absolute(offset[1]))

		# up
		else :
			#right
			if offset[0] >= 0:
				self.topleft =(self.mousePos[0], self.new_mousePos[1])
				self.size = (geo.absolute(offset[0]),geo.absolute(offset[1]))
			#left
			else :
				self.topleft = self.new_mousePos[:]
				self.size = (geo.absolute(offset[0]),geo.absolute(offset[1]))


class BuildSprite(pygame.sprite.Sprite):

	def __init__(self, buildRect):

		self.groups = allGroup
		self.buildRect= buildRect
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface((100,100))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()

	def update(self, seconds):
		self.rect = self.buildRect
		self.image = pygame.Surface(self.buildRect.size)
		self.image.fill(BLUE)
		self.image.set_alpha(100)

	def build(self):

		
		g.OBJECTS.append(testItem(self.rect.topleft, self.rect.size))


def editor():
	# Pygame set up
	# -----------------------------------------------------------
	screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
	pygame.display.set_caption('Simple pygame example')
	clock=pygame.time.Clock()

	bigmap = pygame.Surface((BIGMAP_WIDTH, BIGMAP_HEIGHT))
	bigmap.fill(WHITE)

	# ------- create background ---------------- subsurface of bigmap (what will be on the screen)
	background = pygame.Surface(screen.get_size()) #surface the size of the screen
	backgroundRect = background.get_rect() #create rectangle the size of background/the screen
	background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT)) #take snapshot of bigmap
	background = background.convert()


	# init
	#---------------------------------------------------------
	mainLoop = True
	buildRect = BuildRect()
	buildSprite = BuildSprite(buildRect)



	while mainLoop :
		seconds = clock.tick(TARGET_FPS) /1000.0

		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				mainLoop = False

			if event.type == MOUSEMOTION :
				cursor.update()
				if g.LEFT_CLICK :
					buildRect.mouseMotion()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					buildRect.mousePos = cursor.rect.topleft[:]

			elif event.type == MOUSEBUTTONUP :
				if event.button == 1:
					g.LEFT_CLICK = False
					buildSprite.build()
					

		# ---- update shit and draw allGroup ----------------
		background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT))
		screen.blit(background, (0,0))
		allGroup.update(seconds)
		allGroup.draw(screen)
		pygame.display.flip()

def run():
	# Pygame set up
	# -----------------------------------------------------------
	screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
	pygame.display.set_caption('Simple pygame example')
	clock=pygame.time.Clock()

	bigmap = pygame.Surface((BIGMAP_WIDTH, BIGMAP_HEIGHT))
	bigmap.fill(WHITE)
	allGroup.empty()

	# ------- create background ---------------- subsurface of bigmap (what will be on the screen)
	background = pygame.Surface(screen.get_size()) #surface the size of the screen
	backgroundRect = background.get_rect() #create rectangle the size of background/the screen
	background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT)) #take snapshot of bigmap
	background = background.convert()


	# init
	#---------------------------------------------------------
	mainLoop = True
	for item in g.OBJECTS :
		allGroup.add(item)



	while mainLoop :
		seconds = clock.tick(TARGET_FPS) /1000.0

		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				mainLoop = False

			if event.type == MOUSEMOTION :
				cursor.update()
				if g.LEFT_CLICK :
					buildRect.mouseMotion()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					buildRect.mousePos = cursor.rect.topleft[:]

			elif event.type == MOUSEBUTTONUP :
				if event.button == 1:
					g.LEFT_CLICK = False
					buildSprite.build()
					

		# ---- update shit and draw allGroup ----------------
		background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT))
		screen.blit(background, (0,0))
		allGroup.update(seconds)
		allGroup.draw(screen)
		pygame.display.flip()

editor()
run()




