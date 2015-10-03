from b2_classes import *


class AnimatedUnit(GameObject):
	'''GameObject.init() NEEDS : Box2D object to be created(uses self.fixture in update), self.groups, self.image0 to be set '''
	''' so AnimatedUnit needs self.spritesize, self.image0, self.groups to be set'''
	def __init__(self,world, pos):
		self.img_cycleTime = 0.0
		self.img_index = 0
		self.img_interval = 0.2
		self.walking = False
		self.goingRight = True
		self.movingRight = False
		self.movingLeft = False


		self.world = world
		self.body = world.CreateDynamicBody(position = pygame_to_box2d(pos), fixedRotation = False, angularDamping=0.5)
		self.fixture = self.body.CreatePolygonFixture(box = pixel_to_meter(self.spritesize), density = 1, friction = 0.3, userData = self)
		GameObject.__init__(self)


	def update(self, seconds):
		vel = self.body.linearVelocity

		# determine if going right
		if self.movingRight :
			self.goRight()
		elif self.movingLeft :
			self.goLeft()

		self.animate(seconds)
		GameObject.update(self, seconds)

		
	def animate(self, seconds):

		if self.goingRight:
			if self.walking == True:
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
		self.move(15)
		
		self.walking = True
		self.walkingRight = True
		self.goingRight = True
		self.goingLeft = False



	def goLeft(self):
		self.move(-15)

		self.walking = True
		self.walkingLeft = True
		self.goingLeft = True
		self.goingRight = False

	def stop(self):
		self.move(0)

		self.walking = False
		self.walkingRight = False
		self.walkingLeft = False


	def ground(self):

		self.fixture.body.ApplyForce((0,-500), self.fixture.body.worldCenter, wake = True)

	def move(self, desiredVel):
		vel = self.fixture.body.linearVelocity
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

		self.groups = allGroup
		AnimatedUnit.__init__(self,world, pos)

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
