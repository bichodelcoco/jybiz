import pygame
import Box2D
import math
import spritesheet
import geo


from Box2D.b2 import *


# Constants
# -----------------------------------------------------------
PPM= 20.0 # pixels per meter
TARGET_FPS=60
TIME_STEP=1.0/TARGET_FPS
SCREEN_WIDTH, SCREEN_HEIGHT=1024,768



BLACK       = (   0,   0,   0)
WHITE       = ( 255, 255, 255)
GREEN       = (   0, 255,   0)
RED         = ( 255,   0,   0)
BLUE        = (   0,   0, 255)
BRIGHTGREEN = (  50, 228,  25)
GREY        = ( 128, 128, 128)
BROWN       = (165,42,42)


allGroup = pygame.sprite.LayeredUpdates()
enemyGroup = pygame.sprite.Group()
projectileGroup = pygame.sprite.Group()
terrainGroup = pygame.sprite.Group()
ledgeGroup = pygame.sprite.Group()
effectGroup = pygame.sprite.Group()
reboundGroup = pygame.sprite.Group()
hoverGroup = pygame.sprite.Group()
unitGroup = pygame.sprite.Group()

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
		self.rect.center = rect(pos)




# GameObject
# ----------------------------------------------------------
''' a gameobject is a sprite linked to a box2d.body'''

class GameObject(pygame.sprite.Sprite):
	'''NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	def __init__(self):

		pygame.sprite.Sprite.__init__(self, self.groups)
		self.pos = vec_to_coordinates(self.fixture.body.position)
		
		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
		self.angle = self.oldAngle
		self.vel = self.fixture.body.linearVelocity


		self.image = pygame.transform.rotate(self.image0, self.angle).convert()
		self.rect = self.image.get_rect()

		hoverGroup.add(self)

	def update(self, seconds):

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








	def stand(self):
		desiredVel=10
		#if 0<=self.fixture.body.angle<math.pi:
		if 10<self.angle<350:
			self.standing=True

			velChange = desiredVel - self.fixture.body.angularVelocity
			self.fixture.body.angularVelocity=desiredVel
			#self.fixture.body.ApplyTorque(velChange*self.fixture.body.mass, wake = True)
		# elif math.pi<self.fixture.body.angle<2*math.pi:
		# 	velChange = -desiredVel - self.fixture.body.angularVelocity
		# 	self.fixture.body.ApplyTorque(velChange*self.fixture.body.mass, wake = True)

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

	def kill(self):
		g.TO_DESTROY.append(self.fixture.body)
		pygame.sprite.Sprite.kill(self)

class Projectile(GameObject):
	''' PROJECTILE.IMAGE0 SHOLD BE HORIZONTAL FACING RIGHT'''

	def __init__(self, world, owner, size, startingPos,  startingImpulse, bullet=False, image0= None,lifetime = -1, density=1, boxShape = True, angle = 0):
		self.world = world
		self.owner = owner
		self.startingPos = startingPos
		self.size = size
		self.startingImpulse = startingImpulse
		self.lifetime= lifetime
		self.alivetime = 0.0
		self.image0 = image0

		if boxShape :
			self.body = world.CreateDynamicBody(position = pygame_to_box2d(startingPos), bullet=bullet)
			self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter(size), density = density, friction = 0.3, userData = self)
		self.groups = allGroup, projectileGroup, reboundGroup
		GameObject.__init__(self)

		self.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec(self.impulse), self.fixture.body.worldCenter, wake = True)



	def update(self, seconds):
		self.alivetime += seconds
		if self.alivetime >= self.lifetime :
			self.die()
		GameObject.update(self,seconds)

	def die(self):
		self.kill()

class Projectile_grenade(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 40, blast_aoe = (200,200),blast_power = 500):
		# image loading management
		if Projectile_grenade.image0 == None :
			Projectile_grenade.image0 = pygame.image.load('images/weapons/grenade.png')
			Projectile_grenade.image0.set_colorkey(WHITE)
		#--------------------------


		
		self.power = power
		self.blast_aoe = blast_aoe
		self.blast_power = blast_power
		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, Grenade.size, startingPos, self.impulse, image0 = Projectile_grenade.image0,lifetime = 3)


	def die(self):
		area = AOE(self.pos, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, unitGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.pos[0]- area.pos[0], item.pos[1] - area.pos[1])
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)



class Projectile_Rifle(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 150):
		# image loading management
		if Projectile_Rifle.image0 == None :
			Projectile_Rifle.image0 = pygame.Surface((5,5))
			Projectile_Rifle.image0.fill(BLACK)
			Projectile_Rifle.image0.set_colorkey(WHITE)
		#--------------------------


		
		self.power = power
		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world,owner, Rifle.size, startingPos, self.impulse, bullet=True, image0 = Projectile_Rifle.image0,lifetime = 1, density=20)


	def update(self, seconds):

		Projectile.update(self,seconds)


class Projectile_megaBall(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 1000, blast_aoe = (230,230), blast_power = 10):


		# image loading management
		if Projectile_megaBall.image0 == None :
			Projectile_megaBall.image0 = pygame.image.load('images/weapons/megaBall_big.png')
			Projectile_megaBall.image0.set_colorkey(WHITE)
		#--------------------------

		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		
		self.power = power
		self.blast_aoe=blast_aoe
		self.blast_power=blast_power
		
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.pos[0], vec[1]*50+ owner.pos[1])

		Projectile.__init__(self, owner.world, owner, Rifle.size, startingPos, self.impulse, image0 = Projectile_megaBall.image0,lifetime = 10, density=5000)

		self.fixture.body.gravityScale = 0

	def die(self):
		area = AOE(self.pos, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.pos[0] - area.pos[0], item.pos[1] - area.pos[1])
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)

class Projectile_Hadouken(Projectile):
	start_range = 70
	image0 = None
	size = (58,58)

	def __init__(self, owner, pos, speed = 5, power = 800, recoil = 10):

		vec = (pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		if vec[1] <= 0:
			self.angle =geo.vecAngle((1,0), vec)
		else :
			self.angle = -geo.vecAngle((1,0), vec)
		
		# image loading management
		if Projectile_Hadouken.image0 == None :
			Projectile_Hadouken.image0= pygame.image.load('images/weapons/hadouken.png')
			#Projectile_Hadouken.image0 = pygame.transform.rotate(Projectile_Hadouken.image0, self.angle)
			Projectile_Hadouken.image0.set_colorkey(WHITE)
		#--------------------------

		self.power = power
		self.speed = speed
		self.recoil = recoil

		self.world = owner.world
		self.body = self.world.CreateDynamicBody(position = pygame_to_box2d(pos), bullet = True, angle = self.angle)
		self.body.gravityScale = 0
		self.fixture = self.body.CreateCircleFixture(radius = real_pixel_to_meter(29), restitution = 0.8, density = 500, friction = 0, userData = self)


		vec = geo.normalizeVector(pos[0]- owner.pos[0], pos[1]- owner.pos[1])
		self.impulse = (vec[0]*self.power, vec[1]* self.power)
		startingPos = (vec[0]*self.start_range + owner.pos[0], vec[1]*self.start_range + owner.pos[1])

		Projectile.__init__(self, self.world, owner, self.size, startingPos, self.impulse,bullet= True, image0 = self.image0, lifetime = 1.5, boxShape = False)







class Crate(GameObject):
	image0 = pygame.image.load('images/test_crate.png')
	image0.set_colorkey(WHITE)

	def __init__(self,world, pos, angle = 0 ):
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




class Weapon(object):
	def __init__(self, owner, weapon_range, cooldown = 0.0):
		self.owner = owner
		self.weapon_range = weapon_range
		self.cooldown = cooldown

	def deactivate(self):
		pass

class BaseballBat(Weapon):
	def __init__(self, owner, power= 40, aoe = (50,50), weapon_range = 200):
		Weapon.__init__(self,owner, weapon_range)
		self.power = power
		self.aoe = aoe


	def activate(self, mousePos):
		area = AOE(mousePos, self.aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		vec = geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
		for item in collidegroup :
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((vec[0]*self.power,vec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		area.kill()


class Grenade(Weapon):
	start_range = 20
	projectile = Projectile_grenade
	size = (25,25)
	weapon_range = 1000 #distance a laquelle tu peux cliquer
	def __init__(self, owner, power = 40, blast_aoe = (100,100), blast_power = 500):#power : init velocity
		Weapon.__init__(self,owner, Grenade.weapon_range)
		self.power = power
		self.blast_aoe = blast_aoe
		self.blast_power = blast_power

	def activate(self, mousePos): #pos = position mouse
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# push objects from starting point else bug
		# push_area = AOE((self.owner.pos[0] + vec[0]*Grenade.start_range,self.owner.pos[1] + vec[1]*Grenade.start_range), (28,28))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Grenade.projectile(self.owner, pos, self.power, blast_aoe = self.blast_aoe, blast_power = self.blast_power)

class Rifle(Weapon):
	start_range = 20
	projectile = Projectile_Rifle
	size = (5,5)
	weapon_range = 1000
	def __init__(self, owner, power = 150):
		Weapon.__init__(self,owner, Rifle.weapon_range)
		self.power = power

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		# push_area = AOE((vec[0]*Rifle.start_range,vec[1]*megaBall.start_range), (6,6))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		Rifle.projectile(self.owner, pos, power=self.power)

class megaBall(Weapon):
	start_range = 20
	projectile = Projectile_megaBall
	size = (220,220)
	weapon_range = 1000
	def __init__(self, owner, power = 1000):
		Weapon.__init__(self,owner, megaBall.weapon_range)
		self.power = power

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		push_area = AOE((vec[0]*megaBall.start_range,vec[1]*megaBall.start_range), (221,221))
		collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		megaBall.projectile(self.owner, pos, power=self.power)

class Hadouken(Weapon):
	start_range = 70
	projectile = Projectile_Hadouken
	weapon_range = 2000
	def __init__(self, owner, speed = 5, recoil = 10, power = 90000, cooldown = 0.0 ):
		Weapon.__init__(self, owner, Hadouken.weapon_range)
		self.speed = speed
		self.recoil = recoil
		self.power =power
		self.cooldown = cooldown

	def activate(self, mousePos):
		vec =  geo.normalizeVector(mousePos[0]- self.owner.rect.centerx, mousePos[1]- self.owner.rect.centery)
		# ----------------------------------------
		# #push objects from starting point else bug
		# push_area = AOE((self.owner.pos[0] + vec[0]*Hadouken.start_range,self.owner.pos[1] + vec[1]*Hadouken.start_range), (221,221))
		# collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		# for item in collidegroup:
		# 	tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
		# 	item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		pos = (self.owner.pos[0] + self.start_range*vec[0],self.owner.pos[1] + self.start_range*vec[1])
		self.projectile(self.owner, pos, power= self.power, speed = self.speed, recoil = self.recoil)




class GrapplingHook(Weapon):
	weapon_range = 1000

	def __init__(self,owner, pull_power =500):

		Weapon.__init__(self, owner, GrapplingHook.weapon_range)
		self.pull_power = pull_power

	def activate(self, mousePos):
		self.hook = Hook(self.owner, mousePos, self.pull_power)

	def deactivate(self):
		self.hook.kill()



class Hook(pygame.sprite.Sprite):
	def __init__(self, owner, mousePos, pull_power = 400, traveling_speed = 10):

		self.owner = owner
		self.mousePos = mousePos
		self.pull_power = pull_power
		self.traveling_speed = traveling_speed
		self.latched = False
		self.vec = geo.normalizeVector(self.mousePos[0] - self.owner.rect.centerx,self.mousePos[1] - self.owner.rect.centery)

		self.groups = allGroup, effectGroup
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.image = pygame.Surface((10,10))
		self.image.fill(GREY)

		self.rect = self.image.get_rect()
		self.rect.center = self.owner.rect.center[:]

	def update(self, seconds):

		if self.latched == False :
			temp = pygame.sprite.spritecollideany(self, terrainGroup)
			if temp :
				self.latched = True


			else :
				self.rect.centerx += self.vec[0]* self.traveling_speed
				self.rect.centery += self.vec[1]* self.traveling_speed
		else :
			self.pull_vec = geo.normalizeVector(self.rect.centerx -self.owner.rect.centerx, self.rect.centery -self.owner.rect.centery)
			self.owner.fixture.body.ApplyForce(pygameVec_to_box2dVec((self.pull_vec[0]*self.pull_power, self.pull_vec[1]*self.pull_power)), self.owner.fixture.body.worldCenter, wake = True)










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

	def __init__(self, world, ground, leftpoint = (0,0), width = 100, height = 100, color = BROWN, density = 1):
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


		GameObject.__init__(self)







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



