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
BIGMAP_WIDTH, BIGMAP_HEIGHT=1440,900


BLACK       = (   0,   0,   0)
WHITE       = ( 255, 255, 255)
GREEN       = (   0, 255,   0)
RED         = ( 255,   0,   0)
BLUE        = (   0,   0, 255)
BRIGHTGREEN = (  50, 228,  25)
GREY        = ( 128, 128, 128)

playerSprite_size = (40,62)

allGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
projectileGroup = pygame.sprite.Group()
terrainGroup = pygame.sprite.Group()
ledgeGroup = pygame.sprite.Group()
effectGroup = pygame.sprite.Group()
reboundGroup = pygame.sprite.Group()

class g(object):
	TO_DESTROY = []
	LEFT_CLICK = False
	RIGHT_CLICK = False
	CORNERPOINT = (0, 0)
	OBJECTS = []

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

def box2d_to_pygame(pos):
	return int(pos[0]*PPM), SCREEN_HEIGHT - int(pos[1]*PPM)

def radians_to_degrees(angle):
	return (angle*180/math.pi)%360

def degrees_to_radians(angle):
	return angle*math.pi/180

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

cursor = Cursor()

class AOE(pygame.sprite.DirtySprite) :
	''' REMEMBER TO KILL THOSE AFTER USING '''
	def __init__(self, pos, aoe) :
		pygame.sprite.DirtySprite.__init__(self)
		self.image = pygame.Surface(aoe)
		self.visible = 0
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = pos[:]





class GameObject(pygame.sprite.Sprite):
	'''NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	def __init__(self):
		self.onLedge = False
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.slowing = False
		self.midAir = False
		self.goingRight = False
		self.standing = False
		# jump management
		self.jumps = 0
		self.jump_cooldown = 0.000001
		self.jump_elapsedTime = 0

		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
		self.angle = self.oldAngle

		self.image = pygame.transform.rotate(self.image0, self.angle).convert()
		self.rect = self.image.get_rect()

	def update(self, seconds):

		self.velocity = self.fixture.body.linearVelocity

		#check if mid air
		self.jumps = 0
		if self.velocity.x >= 0 :
			self.goingRight = True
		else :
			self.goingRight = False
		self.angle = radians_to_degrees(self.fixture.body.angle)
		if self.angle != self.oldAngle :
			self.image = pygame.transform.rotate(self.image0, self.angle)
			self.rect = self.image.get_rect()
			self.oldAngle= self.angle
			self.rect.center = vec_to_coordinates(self.fixture.body.position)
		else :
			self.rect.center = vec_to_coordinates(self.fixture.body.position)
		# if self.onLedge :


		# 	if self.velocity.y < 0:
		# 		self.fixture.body.ApplyLinearImpulse((0, -1.3*self.velocity.y*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
		# 	else :
		# 		#EXPERMINTAL
		# 		self.fixture.body.gravityScale = 0
		# 		#self.fixture.body.ApplyForce((0,0.01*10*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
		# else :
		# 	if self.fixture.body.gravityScale == 0 :
		# 		self.fixture.body.gravityScale = 1
		if self.slowing :
			if self.midAir :
				self.slow()
		if self.standing :
			if (1>self.angle or self.angle>359):
				print 'yipee'
				#self.fixture.body.ApplyTorque(-200*self.fixture.body.mass, wake=True)
				self.fixture.body.angularVelocity=0
				self.standing = False


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


	def slow(self):

		self.fixture.body.ApplyForce((0,-500), self.fixture.body.worldCenter, wake = True)


	def goRight(self):
		vel = self.fixture.body.linearVelocity
		desiredVel = 15
		velChange = desiredVel - vel.x
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)


	def goLeft(self):
		vel = self.fixture.body.linearVelocity
		desiredVel = -15
		velChange = desiredVel - vel.x
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)


	def jump(self):
		if self.jumps == 0 :

			self.fixture.body.ApplyLinearImpulse((0,9*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
			self.jumps += 1

		elif self.jumps == 1 :
			self.fixture.body.ApplyLinearImpulse((0,15*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
			self.jumps += 1




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

	def __init__(self, world, size, startingPos,  startingImpulse, bullet=False, image0= None,lifetime = -1, density=1):
		self.world = world
		self.startingPos = startingPos
		self.size = size
		self.startingImpulse = startingImpulse
		self.lifetime= lifetime
		self.alivetime = 0.0
		self.image0 = image0

		body = world.CreateDynamicBody(position = pygame_to_box2d(startingPos), bullet=bullet)
		self.fixture = body.CreatePolygonFixture(box = pixel_to_meter(size), density = density, friction = 0.3, userData = self)
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


		self.owner = owner
		self.power = power
		self.blast_aoe = blast_aoe
		self.blast_power = blast_power
		vec = geo.normalizeVector(pos[0]- owner.rect.centerx, pos[1]- owner.rect.centery)
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.rect.centerx, vec[1]*50+ owner.rect.centery)

		Projectile.__init__(self, self.owner.world, Grenade.size, startingPos, self.impulse, image0 = Projectile_grenade.image0,lifetime = 3)


	def die(self):
		area = AOE(self.rect.center, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - area.rect.centerx, item.rect.centery - area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)



class Projectile_rifle(Projectile):
	image0 = None
	def __init__(self, owner, pos, power = 150):
		# image loading management
		if Projectile_rifle.image0 == None :
			Projectile_rifle.image0 = pygame.Surface((5,5))
			Projectile_rifle.image0.fill(BLACK)
			Projectile_rifle.image0.set_colorkey(WHITE)
		#--------------------------


		self.owner = owner
		self.power = power
		vec = geo.normalizeVector(pos[0]- owner.rect.centerx, pos[1]- owner.rect.centery)
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.rect.centerx, vec[1]*50+ owner.rect.centery)

		Projectile.__init__(self, self.owner.world, rifle.size, startingPos, self.impulse, bullet=True, image0 = Projectile_rifle.image0,lifetime = 1, density=20)


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


		self.owner = owner
		self.power = power
		self.blast_aoe=blast_aoe
		self.blast_power=blast_power
		vec = geo.normalizeVector(pos[0]- owner.rect.centerx, pos[1]- owner.rect.centery)
		self.impulse = (vec[0]*power, vec[1]*power)
		startingPos = (vec[0]*50 +owner.rect.centerx, vec[1]*50+ owner.rect.centery)

		Projectile.__init__(self, self.owner.world, rifle.size, startingPos, self.impulse, image0 = Projectile_megaBall.image0,lifetime = 10, density=5000)

		self.fixture.body.gravityScale = 0

	def die(self):
		area = AOE(self.rect.center, self.blast_aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - area.rect.centerx, item.rect.centery - area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.blast_power,tempVec[1]*self.blast_power)), item.fixture.body.worldCenter, wake = True)

		Projectile.die(self)

	def update(self, seconds):

		Projectile.update(self,seconds)


class Crate(GameObject):
	image0 = pygame.image.load('images/test_crate.png')
	image0.set_colorkey(WHITE)

	def __init__(self,world, pos, angle = 0 ):
		body = world.CreateDynamicBody(position = pygame_to_box2d(pos))
		self.fixture = body.CreatePolygonFixture(box = pixel_to_meter((32,32)), density = 1, friction = 0.3, userData = self)
		self.groups = allGroup, enemyGroup, reboundGroup
		GameObject.__init__(self)






class Barrel(GameObject):
	image0 = pygame.Surface((70,32))
	image0.fill(BLACK)

	def __init__(self,world, pos, angle = 0 ):
		body = world.CreateDynamicBody(position = pygame_to_box2d(pos))
		self.fixture = body.CreatePolygonFixture(box = pixel_to_meter((70,32)), density = 1, friction = 0.3, userData = self)
		self.groups = allGroup, enemyGroup, reboundGroup
		GameObject.__init__(self)


		self.oldAngle = radians_to_degrees(self.fixture.body.angle)
		self.angle = self.oldAngle




class Weapon(object):
	def __init__(self, owner, weapon_range):
		self.owner = owner
		self.weapon_range = weapon_range

	def deactivate(self):
		pass

class BaseballBat(Weapon):
	def __init__(self, owner, power= 40, aoe = (50,50), weapon_range = 200):
		Weapon.__init__(self,owner, weapon_range)
		self.power = power
		self.aoe = aoe


	def activate(self, pos):
		area = AOE(pos, self.aoe)
		collidegroup = pygame.sprite.spritecollide(area, enemyGroup, False)
		vec = geo.normalizeVector(pos[0]- self.owner.rect.centerx, pos[1]- self.owner.rect.centery)
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

	def activate(self, pos): #pos = position mouse
		vec =  geo.normalizeVector(pos[0]- self.owner.rect.centerx, pos[1]- self.owner.rect.centery)

		# push objects from starting point else bug
		push_area = AOE((vec[0]*Grenade.start_range,vec[1]*Grenade.start_range), (28,28))
		collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		Grenade.projectile(self.owner, pos, self.power, blast_aoe = self.blast_aoe, blast_power = self.blast_power)

class rifle(Weapon):
	start_range = 20
	projectile = Projectile_rifle
	size = (5,5)
	weapon_range = 1000
	def __init__(self, owner, power = 150):
		Weapon.__init__(self,owner, rifle.weapon_range)
		self.power = power

	def activate(self, pos):
		vec =  geo.normalizeVector(pos[0]- self.owner.rect.centerx, pos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		push_area = AOE((vec[0]*rifle.start_range,vec[1]*megaBall.start_range), (6,6))
		collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		rifle.projectile(self.owner, pos, power=self.power)

class megaBall(Weapon):
	start_range = 20
	projectile = Projectile_megaBall
	size = (220,220)
	weapon_range = 1000
	def __init__(self, owner, power = 1000):
		Weapon.__init__(self,owner, megaBall.weapon_range)
		self.power = power

	def activate(self, pos):
		vec =  geo.normalizeVector(pos[0]- self.owner.rect.centerx, pos[1]- self.owner.rect.centery)

		# ----------------------------------------
		#push objects from starting point else bug
		push_area = AOE((vec[0]*megaBall.start_range,vec[1]*megaBall.start_range), (221,221))
		collidegroup = pygame.sprite.spritecollide(push_area, enemyGroup, False)

		for item in collidegroup:
			tempVec = geo.normalizeVector(item.rect.centerx - push_area.rect.centerx, item.rect.centery - push_area.rect.centery)
			item.fixture.body.ApplyLinearImpulse(pygameVec_to_box2dVec((tempVec[0]*self.power,tempVec[1]*self.power)), item.fixture.body.worldCenter, wake = True)
		# -------------------------------------------
		megaBall.projectile(self.owner, pos, power=self.power)


class GrapplingHook(Weapon):
	weapon_range = 1000

	def __init__(self,owner, pull_power =500):

		Weapon.__init__(self, owner, GrapplingHook.weapon_range)
		self.pull_power = pull_power

	def activate(self, pos):
		self.hook = Hook(self.owner, pos, self.pull_power)

	def deactivate(self):
		self.hook.kill()



class Hook(pygame.sprite.Sprite):
	def __init__(self, owner, pos, pull_power = 400, traveling_speed = 10):

		self.owner = owner
		self.pos = pos
		self.pull_power = pull_power
		self.traveling_speed = traveling_speed
		self.latched = False
		self.vec = geo.normalizeVector(self.pos[0] - self.owner.rect.centerx,self.pos[1] - self.owner.rect.centery)

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

class Player(GameObject):
	spritesheet = None
	standing = None
	spritesize = (40,64)
	image0 = None
	def __init__(self, world, pos):
		# image loading management
		if Player.standing == None :
			Player.spritesheet = spritesheet.Spritesheet('images/dog.png')
			Player.standing  = Player.spritesheet.getImage((101,45, Player.spritesize), -1)
			Player.image0 = Player.standing
		#--------------------------

		self.weapon = megaBall(self)


		self.world = world
		body = world.CreateDynamicBody(position = pygame_to_box2d(pos), fixedRotation = False, angularDamping=0.5)
		self.fixture = body.CreatePolygonFixture(box = pixel_to_meter(Player.spritesize), density = 1, friction = 0.3, userData = self)




		self.groups = allGroup
		GameObject.__init__(self)




		# ledge management
		self.feet = pygame.sprite.Sprite()
		self.feet.rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 2)

	def update(self, seconds):
		self.jump_elapsedTime += seconds
		self.feet.rect.topleft = self.rect.bottomleft
		if pygame.sprite.spritecollideany(self.feet, reboundGroup, False):
			self.jumps=0

		GameObject.update(self, seconds)

	def left_click(self, mousePos):
		self.weapon.activate(mousePos)

	def right_click(self, mousePos):
		self.weapon.deactivate()

class Ledge(GameObject):

	def __init__(self, world, ground, leftpoint, length, width = 10):
		self.world = world

		self.groups = allGroup, terrainGroup, reboundGroup
		self.image0 = pygame.Surface((length+1,width+1))
		self.image0.fill(WHITE)
		self.image0.set_colorkey(WHITE)
		temp = pygame.Surface((length,width))
		temp.fill(BLACK)
		self.image0.blit(temp, (1,1))



		self.rect = self.image0.get_rect()
		self.rect.topleft = leftpoint
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(self.rect.center))
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter((length,width)), density = 1, friction = 0.3, userData = self)

		GameObject.__init__(self)

		self.joint = self.world.CreateRevoluteJoint(
			bodyA = self.body,
			bodyB = ground,
			anchor = self.body.worldCenter,
			collideConnected = True,
			enableLimit = True,
			lowerAngle = degrees_to_radians(-5),
			upperAngle = degrees_to_radians(5)
			)
