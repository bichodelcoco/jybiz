import pygame
from b2_classes import *
import textrect


INT = 1
TUPLE = 2
COLOR = 2


''' ------------ GUI ---------- '''
class EditorGUI(object): #contains value boxes

	def __init__(self, world = None, ground = None, item = None):

		self.world = world
		self.ground = ground

		self.slots = [0 for i in xrange(10)]
		self.posList = []
		self.nameBox = TextBox(pos = (SCREEN_WIDTH - 130, 30), width = 100, height = 20, fontSize = 16, justification = 1)

		self.loadItem(item)
		self.displayedItem = None
		self.itemList = []

	def loadItem(self, item):
		self.nameBox.writeText(item.__name__)
		for i in xrange(10):
			if self.slots[i]:
				self.slots[i].kill()
		self.slots = [0 for i in xrange(10)]
		self.item = item
		if item.__name__ == 'Ledge' :
			self.slots[0] = PropertyBox('width', INT)
			self.slots[1] = PropertyBox('height', INT)
			self.slots[2] = PropertyBox('color', INT)
			self.slots[3] = PropertyBox('lAngle', INT)
			self.slots[4] = PropertyBox('uAngle', INT)
		elif item.__name__ == 'Doodad' :
			self.slots[0] = PropertyBox('width', INT)
			self.slots[1] = PropertyBox('height', INT)
			self.slots[2] = PropertyBox('color', INT)
			self.slots[3] = PropertyBox('density', INT)
		elif item.__name__ == 'Crate':
			pass




		for i in xrange(10):
			if self.slots[i]:
				self.slots[i].leftpoint = (SCREEN_WIDTH - 160, 100 + i*40)
				self.slots[i].update()
		self.displayedItem = self.item


	def build(self, mousePos):
		values = [0 for i in xrange(10)]
		if self.item.__name__ == 'Ledge':

			for i in xrange(5):
				temp = self.slots[i].output()
				if temp:
					if i == 2:
						if temp == 1:
							values[i] = BLACK
						elif temp == 2:
							values[i] = RED
						elif temp == 3:
							values[i] = BLUE
					else :
						values[i] = temp
				#defaulft values if temp( output ) = 0
				elif i == 0:
					values[i] = 300
				elif i == 1:
					values[i] = 20
				elif i == 2:
					values[i]= BLACK
				elif i==3 or i ==4:
					values[i]= 0
			tempItem = Ledge(self.world, self.ground, unrect(mousePos), width = values[0], height = values[1], color = values[2], allowedAngle = (-values[3],values[4]))


		elif self.item.__name__ == 'Doodad':
			for i in xrange(4):
				temp = self.slots[i].output()
				if temp:
					if i == 2:
						values[i] = findColor(temp)
					else :
						values[i] = temp
				elif i == 0:
					values[i] = 100
				elif i == 1:
					values[i] = 100
				elif i == 2:
					values[i]= BROWN
				elif i == 3:
					values[i]= 1
			tempItem = Doodad(self.world, self.ground, unrect(mousePos), width = values[0], height = values[1], color = values[2], density = values[3])

		elif self.item.__name__ == 'Crate' :
			tempItem = Crate(self.world, unrect(mousePos))


		self.itemList.append((tempItem,self.item.__name__, tempItem.pos, values))

	def update(self):
		if self.item != self.displayedItem:
			self.loadItem(self.item)


	def run(self):
		if self.visible :
			for button in self.buttons :
				allGroup.add(button)
				buttonGroup.add(button)
				hoverGroup.add(button)
			for textBox in self.textBoxes :
				allGroup.add(button)

	def hide(self):
		self.visible = False
		for button in buttons :
			allGroup.remove(button)
			buttonGroup.remove(button)
			hoverGroup.remove(button)
		for textBox in self.textBoxes :
			allGroup.remove(button)

	def show(self):
		self.visible = True
		for button in self.buttons :
			allGroup.add(button)
			buttonGroup.add(button)
			hoverGroup.add(button)
		for textBox in self.textBoxes :
			allGroup.add(button)


class ValueBox(pygame.sprite.Sprite):
	#carre de x sur y blanc entoure de noir dans lequel on peut entrer des valeures

	def __init__(self, leftpoint, value_type, height = 20):
		self.width = 60
		self.height = height
		self.textBox = TextBox(pos = leftpoint, width = 100, height = self.height, fontSize = 16, background_color = BRIGHTGREEN)
		self.value_type = value_type
		self.string = ''
		self.value_index = 0
		self.value_strings = ['' for i in xrange(20)]

		self.groups = allGroup, hoverGroup
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.Surface((60,self.height))
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.topleft = leftpoint



	def hover(self):
		print 'hover'
		self.textBox.background_color = RED
		# 	pygame.draw.rect(self.image, BLACK, self.textBox.rect, width = 5 )

	def unhover(self):
		print 'unhover'
		self.textBox.background_color = BRIGHTGREEN
		# if g.INPUT != self:
		# 	pygame.draw.rect(self.image, WHITE, self.textBox.rect, width = 5 )

	def click(self):
		print 'click'
		g.INPUT = self

		self.string = ''
		self.textBox.writeText(self.string)
		# pygame.draw.rect(self.image, RED, self.textBox.rect, width = 5 )
	def enter(self):
		g.INPUT = False



	def input(self, letter):
		self.string += letter
		self.textBox.writeText(self.string)

	def output(self):
		value_index = 0
		if self.string == '':
			return 0
		if self.value_type == INT:
			return int(self.string)

		elif self.value_type == TUPLE :
			for i in xrange(len(self.string)):
				if self.string[i] != "," :
					self.value_strings[value_index] += self.string[i]
				else :
					value_index +=1
			value_index += 1
			if value_index == 2 :

				return (self.value_strings[0],self.value_strings[1])
			if value_index == 3:
				print (self.value_strings[0],self.value_strings[1], self.value_strings[2])
				return (int(self.value_strings[0]),int(self.value_strings[1]), int(self.value_strings[2]))

	def kill(self):
		self.textBox.kill()
		pygame.sprite.Sprite.kill(self)

	def update(self, seconds):
		self.textBox.rect.topleft = self.rect.topleft
		self.textBox.refresh()
		pygame.sprite.Sprite.update(self,seconds)




# class JustText(pygame.sprite.Sprite)
# 	def __init__(self, pos = (0,0), width = 624, height = 120, text_color = BLACK, background_color = None, text = '', fontSize = 32, font = None, justification = 0):

# 		self.groups = allGroup
# 		pygame.sprite.Sprite.__init__(self, self.groups)

# 		self.font = pygame.font.SysFont('None', fontSize)

# 		self.rect = pygame.Rect(pos, (width, height))

# 		self.text = text
# 		self.background_color = background_color
# 		self.old_color = self.background_color
# 		self.text_color = text_color
# 		self.justification = justification
# 		self.writeText(text)


# Text box, a Sprite containing Text
#------------------------------------------------------------------------------------------------------
class TextBox(pygame.sprite.Sprite):

	def __init__(self, pos = (0,0), width = 624, height = 120, text_color = BLACK, background_color = None, text = '', fontSize = 32, font = None, justification = 0):

		self.groups = allGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.font = pygame.font.SysFont('None', fontSize)

		self.rect = pygame.Rect(pos, (width, height))

		self.text = text
		self.background_color = background_color
		self.old_color = self.background_color
		self.text_color = text_color
		self.justification = justification
		self.writeText(text)

	def addText(self, text) :
		self.text = text + self.text
		self.writeText(self.text)

	def writeText(self, text):
		if self.background_color :
			self.image = textrect.render_textrect(text, self.font, self.rect, self.text_color, self.background_color, justification = self.justification)
		else :
			self.image = textrect.render_textrect(text, self.font, self.rect, self.text_color,WHITE, justification = self.justification)
			self.image.set_colorkey(WHITE)
		self.text = text

	def refresh(self):
		if self.old_color != self.background_color:
			self.image = textrect.render_textrect(self.text, self.font, self.rect, self.text_color, self.background_color, justification = self.justification)
			self.old_color = self.background_color



class PropertyBox(object):
	# contient une TextBox et une ValueBox pour self.property
	def __init__(self, name, value_type, leftpoint = (0,0)):
		self.name = name
		self.value_type = value_type
		self.leftpoint = leftpoint
		self.textBox = TextBox(leftpoint, width =60, height = 80, text_color = BLACK, background_color = None, text = name, fontSize = 16, font = None, justification = 0)
		self.valueBox = ValueBox((leftpoint[0]+80, leftpoint[1]), value_type = value_type)

	def kill(self):
		self.textBox.kill()
		self.valueBox.kill()

	def update(self):
		self.textBox.rect.topleft = self.leftpoint
		self.valueBox.rect.topleft = (self.leftpoint[0]+80, self.leftpoint[1])

	def output(self):
		return self.valueBox.output()









# GUI Icons
# ---------------------------------------------------------

class Icon(pygame.sprite.Sprite):
	def __init__(self, pos, imagepath = None, size =(40,40)):

		self.groups = allGroup, guiGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.image.load(imagepath)
		self.rect = self.image.get_rect()

		self.rect.topleft = pos[:]

class WeaponIcon(Icon):

	def __init__(self, pos, weapon = None):

		self.weapon = weapon

		if self.weapon.__class__.__name__ == 'Rifle' :
			imagepath = 'images/icons/rifle_icon.png'
		elif self.weapon.__class__.__name__== 'BaseballBat' :
			imagepath = 'images/icons/baseballbat_icon.png'
		elif self.weapon.__class__.__name__== 'GrapplingHook' :
			imagepath = 'images/icons/hook_icon.png'
		elif self.weapon.__class__.__name__== 'Grenade' :
			imagepath = 'images/icons/grenade_icon.png'
		elif self.weapon.__class__.__name__== 'megaBall' :
			imagepath = 'images/icons/megaball_icon.png'
		elif self.weapon.__class__.__name__== 'Hadouken' :
			imagepath = 'images/icons/hadouken_icon.png'
		elif self.weapon.__class__.__name__== 'BouncingBall' :
			imagepath = 'images/icons/bouncingball_icon.png'
		elif self.weapon.__class__.__name__== 'FragmentedBall' :
			imagepath = 'images/icons/frag_icon.png'
		elif self.weapon.__class__.__name__== 'MiniBouncingBall' :
			imagepath = 'images/icons/minibouncingball_icon.png'


		Icon.__init__(self, pos, imagepath)

# ------------------------------------------------------------------------------------

# Player lifeBar

class PlayerLifebar(pygame.sprite.Sprite):
	"""docstring for PlayerLifebar"""
	def __init__(self,gui, color = RED):
		
		self.image0 = pygame.image.load('images/lifebars/player_lifebar.png').convert()
		setColorkey(self.image0)
		self.color= color
		self.player = gui.player
		self.percent = 1.0
		self.old_playerHitpoints = self.player.maxHitpoints
		
		


		self.groups = allGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = self.image0
		self.rect= self.image.get_rect()

		self.rect.topleft = (5, 5)
		self.hitpointsInfoBox = TextBox((105,32), width =200, height = 30, text_color = BLACK, background_color = None, text = str(int(self.player.hitpoints)) + '/'+str(self.player.maxHitpoints), fontSize = 20, font = None, justification = 0)

		self.refresh()


	def update(self, seconds):
		if self.player.hitpoints != self.old_playerHitpoints:
			self.percent = self.player.hitpoints*1.0 / (self.player.maxHitpoints*1.0)
			self.old_playerHitpoints = self.player.hitpoints
			self.refresh()

	def refresh(self):
		self.hitpointsInfoBox.writeText(str(int(self.player.hitpoints)) + '/'+str(self.player.maxHitpoints))
		if self.percent != 1.0:

			self.image = self.image0
			pygame.draw.rect(self.image, self.color, (406- (1-self.percent)*397, 7,  (1-self.percent)*397,12))
		else :
			self.image = self.image0

		
class GameGUI(object):

	def __init__(self, world, ground, player = None):

		self.world = world
		self.ground = ground
		self.player = player

		self.weaponslot1 = WeaponIcon((SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80),weapon =self.player.weapon1)
		self.weaponslot2 = WeaponIcon((SCREEN_WIDTH - 90, SCREEN_HEIGHT - 80),weapon =self.player.weapon2)

		self.weapon1NameBox = TextBox(pos =(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 30), width = 60, height = 20, text = self.player.weapon1.__class__.name, fontSize = 14, justification = 1)
		self.weapon2NameBox = TextBox(pos =(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30), width = 60, height = 20, text = self.player.weapon2.__class__.name, fontSize = 14, justification = 1)

		self.playerLifebar = PlayerLifebar(self)

	def update(self):
		if self.weaponslot1.weapon != self.player.weapon1 :
			self.weaponslot1.kill()
			self.weaponslot1 = WeaponIcon((SCREEN_WIDTH - 150, SCREEN_HEIGHT - 80),weapon =self.player.weapon1)
			self.weapon1NameBox.writeText(self.player.weapon1.__class__.name)

		if self.weaponslot2.weapon != self.player.weapon2 :
			self.weaponslot2.kill()
			self.weaponslot2 = WeaponIcon((SCREEN_WIDTH - 90, SCREEN_HEIGHT - 80),weapon =self.player.weapon2)
			self.weapon2NameBox.writeText(self.player.weapon2.__class__.name)
