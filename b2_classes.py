import pygame
import Box2D
import math
import spritesheet
import geo
import random





from Box2D.b2 import *


# Constants
# -----------------------------------------------------------
PPM= 20.0 # pixels per meter
TARGET_FPS=60
TIME_STEP=1.0/TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT=800,600

FILEPATH = 'tt.db'



BLACK       = (   0,   0,   0)
WHITE       = ( 255, 255, 255)
GREEN       = (   0, 255,   0)
RED         = ( 255,   0,   0)
BLUE        = (   0,   0, 255)
BRIGHTGREEN = (  50, 228,  25)
GREY        = ( 128, 128, 128)
BROWN       = (165,42,42)
SPRITEGREEN = (76,255,0)


allGroup = pygame.sprite.LayeredUpdates()
enemyGroup = pygame.sprite.Group()
projectileGroup = pygame.sprite.Group()
terrainGroup = pygame.sprite.Group()
ledgeGroup = pygame.sprite.Group()
effectGroup = pygame.sprite.Group()
reboundGroup = pygame.sprite.Group()
hoverGroup = pygame.sprite.Group()
unitGroup = pygame.sprite.Group()
playerGroup = pygame.sprite.Group()
guiGroup = pygame.sprite.Group()





class g(object):
	TO_DESTROY = []
	LEFT_CLICK = False
	RIGHT_CLICK = False
	CORNERPOINT = [0, 0]
	OBJECTS = []
	INPUT = False
	scrollStepx = 3
	scrollStepy = 3
	BIGMAP_WIDTH=1440
	BIGMAP_HEIGHT=900
	TIMEON = True
	TIMERS = []

	#keys
	K_RIGHT = False
	K_LEFT = False

# Utility functions
# ----------------------------------------------------------

def pygame_to_box2d(pygame_position):
	return pygame_position[0]/PPM,(SCREEN_HEIGHT - pygame_position[1])/PPM

def vec_to_coordinates(vec):
	return int(vec.x*PPM), SCREEN_HEIGHT - int(vec.y*PPM)

def pygameVec_to_box2dVec(vec):
	return vec[0], -vec[1]

def pixel_to_meter(pos):
	return (pos[0]/(2*PPM), pos[1]/(2*PPM))

def real_pixel_to_meter(value):
	return value/PPM

def box2d_to_pygame(pos):
	return int(pos[0]*PPM), SCREEN_HEIGHT - int(pos[1]*PPM)

def radians_to_degrees(angle):
	return (angle*180/math.pi)%360

def degrees_to_radians(angle):
	return angle*math.pi/180

def rect(pos):
	return pos[0]- g.CORNERPOINT[0], pos[1] - g.CORNERPOINT[1]

def unrect(pos):
	return pos[0]+ g.CORNERPOINT[0], pos[1] + g.CORNERPOINT[1]

def className(cls):
	return cls.__class__.__name__

def findColor(temp):
	if temp == 1:
		return BLACK
	elif temp == 2:
		return RED
	elif temp == 3:
		return BLUE
	elif temp == 4:
		return GREEN

def setColorkey(image):

	image.set_colorkey(image.get_at((0,0)))
def setColorkeyList(imageList):
	for image in imageList:
		setColorkey(image)


# Cursor
# ----------------------------------------------------------
class Cursor(pygame.sprite.DirtySprite) :
	image = 0
	def __init__(self) :
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface([1, 1])
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.visible = 0


	def update(self) :
		m = pygame.mouse.get_pos()
		self.rect.x = m[0]
		self.rect.y = m[1]
		self.pos = (self.rect.centerx + g.CORNERPOINT[0], self.rect.centery + g.CORNERPOINT[1])

cursor = Cursor()

# Area Of Effect Sprite
# --------------------------------------------------------
class AOE(pygame.sprite.DirtySprite) :
	''' REMEMBER TO KILL THOSE AFTER USING '''
	def __init__(self, pos, aoe) :
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface(aoe)
		self.visible = 0
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.pos = pos[:]
		self.rect.center = pos[:]

# Lifebar
# --------------------------------------------------------

class Lifebar(pygame.sprite.Sprite):

	def __init__(self, owner, distance = 12, size = (40, 5)):

		self.owner = owner
		self.percent = 1.0
		self.old_ownerHitpoints = self.owner.maxHitpoints
		self.distance = distance
		self.size = size


		self.groups = allGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface(size)
		self.image.set_colorkey(BLACK)
		self.rect= self.image.get_rect()

		self.rect.topleft = (self.owner.rect.topleft[0], self.owner.rect.topleft[1] - self.distance)

		self.refresh()

	def update(self, seconds):
		self.rect.topleft = (self.owner.rect.topleft[0], self.owner.rect.topleft[1] - self.distance)
		if self.owner.hitpoints != self.old_ownerHitpoints:
			self.percent = self.owner.hitpoints*1.0 / (self.owner.maxHitpoints*1.0)
			self.old_ownerHitpoints = self.owner.hitpoints
			self.refresh()

	def refresh(self):
		if self.percent != 1.0:

			pygame.draw.rect(self.image, BRIGHTGREEN,(0,0, self.size[0]*self.percent, self.size[1]))
			pygame.draw.rect(self.image, RED, ( self.size[0]*self.percent,  0,  self.size[0]*(1-self.percent), self.size[1]))
		else :
			self.image.fill(BLACK)





# GameObject
# ----------------------------------------------------------
''' a gameobject is a sprite linked to a box2d.body'''

class GameObject(pygame.sprite.Sprite):
	'''NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	def __init__(self, maxHitpoints = 100, lifetime = -1):

		pygame.sprite.Sprite.__init__(self, self.groups)
		self.pos = vec_to_coordinates(self.fixture.body.position)

		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
		self.angle = self.oldAngle
		self.vel = self.fixture.body.linearVelocity
		self.maxHitpoints = maxHitpoints
		self.hitpoints = self.maxHitpoints
		self.lifetime = lifetime


		self.image = pygame.transform.rotate(self.image0, self.angle).convert()
		self.rect = self.image.get_rect()

		hoverGroup.add(self)

	def update(self, seconds):
		if self.lifetime != -1:
			self.alivetime += seconds
			if self.alivetime >= self.lifetime :
				self.die()

		self.vel = self.fixture.body.linearVelocity

		self.angle = radians_to_degrees(self.fixture.body.angle)
		if self.angle != self.oldAngle :
			self.image = pygame.transform.rotate(self.image0, self.angle)
			self.rect = self.image.get_rect()
			self.oldAngle= self.angle
			self.pos = vec_to_coordinates(self.fixture.body.position)
			self.rect.center = rect(vec_to_coordinates(self.fixture.body.position))
		else :
			self.pos = vec_to_coordinates(self.fixture.body.position)


		self.rect.center = rect(self.pos)


	def loseHitpoints(self, value):
		self.hitpoints -= value
		if self.hitpoints < 0 :
			self.die()

	def rotateLeft(self):
		desiredVel = 50
		velChange = desiredVel - self.fixture.body.angularVelocity
		torque = self.fixture.body.mass * velChange
		self.fixture.body.ApplyTorque(torque, wake = True)

	def rotateRight(self):
		desiredVel = -50
		velChange = desiredVel - self.fixture.body.angularVelocity
		torque = self.fixture.body.mass * velChange
		self.fixture.body.ApplyTorque(torque, wake = True)




	def hover(self):
		pass
	def unhover(self):
		pass
	def click(self):
		pass
	def moveRight(self):
		desiredVel = 15
		velChange = desiredVel - vel.x
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)
		self.fixture.body.ApplyForce((0, 10*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True )

	def moveLeft(self):
		desiredVel = -15
		velChange = desiredVel - vel.x
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)
		self.fixture.body.ApplyForce((0, 10*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True )

	def die(self):
		self.kill()


	def kill(self):
		# g.TO_DESTROY.append(self.fixture.body)
		self.world.DestroyBody(self.body)
		pygame.sprite.Sprite.kill(self)





class Timer(object):

	def __init__(self):
		self.elapsedTime = 0.0

	def update(self, seconds):
		self.elapsedTime += seconds
	def reset(self):
		self.elapsedTime = 0.0




class Crate(GameObject):
	image0 = pygame.image.load('images/test_crate.png')
	image0.set_colorkey(WHITE)

	def __init__(self,world, pos, angle = 0 ):
		self.world = world
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(pos))
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter((32,32)), density = 1, friction = 0.3, userData = self)
		self.groups = allGroup, enemyGroup, reboundGroup, unitGroup
		GameObject.__init__(self)






class Barrel(GameObject):


	def __init__(self,world, pos, angle = 0 ):
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(pos))
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter((70,32)), density = 1, friction = 0.3, userData = self)
		self.groups = allGroup, enemyGroup, reboundGroup, unitGroup
		GameObject.__init__(self)


		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
		self.angle = self.oldAngle














# class Ninja(GameObject):
# 	spritesheet = None
# 	standing = None
# 	walkingLeft = None
# 	walkingRight = None
# 	spritesize = (40,66)
# 	image0 = None

# 	def __init__(self, world, pos):
# 		if Ninja.standing == None :
# 			Ninja.spritesheet = spritesheet.Spritesheet()


# 		body = world.CreateDynamicBody(position = pygame_to_box2d(pos))
# 		self.fixture = body.CreatePolygonFixture(box = pixel_to_meter(Ninja.spritesize), density = 1, friction = 0.3, userData = self)
# 		self.groups = allGroup, enemyGroup
# 		GameObject.__init__(self)

# 		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
# 		self.angle = self.oldAngle

# 		self.image = pygame.transform.rotate(self.image0, self.angle).convert()
# 		self.rect = self.image.get_rect()

class Ledge(GameObject):

	def __init__(self, world, ground, leftpoint = (0,0), width= 200, height = 10, color = BLACK, allowedAngle = (-5,5)):
		self.world = world

		self.groups = allGroup, terrainGroup, reboundGroup
		self.image0 = pygame.Surface((width+1,height+1))
		self.image0.fill(WHITE)
		self.image0.set_colorkey(WHITE)
		temp = pygame.Surface((width,height))
		temp.fill(color)
		self.image0.blit(temp, (1,1))

		self.color = color



		self.body = world.CreateDynamicBody(position = pygame_to_box2d(leftpoint))
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter((width,height)), density = 1, friction = 0.3, userData = self)

		GameObject.__init__(self)

		self.joint = self.world.CreateRevoluteJoint(
			bodyA = self.body,
			bodyB = ground.body,
			anchor = self.body.worldCenter,
			collideConnected = True,
			enableLimit = True,
			lowerAngle =degrees_to_radians(allowedAngle[0]),
			upperAngle = degrees_to_radians(allowedAngle[1])
			)



class Doodad(GameObject):

	def __init__(self, world, ground, leftpoint = (0,0), width = 100, height = 100, color = BROWN, density = 1, lifetime = -1):
		self.world = world

		self.groups = allGroup, terrainGroup, reboundGroup,unitGroup
		self.image0 = pygame.Surface((width,height))
		self.image0.fill(WHITE)
		self.image0.set_colorkey(WHITE)
		temp = pygame.Surface((width,height))
		temp.fill(color)
		self.image0.blit(temp, (1,1))
		self.color = color



		self.body = world.CreateDynamicBody(position = pygame_to_box2d(leftpoint), angle = math.pi/4.0)
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter((width,height)), density = density, friction = 0.3, userData = self)


		GameObject.__init__(self, lifetime = lifetime)







class StaticObject(pygame.sprite.Sprite): #used for world boundaries and the like

	def __init__(self, world, leftpoint, size, color = GREY):
		self.body = world.CreateStaticBody(
		position=pygame_to_box2d((leftpoint[0] + size[0]/2,leftpoint[1] + size[1]/2)),
		shapes=polygonShape(box=pixel_to_meter(size))
		)

		self.groups = allGroup, terrainGroup, reboundGroup
		self.leftpoint = leftpoint

		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface(size)
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.topleft = rect(leftpoint)

	def update(self,seconds):

		self.rect.topleft = rect(self.leftpoint)
