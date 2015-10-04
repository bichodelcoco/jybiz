from b2_classes import *


class AnimatedUnit(GameObject):
	'''GameObject.init() NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	''' so AnimatedUnit needs self.spritesize, self.image0, self.groups to be set'''
	def __init__(self,world, pos, maxSpeed = 30,accel = 15,slowFactor = 0.4, health = 100):
		self.img_cycleTime = 0.0
		self.img_index = 0
		self.img_interval = 0.2
		self.walking = False
		self.goingRight = True
		self.movingRight = False
		self.movingLeft = False
		self.attacking = False

		self.accel = accel
		self.desiredVel = 0
		self.maxSpeed = maxSpeed
		self.slowFactor = slowFactor


		self.world = world
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(pos), fixedRotation = False, angularDamping=0.5)
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter(self.spritesize), density = 1, friction = 0.3, userData = self)
		GameObject.__init__(self, health)


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

	def go(self, desiredVel, accel):
		if desiredVel > 0 :
			if self.vel.x < desiredVel :
				self.body.ApplyForce((accel, 0), self.body.worldCenter, wake = True)
		elif desiredVel < 0 :
			if self.vel.x > desiredVel :
				self.body.ApplyForce((-accel, 0), self.body.worldCenter, wake = True)

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

class Player(AnimatedUnit):
	spritesheet = None
	img_standingRight = None
	spritesize = (40,64)
	image0 = None
	def __init__(self, world, pos):
		
		self.loadImages()
		self.jump_elapsedTime = 0.0
		self.timeSinceShot = 0.0

		self.weapon = Hadouken(self)
		self.timeSinceShot = 0.0

		self.groups = allGroup, unitGroup
		AnimatedUnit.__init__(self,world, pos, maxSpeed = 30, accel = 120, health = 300)

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
		if self.timeSinceShot >= self.weapon.cooldown :
			self.weapon.activate(mousePos)
			self.timeSinceShot = 0.0

	def right_click(self, mousePos):
		self.weapon.deactivate()

class EnemyUnit(AnimatedUnit):

	def __init__(self, world, pos, maxSpeed = 20, accel = 50, attack_range = 300, health = 100):


		
		self.groups = allGroup, enemyGroup, unitGroup
		self.attack_range = attack_range

		AnimatedUnit.__init__(self,world,pos, maxSpeed = maxSpeed, accel = accel, health = health)



	def goTo_x(self, pos_x, distance):
		if geo.distance_oneDim(pos_x, self.pos[0]) > distance:
			if pos_x - self.pos[0] >= 0:
				self.goRight()
			else :
				self.goLeft()
		else :
			self.slow_x()

	def attack(self, target):
		#self.playAnim_attack()
		self.weapon.activate(target.pos)

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
			Vampire.img_standingRight.set_colorkey(WHITE)

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

		



