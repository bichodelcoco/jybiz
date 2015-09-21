import pygame
from b2_classes import *
import textrect


INT = 1
TUPLE = 2
COLOR = 3

''' ------------ GUI ---------- '''
class EditorGUI(object): #contains value boxes
	
	def __init__(self, item = None):
		self.slots = [0 for i in xrange(10])
		self.posList = [()]

		self.loadItem(item)
		self.displayedItem = None

	def loadItem(self, item):
		self.slots = [0 for i in xrange(10)]
		self.item = item
		if className(item) == 'Ledge' :
			self.slots[0] = PropertyBox('leftpoint', TUPLE)
			self.slots[1] = PropertyBox('length', INT)
			self.slots[2] = PropertyBox('width', INT)
			self.slots[3] = PropertyBox('color', COLOR)



		for i in xrange(10)


	def update(self):
		if self.item != self.displayedItem:

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
	#carré de x sur y blanc entouré de noir dans lequel on peut entrer des valeures

class PropertyBox(object):
	# contient une TextBox et une ValueBox pour self.property
	def __init__(name, value_type)



class TextBox(pygame.sprite.Sprite):

	def __init__(self, pos = (200,0), width = 624, height = 120, text_color = BLACK, background_color = None, text = "caca", fontSize = 32, font = None, justification = 0):

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