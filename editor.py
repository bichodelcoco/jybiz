import pygame
from pygame.locals import *
from b2_classes import *
import geo
import GUI

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

	bigmap = pygame.Surface((g.BIGMAP_WIDTH, g.BIGMAP_HEIGHT))
	bigmap.fill(WHITE)

	# --- pybox2d world setup -----------------------------------
	# Create the world
	_world = world(gravity=(0,0),doSleep=True)

	# edges
	ground= StaticObject(_world, (0, g.BIGMAP_HEIGHT - 20), (g.BIGMAP_WIDTH,15))
	leftEdge = StaticObject(_world, (0,0), (20, g.BIGMAP_HEIGHT))
	rightEdge = StaticObject(_world, (g.BIGMAP_WIDTH,0), (20, g.BIGMAP_HEIGHT))
	roof = StaticObject(_world, (0,0), (g.BIGMAP_WIDTH, 20))

	# ------- create background ---------------- subsurface of bigmap (what will be on the screen)
	background = pygame.Surface(screen.get_size()) #surface the size of the screen
	backgroundRect = background.get_rect() #create rectangle the size of background/the screen
	background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT)) #take snapshot of bigmap
	background = background.convert()


	# init
	#---------------------------------------------------------
	mainLoop = True
	freeBuild = False
	building = False
	buildRect = BuildRect()
	buildSprite = BuildSprite(buildRect)
	GUI = GUI.EditorGUI(world = _world, ground = ground)
	scrollx = 0
	scrolly = 0



	while mainLoop :
		seconds = clock.tick(TARGET_FPS) /1000.0

		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				mainLoop = False

			if event.type == MOUSEMOTION :
				cursor.update()
				if g.LEFT_CLICK :
					buildRect.mouseMotion()
				else :
					old_hover = hovered
					hovered =  pygame.sprite.spritecollide(cursor, hoverGroup, False)
					for item in old_hover not in hovered :
						item.unhover()
					for item in hovered :
						item.hover()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					if freeBuild :
						buildRect.mousePos = cursor.rect.topleft[:]
					elif building :
						pass

			elif event.type == MOUSEBUTTONUP :
				if event.button == 1:
					g.LEFT_CLICK = False
					if freeBuild :
						buildSprite.build()
					elif building :
						GUI.item.build()
			if event.type == KEYDOWN:
				if g.INPUT :
					if event.key == ENTER :
						g.INPUT.enter()
					else :
						g.INPUT(chr(event.key))
				elif event.key == 'b':
					building = True

		# -------- Scrolling  with keyboard------------------
		
		pressedKeys = pygame.key.get_pressed()
		# what happens when u press an arrow to move screen
		if pressedKeys[K_LEFT]:
			scrollx -= g.scrollStepx
		if pressedKeys[K_RIGHT]:
			scrollx += g.scrollStepx
		if pressedKeys[K_DOWN]:
			scrolly += g.scrollStepy
		if pressedKeys[K_UP]:
			scrolly -= g.scrollStepy
		# ---- scroll the screen --------
		g.CORNERPOINT[0] += scrollx
		g.CORNERPOINT[1] += scrolly
		#----- prevent scrolling out of the map
		if g.CORNERPOINT[0] < 0:
			g.CORNERPOINT[0] = 0
			scrollx = 0
		if g.CORNERPOINT[0] > g.bigmapWidth - g.width :
			g.CORNERPOINT[0] = g.bigmapWidth - g.width
			scrollx = 0
		if g.CORNERPOINT[1] < 0:
			g.CORNERPOINT[1] = 0
			scrolly = 0
		if g.CORNERPOINT[1] > g.bigmapHeight - g.height :
			g.CORNERPOINT[1] = g.bigmapHeight - g.height
			scrolly =0
					

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

	# --- pybox2d world setup -----------------------------------
	# Create the world
	_world = world(gravity=(0,-10),doSleep=True)

	# And a static body to hold the ground shape
	ground=_world.CreateStaticBody(
	    position=(0,0),
	    shapes=polygonShape(box=(3000/PPM,50/PPM)),
	    )

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




