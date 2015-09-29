import pygame
from b2_classes import *
import textrect


INT = 1
TUPLE = 2
COLOR = 3

''' ------------ GUI ---------- '''
class EditorGUI(object): #contains value boxes
	
	def __init__(self, world = None, ground = None, item = None):

		self.world = world
		self.ground = ground

		self.slots = [0 for i in xrange(10)]
		self.posList = []

		self.loadItem(item)
		self.displayedItem = None

	def loadItem(self, item):
		for i in xrange(10):
			if self.slots[i]:
				self.slots[i].kill()
		self.slots = [0 for i in xrange(10)]
		self.item = item
		if className(item) == 'Ledge' :
			self.slots[0] = PropertyBox('width', INT)
			self.slots[1] = PropertyBox('height', INT)
			self.slots[2] = PropertyBox('color', TUPLE)
			self.slots[3] = PropertyBox('allowedAngle', TUPLE)




		for i in xrange(10):
			if self.slots[i]:
				self.slots[i].topleft = (SCREEN_WIDTH - 160, 100 + i*80)
		self.displayedItem = self.item


	def build(self, mousePos):
		if className(item) == 'Ledge':
			Ledge(self.world, self.ground, mousePos, width = self.slots[0].output(), height = self.slots[1].output(), color = self.slots[2].output(), allowedAngle = self.slots[3].output())				


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

	def __init__(self, leftpoint, value_type):
		self.width = 60
		self.height = 80
		self.textBox = TextBox(leftpoint, width = 60, height = 80)
		self.value_type = value_type
		self.string = ''
		self.value_index = 0
		self.value_strings = ['' for i in xrange(20)]

		self.groups = allGroup, hoverGroup
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.Surface((60,80))
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect
		self.rect.topleft = leftpoint



	def hover(self):
		if g.INPUT != self:
			pygame.draw.rect(self.image, BLACK, self.textBox.rect, width = 5 )

	def unhover(self):
		if g.INPUT != self:
			pygame.draw.rect(self.image, WHITE, self.textBox.rect, width = 5 )

	def click(self):
		g.INPUT = self
		pygame.draw.rect(self.image, RED, self.textBox.rect, width = 5 )
	def enter(self):
		g.INPUT = False


	def input(self, letter):
		self.string += letter
		self.textBox.writeText(self.string)

	def output(self):
		if value_type == INT:
			return int(self.string)

		elif value_type == TUPLE :
			for i in xrange(len(self.string)):
				if self.string[i] != "," :
					self.value_strings[self.value_index] += self.string[i]
				else :
					self.value_index +=1
			self.value_index += 1
			if self.value_index == 2 :
				return (self.value_strings[0],self.value_strings[1])
			if self.value_index == 3:
				return (self.value_strings[0],self.value_strings[1], self.value_strings[2])

	def kill(self):
		self.textBox.kill()
		pygame.sprite.Sprite.kill(self)






class TextBox(pygame.sprite.Sprite):

	def __init__(self, pos = (0,0), width = 624, height = 120, text_color = BLACK, background_color = None, text = '', fontSize = 32, font = None, justification = 0):

		self.groups = allGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.font = pygame.font.SysFont('None', fontSize)

		self.rect = pygame.Rect(pos, (width, height))
		
		self.text = text
		self.background_color = background_color
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
			self.image = textrect.render_textrect(text, self.font, self.rect, self.text_color, WHITE, justification = self.justification)
			self.image.set_colorkey(WHITE)
		self.text = text

class PropertyBox(object):
	# contient une TextBox et une ValueBox pour self.property
	def __init__(self, name, value_type, leftpoint = (0,0)):
		self.name = name
		self.value_type = value_type
		self.leftpoint = leftpoint
		self.textBox = TextBox(leftpoint, width =60, height = 80, text_color = BLACK, background_color = None, text = name, fontSize = 32, font = None, justification = 0)
		self.valueBox = ValueBox((leftpoint[0]+80, leftpoint[1]), value_type = value_type)

	def kill(self):
		self.textBox.kill()
		self.valueBox.kill()




				




class Button(pygame.sprite.Sprite): #is a button

	def __init__(self, menu, pos, image0 = None, imageHover = None):
		

		pygame.sprite.Sprite.__init__(self)

		self.menu = menu
		menu.buttons.append(self)
		menu.run()

		self.image = image0
		self.image0 = image0
		self.imageHover = imageHover
		self.rect = self.image.get_rect()
		self.rect.topleft = pos[:]

	def hover(self):
		self.image = self.imageHover

	def unhover(self):
		self.image = self.image0

class AbilityButton(Button):

	def __init__(self, menu, pos, ability):

		self.ability = ability

		ability.loadImage()
		Button.__init__(self, menu, pos, ability.image0, ability.imageHover)


	def click(self):
		self.ability.click()