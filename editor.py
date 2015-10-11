import pygame
from pygame.locals import *
from b2_classes import *
import geo
import GUI
import shelve


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

class Blueprint(pygame.sprite.Sprite):
	def __init__(self, size):

		self.groups = allGroup
		
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface(size)
		self.image.fill(BLUE)
		self.image.set_alpha(100)
		self.rect = self.image.get_rect()

	def update(self, seconds):
		self.rect.center = cursor.rect.topleft



def editor(mapFilepath):
	# Pygame set up
	# -----------------------------------------------------------
	screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
	pygame.display.set_caption('Simple pygame example')
	clock=pygame.time.Clock()
	pygame.font.init()

	bigmap = pygame.Surface((g.BIGMAP_WIDTH+SCREEN_WIDTH, g.BIGMAP_HEIGHT+SCREEN_HEIGHT))
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
	deleteMode = False
	modeList = [freeBuild, building, deleteMode]
	buildRect = BuildRect()
	
	itemList = [Ledge, Doodad, Crate]
	itemList_index = 0
	gui = GUI.EditorGUI(world = _world, ground = ground, item = Ledge)
	scrollx = 0
	scrolly = 0
	hovered =  pygame.sprite.spritecollide(cursor, hoverGroup, False)
	infoBox = GUI.TextBox(pos = (0, SCREEN_HEIGHT -20), width = 300, height = 20, fontSize = 16)
	infoString = ''
	blueprint = Blueprint((1,1))

	load(mapFilepath, _world, ground, gui)



	while mainLoop :
		seconds = clock.tick(TARGET_FPS) /1000.0

		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				mainLoop = False

			if event.type == MOUSEMOTION :
				cursor.update()
				if freeBuild :
					if g.LEFT_CLICK :
						buildRect.mouseMotion()
				else :
					old_hover = hovered
					hovered =  pygame.sprite.spritecollide(cursor, hoverGroup, False)
					temp = [item for item in old_hover if item not in hovered]
					for item in temp :
						item.unhover()
					for item in hovered :
						item.hover()

			if event.type == MOUSEBUTTONDOWN :
				if event.button == 1:
					g.LEFT_CLICK = True
					if building :
						pass
					elif freeBuild :
						buildSprite = buildSprite = BuildSprite(buildRect)
						buildRect.mousePos = cursor.rect.topleft[:]

					else :
						if hovered:
							hovered[0].click()

			elif event.type == MOUSEBUTTONUP :
				if event.button == 1:
					g.LEFT_CLICK = False
					if freeBuild :
						gui.freeBuild(buildRect)
						buildSprite.kill()
					if building :
						gui.build(cursor.rect.topleft)
					elif deleteMode:
						if hovered:
							if terrainGroup in hovered[0].groups:
								hovered[0].kill()
								for values in gui.itemList:
									if values[0] == hovered[0]:
										gui.itemList.remove(values)

			if event.type == KEYDOWN:
				if g.INPUT :
					if event.key == K_RETURN :
						g.INPUT.enter()
					elif event.key < 257:
						g.INPUT.input(chr(event.key))
				elif event.key == K_b: #switch from and to building mode
					building = not building
					blueprint.kill()
					if building :
						blueprint = Blueprint((gui.slots[0].output(), gui.slots[1].output()))
				elif event.key == K_f :
					freeBuild = not freeBuild


				elif event.key == K_c: #cycle through buildable items
					itemList_index = (itemList_index + 1)%len(itemList)
					gui.loadItem(itemList[itemList_index])
				elif event.key == K_x : #delete mode
					deleteMode = not deleteMode

		#update infoBox with the stuff
		infoString = ''
		if g.INPUT:
			infoString += '- input ENTER '
		if building:
			infoString += '- building B '
		if deleteMode:
			infoString += '- deleteMode X '
		if freeBuild:
			infoString += '- freeBuild F'
		infoBox.writeText(infoString)

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
			g.CORNERPOINT[0]=0
			scrollx = 0
		elif g.CORNERPOINT[0] > g.BIGMAP_WIDTH - SCREEN_WIDTH :
			g.CORNERPOINT[0] = g.BIGMAP_WIDTH - SCREEN_WIDTH
			scrollx = 0
		if g.CORNERPOINT[1] < 0:
			g.CORNERPOINT[1] = 0
			scrolly = 0
		elif g.CORNERPOINT[1] > g.BIGMAP_HEIGHT - SCREEN_HEIGHT :
			g.CORNERPOINT[1] = g.BIGMAP_HEIGHT - SCREEN_HEIGHT
			scrolly =0
		scrollx = 0
		scrolly = 0
					

		# ---- update shit and draw allGroup ----------------
		background = bigmap.subsurface((g.CORNERPOINT[0], g.CORNERPOINT[1], SCREEN_WIDTH, SCREEN_HEIGHT))
		screen.blit(background, (0,0))
		allGroup.update(seconds)
		allGroup.draw(screen)
		pygame.display.flip()

	tempList = []
	for item in gui.itemList:
		tempList.append((item[1],item[2],item[3]))
	save(FILEPATH, tempList)

	for item in allGroup:
		item.kill()
	temp = []
	for body in _world:
		temp.append(body)
	for body in temp:
		_world.DestroyBody(body)
		temp.remove(body)

def save(filepath, itemList):
	f = shelve.DbfilenameShelf(filepath, flag='c', protocol=None, writeback=False)
	f['itemNumber'] = len(itemList)
	index =0
	for item in itemList:
		f[str(index)]= item
		index += 1
	f.close()

def load(filepath, world, ground, editorGui = None):
	f = shelve.DbfilenameShelf(filepath, flag='r', protocol=None, writeback=False)
	itemList =[]
	itemNumber =f['itemNumber']
	for i in xrange(itemNumber):
		itemList.append(f[str(i)])


	
	for i in xrange(itemNumber):
		item = itemList[i]
		values = item[2]
		pos = item[1]
		name = item[0]
		
		if name == 'Ledge':
			temp = Ledge(world, ground, pos, width = values[0], height = values[1], color = values[2], allowedAngle = (-values[3],values[4]))		
		elif name == 'Doodad':
			temp =Doodad(world, ground, pos, width = values[0], height = values[1], color = values[2], density = values[3])
		elif name == 'Crate':
			temp = Crate(world, pos)
		if editorGui :
			editorGui.itemList.append((temp, name, pos, values))
	
	
	f.close()







