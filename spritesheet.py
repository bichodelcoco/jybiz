import pygame

# ----------- SPRITE SHEET MANAGEMENT -------
class Spritesheet(object) :
	def __init__(self, filename) :
		try:
			self.sheet = pygame.image.load(filename)
		except pygame.error, message:
			print 'Unable to load spritesheet image:', filename
			raise SystemExit, message
	# load a specific image 
	def getImage(self, (x, y, dimension), colorkey = None): #colorkey is the transparent color
		# loads image at (x,y) with widthXheight dimension
		rect = pygame.Rect(x,y,dimension[0],dimension[1])
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0,0), rect)
		if colorkey is not None :
			if colorkey == -1 : # -1 value automatically finds the colorkey (takes the pixel color of (0,0))
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image
	# load multiple images into a list
	def getImages(self, rects, colorkey = None):
		#loads images into a list form a list of coordinates rect format : (x,y,[width, height])
		return [self.getImage((rect[0], rect[1], rect[2]), colorkey) for rect in rects]
	# load a whole strip of images from starting position
	def getStrip(self, (x, y ,dimension), imageNbr, colorkey = None):
		tups = [(x+ dimension[0]*i, y, dimension) for i in range(imageNbr)]
		return self.getImages(tups, colorkey)
	def getStripInverse(self, (x, y ,dimension), imageNbr, colorkey = None): #gets strip but goes from right to left
		tups = [(x- dimension[0]*i, y, dimension) for i in range(imageNbr)]
		return self.getImages(tups, colorkey)
	