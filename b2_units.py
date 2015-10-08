from b2_classes import *
from b2_weapons import *
import random as rd


class AnimatedUnit(GameObject):
	'''GameObject.init() NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	''' so AnimatedUnit needs self.spritesize, self.image0, self.groups to be set'''
	def __init__(self,world, pos, maxSpeed = 30,accel = 15,slowFactor = 0.4, maxHitpoints = 100, lifetime = -1, gravity = -1):
		self.img_cycleTime = 0.0
		self.img_index = 0
		self.img_interval = 0.2
		self.walking = False
		self.goingRight = True
		self.movingRight = False
		self.movingLeft = False
		self.attacking = False
		self.skip = False

		self.accel = accel
		self.desiredVel = 0
		self.maxSpeed = maxSpeed
		self.slowFactor = slowFactor
		self.image0 = self.img_standingRight[0]


		
		self.world = world
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(pos), fixedRotation = False, angularDamping=0.5)
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter(self.spritesize), density = 1, friction = 0.3, userData = self)

		if gravity != -1:
			self.body.gravityScale = gravity
		GameObject.__init__(self, maxHitpoints, lifetime = lifetime)

		self.lifebar = Lifebar(self)

	def update(self, seconds):
		self.vel = self.body.linearVelocity

		# determine if going right
		if self.movingRight :
			self.goRight()
		elif self.movingLeft :
			self.goLeft()
		self.go(self.desiredVel, self.accel)
		self.animate(seconds)
		GameObject.update(self, seconds)

		
	def animate(self, seconds):

		
		if self.skip == False :
			if self.goingRight:
				if self.attacking :
					pass

				elif self.walking == True:
					self.img_list = self.img_walkingRight
				else :
					self.img_list = self.img_standingRight
			else :
					#temporary walkingRIght for all to test stuff
				if self.walking == True:
					self.img_list = self.img_walkingRight
				else :
					self.img_list = self.img_standingRight
			if len(self.img_list) ==1:
				self.image0 = self.img_list[0]
			else :
				self.img_cycleTime += seconds
				if self.img_cycleTime > self.img_interval:
					self.img_index = (self.img_index+1)%len(self.img_list)
					self.image0 = self.img_list[self.img_index]
					self.img_cycleTime = 0.0
# move laterally 
#---------------------------------------------------------------------------------------------
	def goRight(self):
		self.go(self.maxSpeed, self.accel)
		
		self.walking = True
		self.walkingRight = True
		self.goingRight = True
		self.goingLeft = False

	def goLeft(self):
		self.go(-self.maxSpeed, self.accel)

		self.walking = True
		self.walkingLeft = True
		self.goingLeft = True
		self.goingRight = False

	def custom_goRight(self, maxSpeed, accel):
		self.go(maxSpeed, accel)
		
		self.walking = True
		self.walkingRight = True
		self.goingRight = True
		self.goingLeft = False

	def custom_goLeft(self, maxSpeed, accel):
		self.go(-maxSpeed, accel)
		
		self.walking = True
		self.walkingLeft = True
		self.goingLeft = True
		self.goingRight = False

	def go(self, desiredVel, accel):
		if desiredVel > 0 :
			if self.vel.x < desiredVel :
				self.body.ApplyForce((accel, 0), self.body.worldCenter, wake = True)
		elif desiredVel < 0 :
			if self.vel.x > desiredVel :
				self.body.ApplyForce((-accel, 0), self.body.worldCenter, wake = True)
# ---------------------------------------------------------------------------------------------------

# move up and down assuming 0 gravity
#----------------------------------------------------------------------------------------------------
	def flyUp(self, maxSpeed, accel):
		self.fly(-maxSpeed, accel)

	def flyDown(self, maxSpeed, accel):
		self.fly(maxSpeed, accel)




	def fly(self, desiredVel, accel):
		if desiredVel > 0 :
			if self.vel.y < desiredVel :
				self.body.ApplyForce((0, -accel), self.body.worldCenter, wake = True)
		elif desiredVel < 0 :
			if self.vel.y > desiredVel :
				self.body.ApplyForce((0, accel), self.body.worldCenter, wake = True)
# ---------------------------------------------------------------------------------------------------


	def moveRight(self):
		self.move_x(15)
		
		self.walking = True
		self.walkingRight = True
		self.goingRight = True
		self.goingLeft = False
	def moveLeft(self):
		self.move_x(-15)

		self.walking = True
		self.walkingLeft = True
		self.goingLeft = True
		self.goingRight = False

	def stop(self):
		self.move_x(0)
		self.move_y(0)

		self.walking = False
		self.walkingRight = False
		self.walkingLeft = False

	def slow_x(self):
		self.body.ApplyLinearImpulse((-self.vel.x*self.slowFactor*self.body.mass,0), self.body.worldCenter, wake = True)

	def slow_y(self):
		
		self.body.ApplyLinearImpulse((0,-self.vel.y*self.slowFactor*self.body.mass), self.body.worldCenter, wake = True)



	def ground(self):

		self.fixture.body.ApplyForce((0,-500), self.fixture.body.worldCenter, wake = True)

	

	def move_x(self, desiredVel):
		vel = self.fixture.body.linearVelocity
		velChange = desiredVel - vel.x
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)
	def move_y(self, desiredVel):
		velChange = desiredVel - self.vel.y
		impulse = self.fixture.body.mass * velChange
		self.fixture.body.ApplyLinearImpulse((impulse,0), self.fixture.body.worldCenter, wake = True)


	def jump(self):
		if self.jumps == 0 :

			self.fixture.body.ApplyLinearImpulse((0,9*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
			self.jumps += 1

		elif self.jumps == 1 :
			self.fixture.body.ApplyLinearImpulse((0,15*self.fixture.body.mass), self.fixture.body.worldCenter, wake = True)
			self.jumps += 1

	def kill(self):
		self.lifebar.kill()
		GameObject.kill(self)

class Player(AnimatedUnit):
	spritesheet = None
	img_standingRight = None
	spritesize = (40,64)
	image0 = None
	def __init__(self, world, pos):
		
		self.loadImages()
		self.jump_elapsedTime = 0.0
		self.timeSinceShot = 0.0

		self.weapon1 = Hadouken(self)
		self.weapon2 = Grenade(self)
		self.timeSinceShot1 = 0.0
		self.timeSinceShot2 = 0.0

		self.groups = allGroup, unitGroup, playerGroup
		AnimatedUnit.__init__(self,world, pos, maxSpeed = 30, accel = 120, maxHitpoints = 300)

		# ledge management
		self.feet = pygame.sprite.Sprite()
		self.feet.rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 2)
	def loadImages(self):
			# image loading management
		if Player.img_standingRight == None :
			Player.spritesheet = spritesheet.Spritesheet('images/dog.png')
			Player.img_standingRight  = [Player.spritesheet.getImage((101,45, Player.spritesize), -1)]

			Player.img_walkingRight = Player.spritesheet.getStrip((99,173 ,Player.spritesize), 8,step =89, colorkey = -1)
			
			Player.image0 = Player.img_standingRight[0]
		#--------------------------

	def update(self, seconds):
		self.jump_elapsedTime += seconds
		self.timeSinceShot += seconds
		self.feet.rect.topleft = self.rect.bottomleft
		self.jumps = 0
		# if pygame.sprite.spritecollideany(self.feet, reboundGroup, False):
		# 	self.jumps=0

		AnimatedUnit.update(self, seconds)

	def left_click(self, mousePos):
		if self.timeSinceShot1 >= self.weapon1.cooldown :
			self.weapon1.activate(mousePos)
			self.timeSinceShot = 0.0

	def right_click(self, mousePos):
		if self.timeSinceShot2 >= self.weapon2.cooldown :
			self.weapon2.activate(mousePos)
			self.timeSinceShot2 = 0.0


class EnemyUnit(AnimatedUnit):

	def __init__(self, world, pos, maxSpeed = 20, accel = 50, attack_range = 300, maxHitpoints = 100, gravity = -1):


		
		self.groups = allGroup, enemyGroup, unitGroup
		self.attack_range = attack_range

		AnimatedUnit.__init__(self,world,pos, maxSpeed = maxSpeed, accel = accel, maxHitpoints = maxHitpoints, gravity = gravity)



	def goTo_x(self, pos_x, distance):
		if geo.distance_oneDim(pos_x, self.pos[0]) > distance:
			if pos_x - self.pos[0] >= 0:
				self.goRight()
			else :
				self.goLeft()
		else :
			self.slow_x()
	def goTo_Y(self, pos_y, distance):
		if geo.distance_oneDim(pos_y, self.pos[1]) > distance:
			if pos_y - self.pos[1] <= 0:
				self.flyUp(self.maxSpeed, self.accel)
			else :
				self.flyDown(self.maxSpeed, self.accel)
		else :
			self.slow_y()
	def goTo(self, pos, distance = 10):
		self.goTo_x(pos[0],distance)
		self.goTo_y(pos[1], distance)

	def attack(self, target):
		#self.playAnim_attack()
		self.weapon.activate(rect(target.pos))

class Vampire(EnemyUnit):
	img_standingRight = None
	spritesize = (38,67)

	def __init__(self, world, pos, maxSpeed = 30, accel = 180, target = None):

		self.loadImages()
		self.target = target
		self.weapon = VampireRifle(self)

		EnemyUnit.__init__(self,world, pos, maxSpeed, accel, attack_range = 300)

	def update(self, seconds):
		if self.target :
			self.goTo_x(self.target.pos[0], 250)
			if geo.distance(self.pos, self.target.pos) < self.attack_range :
				self.attack(self.target)
		EnemyUnit.update(self, seconds)


	def loadImages(self):
			# image loading management
		if self.img_standingRight == None :
			Vampire.img_standingRight  = [pygame.image.load('images/vampire/walk_idle/goRight_1.png')]
			Vampire.img_standingRight[0].set_colorkey(WHITE)

			Vampire.img_walkingRight = [
pygame.image.load('images/vampire/walk_idle/goRight_1.png'),			
pygame.image.load('images/vampire/walk_idle/goRight_2.png'),
pygame.image.load('images/vampire/walk_idle/goRight_3.png'),
pygame.image.load('images/vampire/walk_idle/goRight_4.png'),
pygame.image.load('images/vampire/walk_idle/goRight_5.png'),
pygame.image.load('images/vampire/walk_idle/goRight_6.png'),
pygame.image.load('images/vampire/walk_idle/goRight_7.png'),
pygame.image.load('images/vampire/walk_idle/goRight_8.png')
			]

			Vampire.img_walkingLeft = [
pygame.image.load('images/vampire/walk_idle/goLeft_1.png'),			
pygame.image.load('images/vampire/walk_idle/goLeft_2.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_3.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_4.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_5.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_6.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_7.png'),
pygame.image.load('images/vampire/walk_idle/goLeft_8.png')
			]

			Vampire.image0 = Vampire.img_standingRight[0]
		#--------------------------

class Zombie(EnemyUnit):
	img_standingRight = None
	spritesize = (40,62)

	def __init__(self, world, pos, maxSpeed = 30, accel = 120, target = None):

		self.loadImages()
		self.target = target
		self.weapon = VampireRifle(self)

		EnemyUnit.__init__(self,world, pos, maxSpeed, accel, attack_range = 300, maxHitpoints = 500)

	def update(self, seconds):
		if self.target :
			self.goTo_x(self.target.pos[0], 10)
		# 	if geo.distance(self.pos, self.target.pos) < self.attack_range :
		# 		self.attack(self.target)
		EnemyUnit.update(self, seconds)

	def loadImages(self):
			# image loading management
		if self.img_standingRight == None :
			Zombie.img_standingRight  = [pygame.image.load('images/zombie/walk/goRight_1.png').convert()]
			Zombie.img_standingRight[0].set_colorkey(BLACK)

			Zombie.img_walkingRight = [
pygame.image.load('images/zombie/walk/goRight_1.png'),			
pygame.image.load('images/zombie/walk/goRight_2.png'),
pygame.image.load('images/zombie/walk/goRight_3.png'),
pygame.image.load('images/zombie/walk/goRight_4.png'),
pygame.image.load('images/zombie/walk/goRight_5.png'),
pygame.image.load('images/zombie/walk/goRight_6.png'),
pygame.image.load('images/zombie/walk/goRight_7.png'),
pygame.image.load('images/zombie/walk/goRight_8.png'),
pygame.image.load('images/zombie/walk/goRight_9.png'),
pygame.image.load('images/zombie/walk/goRight_10.png')
			]

			Zombie.img_walkingLeft = [
pygame.image.load('images/zombie/walk/goLeft_1.png'),			
pygame.image.load('images/zombie/walk/goLeft_2.png'),
pygame.image.load('images/zombie/walk/goLeft_3.png'),
pygame.image.load('images/zombie/walk/goLeft_4.png'),
pygame.image.load('images/zombie/walk/goLeft_5.png'),
pygame.image.load('images/zombie/walk/goLeft_6.png'),
pygame.image.load('images/zombie/walk/goLeft_7.png'),
pygame.image.load('images/zombie/walk/goLeft_8.png'),
pygame.image.load('images/zombie/walk/goLeft_9.png'),
pygame.image.load('images/zombie/walk/goLeft_10.png')
			]
		



class Skull(EnemyUnit):
	img_standingRight = None
	spritesize = (40,62)

	def __init__(self, world, pos,attack_range = 400, maxSpeed = 15,chargeMaxSpeed = 35, accel = 200, target = None, moveCooldown = 4.0):

		self.loadImages()
		self.target = target
		self.moveCooldown = moveCooldown
		self.moveElapsedTime = moveCooldown 
		self.chargeMaxSpeed = chargeMaxSpeed
		self.fullChargeTime = 8.0
		self.chargeTime = 0.0

		EnemyUnit.__init__(self,world, pos, maxSpeed, accel, attack_range = attack_range, maxHitpoints = 200, gravity = 0)

		self.skip = True

	def update(self, seconds):
		if self.target :
			self.chargeTime += seconds
			speed_factor = geo.minimum(self.chargeTime/self.fullChargeTime, 1)
			if speed_factor >= 0.35:
				self.image0 = self.img_chargeMaxSpeed[0]
			else : 
				self.image0 = self.img_targetting[0]

			self.charge(self.target.pos, speed_factor)

		else :
			#check for target
			for unit in playerGroup :
				if geo.distance(unit.pos, self.pos) <= self.attack_range:
					self.target = unit
			self.image0 = self.img_standingRight[0]
			self.chargeTime = 0.0
			directionVec = (0,0)
			if self.moveElapsedTime >= self.moveCooldown:
				directionVec = (rd.randint(-1,1),rd.randint(-1,1))
			self.go(directionVec[0]*self.maxSpeed, self.accel)
			self.fly(directionVec[1]*self.maxSpeed, self.accel)

		
		EnemyUnit.update(self, seconds)

	def charge(self, pos, speed_factor, distance = 10):
		
		if geo.distance_oneDim(pos[0], self.pos[0]) > distance:
			if pos[0] - self.pos[0] >= 0:
				self.custom_goRight(self.chargeMaxSpeed, speed_factor*self.accel)
			else :
				self.custom_goLeft(self.chargeMaxSpeed, speed_factor*self.accel)
		else :
			self.slow_x()
			
		if geo.distance_oneDim(pos[1], self.pos[1]) > distance:
			if pos[1] - self.pos[1] <= 0:
				self.flyUp(self.chargeMaxSpeed, speed_factor*self.accel)
			else :
				self.flyDown(self.chargeMaxSpeed, speed_factor*self.accel)
		else :
			self.slow_y()

		if geo.distance(pos, self.pos) <= 60 :
			self.chargeTime = 0.0
	def loadImages(self):
		if self.img_standingRight == None :
			Skull.img_standingRight = [pygame.image.load('images/skull/noeyes.png').convert()]
			setColorkey(Skull.img_standingRight[0])
			Skull.img_walkingRight = Skull.img_standingRight
			Skull.img_walkingLeft = Skull.img_standingRight
			Skull.img_targetting = [pygame.image.load('images/skull/eyes.png').convert()]
			setColorkeyList(Skull.img_targetting)
			Skull.img_chargeMaxSpeed = [pygame.image.load('images/skull/charge.png').convert()]
			setColorkeyList(Skull.img_chargeMaxSpeed)



